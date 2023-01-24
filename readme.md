# Filters the backup database
This filters the csv formatted backup database:
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