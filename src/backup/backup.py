import argparse
import csv
import json
import os
import sys
from argparse import _MutuallyExclusiveGroup
from collections.abc import Sequence
from pathlib import Path
from typing import Any
from typing import Optional

from backup import __version__
from backup.fetch_data import fetch_main
from backup.settings import FIELDS
from backup.settings import FIELDS_TRANSLATED


def main(argv: Optional[Sequence[str]] = None) -> int:
    output: list[list[Any]] = []

    parser = argparse.ArgumentParser(
        description=(
            "Backup lets you fetch backup files from Google Cloud Platform, and generate\n"
            "filtered lists of record_ids from the fetched backup files.\n\n"
            "You can print the output in the terminal or save it to one or more csv-files, that\n"
            "can be directly imported to SAM to create new update jobs.\n\n"
            "Use 'backup fetch' to fetch backup files of records, registrations, entities, jobs...\n"
            "Use 'backup list' to view information about all the possible search filters.\n"
            "Use 'backup search' to search a given backup file."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)

    # subparsers
    subs = parser.add_subparsers(
        title="commands",
        dest="command",
        # description="description str, set to replace the {} list of commands",
        # metavar="",
    )

    # fetch subcommand
    fetch = subs.add_parser(
        "fetch",
        help="Fetch backup-files from Google Cloud Platform",
        description=(
            "Fetch backup files from Google Cloud Platform.\n\n"
            "Use it to download backups of 'records', 'entities', 'relations', 'acquisitions',\n"
            "'registrations' and 'updates'.By default all backups are downloaded, use any number \n"
            "of --type to specify which files "
            "to fetch.\n\n"
            "Example: 'backup fetch --type records entities --output-dir z:/backups/GCP'"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    fetch.add_argument(
        "--type",
        metavar="backup_type",
        nargs="+",
        # action='append',
        type=str,
        help="",
        choices=["records", "entities", "relations", "acquisitions", "registrations", "updates"],
    )
    fetch.add_argument(
        "--key",
        metavar="secret_key",
        nargs="?",
        type=str,
        help="Key for fetching online data...",
    )
    fetch.add_argument(
        "--fetch-output-dir",
        metavar="fetch_output_dir_",
        type=Path,
        help="Specify path to csv output",
    )

    # list subcommand
    subs.add_parser(
        "list",
        help="List all valid search fields and their associated operators",
        description=(
            "Lists all the metadata fields that are available for filtering, along with the "
            "operators that each field allows.\n\n"
            "Use one or more of these metadata fields to filter the output from `backup search`"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Search subcommand
    search = subs.add_parser(
        "search",
        help="Search a backupfile using multiple filters",
        description=(
            "Filters the csv formatted backup database:\n"
            "Apply any number of --filter \n"
            "Use --filestem to specify a custom filestem for the output file(s).\n"
            "\n\n"
            'ex.1 field is "id-field"\n'
            "--filter Samling equalTo 1\n"
            "or\n"
            "--filter Samling contains Salling\n\n"
            "ex.2 if the field is a dictionary, and target search is in a key's value:\n"
            '--filter "Administrative data" contains '
            '"Bestillingsinformation:negativsamlingen 1970"\n\n'
            "ex.3 if the field is a dictionary, and filter after target has a certain key:\n"
            '--filter "Administrative data" hasKey Bestillingsinformation\n\n'
            "ex.4 the field is a dictionary and the key is known and filter on the value:\n"
            '--filter "Beskrivelsesdata" contains Typer:Farve\n\n'
            'ex.5 use the "null" keyword to filter for any entry has a certain field:\n'
            "--filter Samling equalTo null or --filter Samling notEqualTo null\n\n"
            "All user inputs are case-insensitive. Field names are case-sensitive."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    search.add_argument(
        "csv_path",
        metavar="input_csv_file_path",
        type=str,
        help="Path to the backup database csv file.",
    )

    # print or save result
    output_format: _MutuallyExclusiveGroup = search.add_mutually_exclusive_group(required=True)
    output_format.add_argument("--output-dir", type=str, help="Path to the output directory for resulting csv file(s).")
    output_format.add_argument(
        "--print",
        action="store_true",
        help="Print the results instead of saving to files",
    )

    search.add_argument("--filestem", type=str, help="If saving to csv-files, optionally specify the filestem")

    search.add_argument(
        "--extra-field",
        type=str,
        action="append",
        help="Include one or more output columns besides the default 'id'-column",
    )

    search.add_argument(
        "--filter",
        type=str,
        nargs=3,
        action="append",
        help="Add one or more filters to limit the results",
    )

    search.add_argument("--or_", action="store_true", help="Use OR between filters instead of default AND")

    args = parser.parse_args(argv)

    if not args.command or args.command not in ["list", "search", "fetch"]:
        sys.exit("You must use the 'list', 'search' or 'fetch' subcommand")

    if args.command == "list":
        for key in FIELDS_TRANSLATED.keys():
            print(key.ljust(25), end="")
            print(", ".join(FIELDS[FIELDS_TRANSLATED[key]].keys()))
        sys.exit(0)

    elif args.command == "fetch":
        if args.key:
            os.environ["SECRET_KEY"] = args.key

        else:
            config_file: Path = Path.home() / ".backup.config"

            if not config_file.exists() and args.command == "fetch":
                print(f"Specify secret key in {config_file} to enable fetch...")
                with open(config_file, "w", encoding="utf-8", newline="\n") as file:
                    to_file: dict = {"secret_key": ""}
                    file.write(json.dumps(to_file))
            else:
                with open(config_file, encoding="utf-8", newline="\n") as file:
                    print("Loading secret key for fetch...")
                    content = file.read()
                    json_content: dict = json.loads(content)
                    if json_content.get("secret_key"):
                        os.environ["SECRET_KEY"] = json_content["secret_key"]
                        print("Loaded: Secret key for fetch...ok.")
                    else:
                        sys.exit(f"No secret key specified in {config_file}")

        fetch_main(types=args.type, output_dir=args.fetch_output_dir)

    if args.csv_path:
        input_csv = Path(args.csv_path)

    if args.output_dir:
        output_dir = Path(args.output_dir)

    filters: list[list[str]] = args.filter or []
    extra_fields: list[str] = args.extra_field or []
    header_print: list[str] = []

    if extra_fields:
        header_print.append("id")
        for field in extra_fields:
            header_print.append(field)

    if not args.csv_path:
        sys.exit("Missing path to backup csv-file")

    if not args.filter:
        sys.exit("At least one filter must be defined.")

    if input_csv.suffix != ".csv":
        sys.exit(f"Path to backup file does not point to a csv-file: {input_csv}")

    if not input_csv.exists():
        sys.exit(f"Backup csv-file does not exists: {input_csv}")

    if not args.output_dir and not args.print:
        sys.exit("You must use either --output-dir or --print")

    if args.output_dir and not output_dir.exists():
        sys.exit(f"Output directory must exist: {output_dir}")

    with open(input_csv, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        print("Started filtering backup file...")
        for row in csvReader:
            _dict: dict = json.loads(row["oasDictText"])

            operators_results: list[bool] = []

            for i in range(len(filters)):  # i is filter No.
                fieldname: str = args.filter[i][0]
                # fieldname = FIELDS_TRANSLATED[fieldname]

                fieldname_lower: str = fieldname.lower()

                for key in FIELDS_TRANSLATED:
                    if key.lower() == fieldname_lower:
                        fieldname = FIELDS_TRANSLATED[key]
                        break

                operator_key: str = args.filter[i][1]
                fieldvalue: str = args.filter[i][2]
                fieldvalue = fieldvalue.lower()

                if (fieldvalue == "null" and operator_key == "equalTo" and not _dict.get(fieldname)) or (
                    fieldvalue == "null" and operator_key == "notEqualTo" and _dict.get(fieldname)
                ):
                    op_results = True
                elif not _dict.get(fieldname):
                    op_results = False
                else:
                    operator = FIELDS[fieldname][operator_key]
                    op_results = operator(_dict[fieldname], fieldvalue)

                operators_results.append(op_results)

            total_op_result = any(operators_results) if args.or_ else all(operators_results)

            if not total_op_result:
                continue

            id_ = row["id"]
            header: list[str] = ["id"]
            to_add: list[Any] = [id_]

            for field in extra_fields:
                # header.append(field[0])
                header.append(field)

                fieldname = FIELDS_TRANSLATED[field]
                fieldvalue_ = _dict.get(fieldname, "")

                to_add.append(json.dumps(fieldvalue_, ensure_ascii=False))

            output.append(to_add)

    print(f"Found {len(output)} results matching the applied filter(s)")

    if args.print:
        print(header_print)
        for row in output:  # type: ignore
            print(str(row))
    else:
        max_file_size = 5000
        count = 0
        for i in range(0, len(output), max_file_size):
            if args.filestem:
                custom_filestem: str = args.filestem
                csv_out_path = Path(output_dir, Path(custom_filestem + f"_{count}.csv"))
            else:
                csv_out_path = Path(output_dir, Path(f"backup-search-results_{count}.csv"))

            with open(csv_out_path, "w", newline="", encoding="utf-8") as f:
                write = csv.writer(f)
                write.writerow(header)
                write.writerows(output[i : i + max_file_size])  # writes data in blobs of max_file_size
                count += 1
        print(f"Finished writing csv-files to output-dir: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
