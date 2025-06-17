import csv
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Optional

import requests  # type: ignore


def get_date() -> str:
    return datetime.datetime.now().date()
    # year: int = datetime.date.today().year
    # month: int = datetime.date.today().month
    # day: int = datetime.date.today().day
    # # 2024-03-15_oas_backup.csv

    # month_: str = ""
    # day_: str = ""

    # month_ = f"0{month}" if month < 10 else f"{month}"

    # day_ = f"0{day}" if day < 10 else f"{day}"

    # return f"{year}-{month_}-{day_}"


def query_endpoint(operation: str, data: Optional[dict] = None) -> dict:
    """Handles api-calls regarding registration jobs and updates."""
    out: list = []
    url = "https://openaws.appspot.com/sam_tools_v2"
    default: dict = {
        "client_secret": os.environ["SECRET_KEY"],
        "operation": operation,
    }
    if data:
        default["data"] = json.dumps(data)

    r = requests.post(url, data=default)
    resp: dict = json.loads(r.text)

    out.extend(list_ for list_ in resp.get("result"))

    cursor: str = resp.get("cursor")
    while cursor:
        default: dict = {"client_secret": os.environ["SECRET_KEY"], "operation": operation, "data": {"cursor": cursor}}
        if data:
            default["data"].update(data)
        default["data"] = json.dumps(default["data"])
        r = requests.post(url, data=default)
        resp: dict = json.loads(r.text)

        out.extend(list_ for list_ in resp.get("result")[1:])
        cursor = resp.get("cursor")

    return {"status_code": resp["status_code"], "result": out}


def fetch_jobs(output_dir: Path, operation: str):
    if operation not in ["update", "registration"]:
        sys.exit(f"-type value must be 'update' or 'registration'. Received {operation}")

    meta_file = output_dir / f"{get_date()}_{operation}_meta.csv"
    changes_file = output_dir / f"{get_date()}_{operation}_changes.csv"

    if meta_file.exists():
        print(f"Output file {meta_file} already exits. Deleting...")
        meta_file.unlink()

    if changes_file.exists():
        print(f"Output file {changes_file} already exits. Deleting...")
        changes_file.unlink()

    resp: dict = query_endpoint(f"fetch{'Reg' if operation == 'registration' else 'Update'}JobMetaList")
    if resp["status_code"] != 0:
        sys.exit(str(resp))

    results: list[list] = resp["result"]
    print(f"Total {len(results) - 1} results")
    with open(meta_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for row in results:
            writer.writerow(row)

    content: list[list] = []  # all results and its changes

    for result in results[1:]:
        job_id: int = result[0]
        resp: dict = query_endpoint("fetchJobChangeLog", {"job_id": job_id})
        changes: list[list] = resp["result"]
        print(f"Processed {len(changes)} changes for job {job_id}")
        for change in changes:
            row: list = [job_id, *change]
            content.append(row)

    # write all changes
    with open(changes_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["job_id", "change_id", "affected_group", "operation", "key", "value"])
        for row in content:
            writer.writerow(row)


def fetch_backup(operation: str, output_dir: Path, cursor: Optional[str] = None):
    """Get data and append to csv."""
    output_filenames: dict[str, str] = {
        "getBackupOASMeta": "oas_backup",
        "getBackupEntityMeta": "entities_backup",
        "getBackupRelationEntityMeta": "entity_relations_backup",
        "getBackupRegnoteMeta": "acquisitions_backup",
    }

    output_file = output_dir / f"{get_date()}_{output_filenames[operation]}.csv"

    if output_file.exists():
        print(f"Output file {output_file} already exits...deleting...")
        output_file.unlink()

    cursor = "start"
    count: int = 1
    failed: bool = False

    while cursor and not failed:
        with open(output_file, "a", encoding="utf-8", newline="\n") as file:
            url = "https://openaws.appspot.com/sam_tools_v2"
            body: dict = {"client_secret": os.environ["SECRET_KEY"], "operation": operation}
            if cursor and cursor != "start":
                body["data"] = json.dumps({"cursor": cursor})

            response = requests.post(url, data=body)
            response_json: dict = json.loads(response.text)

            if response_json["status_code"] != 0:
                failed = True
                print(str(response_json))
                break

            header: list[str] = response_json["result"]["data"][0]
            data: list = response_json["result"]["data"][1:]
            data_: list[dict] = [dict(zip(header, row)) for row in data]

            fieldnames = header
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if count == 1:
                writer.writeheader()

            writer.writerows(data_)

            cursor = response_json["result"].get("cursor", None)

            print("Wrote rows...", count)
            count += 1

    if failed and output_file.exists():
        output_file.unlink()
        sys.exit("Download failed, partial downloaded file deleted...")

    return


def fetch_main(types: list[str], output_dir: Path):
    # determine which backup-files shall be fetched
    operations: dict[str, str] = {
        "records": "getBackupOASMeta",
        "entities": "getBackupEntityMeta",
        "relations": "getBackupRelationEntityMeta",
        "acquisitions": "getBackupRegnoteMeta",
        "registrations": "fetchRegistrations",
        "updates": "fetchUpdates",
    }

    for t in types:
        if t not in operations:
            sys.exit(
                f"""Value of `--type`-option is invalid: {t}.\nUse 'records', 'entities',
                'relations', 'registrations', 'updates' or 'acquisitions'"""
            )

    for t in types:
        if t == "registrations":
            fetch_jobs(output_dir, "registration")
        elif t == "updates":
            fetch_jobs(output_dir, "update")
        else:
            fetch_backup(operation=operations[t], cursor=None, output_dir=output_dir)

    print(f"Fetching of {types} done...")
    sys.exit(0)
