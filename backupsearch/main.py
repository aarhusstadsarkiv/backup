import json
import sys
from pathlib import Path
import csv
import argparse
from typing import List, Optional, Sequence, Any
from importlib import metadata
from backupsearch.settings import FIELDS, FIELDS_TRANSLATED


def main(argv: Optional[Sequence[str]] = None) -> int:
    output: List[List[Any]] = []

    parser = argparse.ArgumentParser(
        description=(
            "Backupsearch lets you generate filtered lists of record_ids from a backupfile.\n\n"
            "You can print the output in the terminal or save it to one or more csv-files, that "
            "can be directly imported to SAM to create new update jobs.\n\n"
            "Use 'backupsearch list' to view information about all the possible search filters.\n"
            "Use 'backupsearch search' to search a given backup file."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=metadata.version("backupsearch"))

    # subparsers
    subs = parser.add_subparsers(
        title="commands",
        dest="command",
        # description="description str, set to replace the {} list of commands",
        # metavar="",
    )

    # list subcommand
    subs.add_parser(
        "list",
        help="List all valid search fields and their associated operators",
        description=(
            "Lists all the metadata fields that are available for filtering, along with the "
            "operators that each field allows.\n\n"
            "Use one or more of these metadata fields to filter the output from backupsearch."
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
    search.add_argument(
        "output_path",
        metavar="output_dir",
        type=str,
        help="Path to the output/result directory for csv file(s).",
    )
    search.add_argument(
        "--filter",
        type=str,
        nargs=3,
        action="append",
        help="Add one or more filters to limit the results",
    )
    search.add_argument(
        "--print",
        action="store_true",
        help="If the results are few, prints the results instead of generating csv file(s).",
    )
    search.add_argument(
        "--filestem", type=str, help="Specify the output filestem(s)"
    )  # remove action?
    search.add_argument("--or_", action="store_true", help="Use OR between filters")
    search.add_argument(
        "--field",
        type=str,
        action="append",
        help="Include one or more columns besides the default 'id'-column",
    )
    # print("argparse done")
    # if not argv:
    #     argv = Sequence(["--help"])
    args = parser.parse_args(argv)
    # print("vars(args):")
    # print(vars(args))

    if args.command == "list":
        for key in FIELDS_TRANSLATED.keys():
            print(key.ljust(25), end="")
            print(", ".join(FIELDS[FIELDS_TRANSLATED[key]].keys()))
        return 0

    elif args.command != "search":
        raise NotImplementedError(f"Command {args.command} does not exist.")

    if args.csv_path:
        input_csv = Path(args.csv_path)
    if args.output_path:
        output_dir = Path(args.output_path)

    filters: List[List[str]] = args.filter or []
    extra_fields: List[List[str]] = args.field or []
    header_print: List[str] = []

    if args.field:
        header_print.append("id")
        for field in args.field:
            # header_print.append(field[0])
            header_print.append(field)
    if not args.csv_path:
        sys.exit("No input csv database backup given...")

    if not args.filter:
        sys.exit("No filters were given...")

    if not input_csv.suffix == ".csv":
        sys.exit("input file is not a csv-file...")

    if not input_csv.exists():
        sys.exit("input csv-file does not exists...")

    if not args.output_path and not args.print:
        sys.exit("No output path or --print...")

    if args.output_path and not output_dir.exists():
        sys.exit("output directory does not exists. Please create one...")

    print("Starting filtering process...")
    with open(input_csv, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            _dict: dict = json.loads(row["oasDictText"])

            operators_results: List[bool] = []

            for i in range(len(filters)):  # i is filter No.
                fieldname: str = args.filter[i][0]
                fieldname = FIELDS_TRANSLATED[fieldname]

                operator_key: str = args.filter[i][1]
                fieldvalue: str = args.filter[i][2]
                fieldvalue = fieldvalue.lower()

                if fieldvalue == "null" and operator_key == "equalTo" and not _dict.get(fieldname):
                    op_results = True
                elif fieldvalue == "null" and operator_key == "notEqualTo" and _dict.get(fieldname):
                    op_results = True
                elif not _dict.get(fieldname):
                    op_results = False
                else:
                    operator = FIELDS[fieldname][operator_key]
                    op_results = operator(_dict[fieldname], fieldvalue)

                operators_results.append(op_results)

            if args.or_:
                total_op_result = any(operators_results)
            else:
                total_op_result = all(operators_results)

            if not total_op_result:
                continue

            id_ = row["id"]
            header: List[str] = ["id"]
            to_add: List[Any] = [id_]

            for field in extra_fields:
                # header.append(field[0])
                header.append(field)

                fieldname = FIELDS_TRANSLATED[field]
                fieldvalue_ = _dict.get(fieldname, "")

                to_add.append(json.dumps(fieldvalue_, ensure_ascii=False))

            output.append(to_add)

    print(f"Done: Found {len(output)} results matching the applied filter(s)")

    if args.print:
        print(header_print)
        for row in output:
            print(str(row))
    else:
        max_file_size = 5000
        count = 0
        for i in range(0, len(output), max_file_size):
            if args.filestem:
                custom_filestem: str = args.filestem
                csv_out_path = Path(output_dir, Path(custom_filestem + f"_{count}.csv"))
            else:
                csv_out_path = Path(output_dir, Path(f"filter_results_{count}.csv"))

            with open(csv_out_path, "w", newline="", encoding="utf-8") as f:
                write = csv.writer(f)
                write.writerow(header)
                write.writerows(
                    output[i : i + max_file_size]
                )  # writes data in blobs of max_file_size
                count += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    # exit(main())
