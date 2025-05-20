# Backup
Commandline tool used to query the backup-files generated from our Google-based metadata-store ("oas"-backups). These backup files are located here `AFD-Aarhus Stadsarkiv/_DIGITALT_ARKIV/ark_meta_backup`

In time, a `fetch` subcommand that generated a new backup-file, will be implemented. For now only the `search` subcommand is in use


Apply any number of --filter.
## --filter [field] [operator] [value]:
ex. --filter Samling contains Salling. Value is the variable user input.

## --list:
Lists the available fields and their operators.

## --filename [filename]
Specify the custom filename for the output file(s).

## --or_
Default concatination mode of filters are "and", this option switches it to "or".

## --version
Print the actual version of the cli.


```
Filters the csv formatted backup database:
Apply any number of --filter
Use --list for allowed fields and operators.

ex.1 field is "id-field"
--filter Samling equalTo 1
or
--filter Samling contains Salling

ex.2 if the field is a dictionary, and target search is in a key's value:
--filter "Administrative data" contains "Bestillingsinformation:negativsamlingen 1970"

ex.3 if the field is a dictionary, and filter after target has a certain key:
--filter "Administrative data" hasKey Bestillingsinformation

ex.4 the field is a dictionary and the key is known and filter on the value:
--filter "Beskrivelsesdata" contains Typer:Farve

positional arguments:
  input_csv_file_path   Path to the backup database csv file.
  output_dir            Path to the output/result directory for csv file(s).

options:
  -h, --help            show this help message and exit
  --filter FILTER FILTER FILTER
                        Adds a filter to limit the results
  --version             States the current version of this CLI.
  --list                Lists the allowed fields and their operators.
  --filename FILENAME   specify the output filename(s).
  --or_                 the filters are or'ed together.
```

# Operators
```
ex. ""1;Sejrs Sedler (1700-1970)""
OPERATORS_ID_FIELD: dict = {
    "equalTo": equal to the integer of the "id field"
    "notEqualTo": not equal to the integer of the "id field"
    "greaterThan": larger than the integer of the "id field"
    "lessThan": smaller than the integer of the "id field"
    "contains": if integer or string is contained in "id field"
    "regex": pattern match both integer and string in "id field"
}

ex. [""1;Aarhus Stadsarkiv""]
OPERATORS_ID_FIELD_LIST: dict = {
    "equalTo": equal to string or number
    "notEqualTo": not equal to string or number
    "greaterThan": larger than integer in "id field list"
    "lessThan": smaller than integer in "id field list"
    "contains": integer or string contained in "id field list"
    "regex": pattern match "id field list"
}
ex. ""1903-02-11""
OPERATORS_DATE_FIELD: dict = {
    "equalTo": date exactly equal to
    "notEqualTo": date different from
    "greaterThan": date later than
    "lessThan": date earlier than
    "regex": pattern match date
}
ex. ""Tekstindholdet af dette kartotekskort er afskrevet af frivillige, men selve kortet er ikke digitaliseret.""
OPERATORS_STRING_FIELD: dict = {
    "equalTo": exact equal to
    "notEqualTo": different from
    "contains": substring of string exists
    "notContains": substring not in string
    "regex": pattern matches the string
}
ex. {""source"": ""Aarhus Stiftstidende""}
OPERATORS_DICT_FIELD: dict = {
    "notHasKey": if key not exists
    "exists": check if the field exists
    "notExists": check if the field not exists
    "hasKey": if key exists
    "contains": if value contains, like: key:value
    "regex": searches for pattern matching in values
}
ex. [""8012994031""]
OPERATORS_STRING_FIELD_LIST: dict = {
    "contains": contains in any of the strings in the list
    "equalTo": must match any string in the list
    "notEqualTo": must not match any string in the list
    "regex": like contains, searches for pattern matching in any string in the list
}
```

## Releases
Pyinstaller virker (indtil videre!) med følgende kald:

`poetry run pyinstaller --onefile --name backup .\backupsearch\backup.py`
