import requests
import sys
from typing import Optional
from pathlib import Path
import json
import csv
import os
import datetime

def fetch_main(types: list[str], output_dir: Path):



    # determine which backup-files shall be fetched
    if types:
        for t in types:
            if t not in ['records', 'entities', 'relations', 'acquisitions']:
                sys.exit(f"Value of `--type`-option is invalid: {t}.\nUse 'records', 'entities', 'relations' or 'acquisitions'")
    else:
        sys.exit("No fetch types specified...")

    operations: dict[str, str] = {
        "records" : "getBackupOASMeta",
        "entities" : "getBackupEntityMeta",
        "relations" : "getBackupRelationEntityMeta",
        "acquisitions" : "getBackupRegnoteMeta"
    }
    

    for t in types:
        fetch_backup(operation=operations[t], cursor=None, output_dir=output_dir)
       
    print(f"Fetching of {types} done...")
    sys.exit(0)





def fetch_backup(operation: str, output_dir: Path, cursor: Optional[str] = None):
    '''
    Get data and append to csv.    
    '''

    output_filenames: dict[str, str] = {
        "getBackupOASMeta" : "oas_backup",
        "getBackupEntityMeta" : "entities_backup",
        "getBackupRelationEntityMeta" : "entity_relations_backup",
        "getBackupRegnoteMeta" : "acquisitions_backup"
    }


    year: str = datetime.date.today().year
    month: str = datetime.date.today().month
    day: str = datetime.date.today().day
    # 2024-03-15_oas_backup.csv
    output_dir = output_dir / f"{year}-{month}-{day}_{output_filenames[operation]}.csv"
    
    
    if output_dir.exists():
        print(f"Output file {output_dir} exits...deleting...")
        output_dir.unlink()
   
    cursor = "start"
    count: int = 1
    failed: bool = False

    while cursor and not failed:

        with open(output_dir, "a", encoding='utf-8', newline='\n') as file:
            
            url = "https://openaws.appspot.com/sam_tools_v2"
            body: dict = {
                "client_secret": os.environ["secret_key"],
                "operation": operation
            }
            if cursor and cursor != "start":
                body["data"] = json.dumps({"cursor": cursor})
        
            response = requests.post(url, data=body)
            
            response_json: dict = json.loads(response.text)
            
            if response_json["status_code"] == 0:
                pass
            else:
                failed = True
                print("Fetch failed...")
                break

            header: list[str] = response_json["result"]["data"][0]
            data: list = response_json["result"]["data"][1:]
            data_: list[dict] = [dict(zip(header, row)) for row in data ]

            fieldnames = header
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if count == 1:
                writer.writeheader()

            writer.writerows(data_)

            cursor = response_json["result"].get("cursor", None)

            print("Wrote rows...", count)
            count += 1

    if failed:
        if output_dir.exists():
            output_dir.unlink()            
            sys.exit("Download failed, partial downloaded file deleted...")

    return


    