import json
from pathlib import Path
import csv
import argparse
from settings import FIELDS, FIELDS_TRANSLATED



def get_version() -> str:
    version = "Ukendt version"
    with open(Path(__file__).absolute().parent.parent / "pyproject.toml") as i:
        for line in i.readlines():
            if line.startswith("version"):
                version = line[line.index('"') + 1 : -2]
    return version


def main(args=None):

    output: list[tuple[int, int, int]] = []

    parser = argparse.ArgumentParser(
        description=(
            "Filters the csv formatted backup database:\n"
            "Apply any number of --filter \n"
            "Use --list for allowed fields and operators.\n"
            "Use --filename to specify a custom filename for the output file(s).\n"
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
            '--filter Samling equalTo null or --filter Samling notEqualTo null\n\n'
            'All user inputs are case-insensitive.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "csv_path",
        metavar="input_csv_file_path",
        type=str,
        nargs="?",
        help="Path to the backup database csv file.",
    )
    parser.add_argument(
        "output_path",
        metavar="output_dir",
        type=str,
        nargs="?",
        help="Path to the output/result directory for csv file(s).",
    )
    parser.add_argument(
        "--filter",
        type=str,
        nargs=3,
        action="append",
        help=("Adds a filter to limit the results"),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=get_version(),
        help="States the current version of this CLI.",
    )
    parser.add_argument(
        "--list", action="store_true", help="Lists the allowed fields and their operators."
    )

    parser.add_argument(
        "--filename", type=str, nargs=1, action="append", help="specify the output filename(s)."
    )#remove action?
    parser.add_argument("--or_", action="store_true", help="the filters are or'ed together.")

    parser.add_argument(
        "--field", type=str, nargs=1, action="append", help="if specified, adds extra data field in results file(s)."
    )


    args = parser.parse_args(args)

    def list_fields() -> None:
        print("Printing fields and operators...")
        for key in FIELDS_TRANSLATED.keys():
            print(key.ljust(25), end="")
            print(", ".join(FIELDS[FIELDS_TRANSLATED[key]].keys()))

    if args.list:
        list_fields()
        exit(0)

    input_csv = Path(args.csv_path)
    output_dir = Path(args.output_path)

    print("Starting filtering process...")

    filters: list[list[str]] = args.filter
    extra_fields: list[list[str]] = args.field

    csv_path = input_csv
    # -----input validation-------------------------------------------------
    if not csv_path.suffix == ".csv":
        exit("input file is not a csv-file...")

    if not csv_path.exists():
        exit("input csv-file does not exists...")

    if not output_dir.exists():
        exit("output directory does not exists. Please create one...")
    # ----------------------------------------------------------------------

    with open(csv_path, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            _dict: dict = json.loads(row["oasDictText"])

            

            operators_results: list[bool] = []

            for i in range(len(filters)):  # i is filter No.

                fieldname: str = args.filter[i][0]
                fieldname = FIELDS_TRANSLATED[fieldname]

                operator_key: str = args.filter[i][1]
                fieldvalue: str = args.filter[i][2]
                fieldvalue = fieldvalue.lower()

                if (
                    fieldvalue == "null"
                    and operator_key == "equalTo"
                    and not _dict.get(fieldname)
                ):
                    op_results = True
                elif (
                    fieldvalue == "null"
                    and operator_key == "notEqualTo"
                    and _dict.get(fieldname)
                ):
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
                continue  # if false
            
            id = row["id"]
            header: list[str] = ["id"]
            to_add: list[str] = [id]

            if extra_fields:
                for field in extra_fields:
                    
                    header.append(field[0])

                    fieldname = FIELDS_TRANSLATED[field[0]]
                    fieldvalue_ = _dict.get(fieldname, "")
                    
                    to_add.append(json.dumps(fieldvalue_))

            output.append(to_add)   # if true            

    max_file_size = 5000
    count = 0
    for i in range(0, len(output), max_file_size):

        if args.filename:
            custom_filename: str = args.filename[0][0]
            csv_out_path = Path(output_dir, Path(custom_filename + "_" + str(count) + ".csv"))
        else:
            csv_out_path = Path(output_dir, Path("filter_results_" + str(count) + ".csv"))

        with open(csv_out_path, "w", newline="", encoding='utf-8') as f:
            write = csv.writer(f)            
            write.writerow(header)
            write.writerows(output[i : i + max_file_size])  # writes data in blobs of max_file_size

        count += 1

    print("Done: Found " + str(len(output)) + " results matching the applied filter(s)")


if __name__ == "__main__":
    main()
