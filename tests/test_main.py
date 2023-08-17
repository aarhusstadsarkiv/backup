import pytest
import sys
import os
from backupsearch import main

# from importlib import metadata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

CSV_PATH = "./tests/test_data/testdata.csv"
TEST_PATH_OUTPUT = "./tests/test_data/"


def test_default(capsys):
    with pytest.raises(SystemExit) as e:
        main.main([])
    assert e.value.code == 0
    assert "backupsearch" in str(capsys.readouterr().out).lower()


def test_help(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["-h"])
    assert e.value.code == 0
    assert "backupsearch" in str(capsys.readouterr().out).lower()


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["--version"])
    assert e.value.code == 0
    assert str(capsys.readouterr().out.split(".")[1]).isnumeric()


def test_list(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["list"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("Persondata")


def test_list_help(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["list", "-h"])
    assert e.value.code == 0
    assert "fields" in capsys.readouterr().out


def test_search_help(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["search", "-h"])
    assert e.value.code == 0
    assert "apply" in str(capsys.readouterr().out).lower()


# def test_OPERATORS_DICT_FIELD_or(capfd):
#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesdata",
#         "regex",
#         "Aarhus Stiftstidende$",  # 8 results
#         "--filter",
#         "Skematype",
#         "contains",
#         "Analog",  # 13 results
#         "--or_",  # or
#     ]
#     args = ["search", "-h"]
#     main(args)
#     out, err = capfd.readouterr()
#     assert out.__contains__("13") and err == ""


# # --------OPERATORS_ID_FIELD-----------------------------------------------------------
# def test_OPERATORS_ID_FIELD_regex(capfd):

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Samling",
#         "regex",
#         "\\(1700-1970\\)",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("10") and err == ""


# def test_OPERATORS_ID_FIELD_contains(capfd):
#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Samling",
#         "contains",
#         "Sejrs Sedler",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("9") and err == ""


# def test_OPERATORS_ID_FIELD_notEqualTo(capfd):
#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Samling",
#         "notEqualTo",
#         "2",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("8") and err == ""


# def test_OPERATORS_ID_FIELD_equalTo(capfd):
#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Samling",
#         "equalTo",
#         "2",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("4") and err == ""


# # --------OPERATORS_ID_FIELD_LIST--------------------------------------------------------
# def test_OPERATORS_ID_FIELD_LIST_regex(capfd):
#     args = ["search", CSV_PATH, TEST_PATH_OUTPUT, "--filter", "Kurator", "regex", "1"]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("13") and err == ""


# def test_OPERATORS_ID_FIELD_LIST_equalTo(capfd):
#     args = ["search", CSV_PATH, TEST_PATH_OUTPUT, "--filter", "Kurator", "equalTo", "3"]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("1") and err == ""


# def test_OPERATORS_ID_FIELD_LIST_contains_two_filters(capfd):
#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Kurator",
#         "contains",
#         "Test",
#         "--filter",
#         "Kurator",
#         "equalTo",
#         "1",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("1") and err == ""


# def test_OPERATORS_ID_FIELD_LIST_greaterThan(capfd):
#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Kurator",
#         "greaterThan",
#         "1",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("2") and err == ""


# def test_OPERATORS_ID_FIELD_LIST_lessThan(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Kurator",
#         "lessThan",
#         "2",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("13") and err == ""


# # --------OPERATORS_DATE_FIELD---------------------------------------------------------------------------
# def test_OPERATORS_DATE_FIELD_regex(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Startdato",
#         "regex",
#         "1877",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("1") and err == ""


# def test_OPERATORS_DATE_FIELD_equalTo(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Startdato",
#         "equalTo",
#         "1877-04-17",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("1") and err == ""


# def test_OPERATORS_DATE_FIELD_greaterThan(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Startdato",
#         "greaterThan",
#         "1877-04-17",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("10") and err == ""


# def test_OPERATORS_DATE_FIELD_lessThan(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Startdato",
#         "lessThan",
#         "1877-04-17",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("2") and err == ""


# # --------OPERATORS_STRING_FIELD--------------------------------------------------------------------------
# def test_OPERATORS_STRING_FIELD_regex(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesnoter",
#         "regex",
#         "frivillige",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("10") and err == ""


# def test_OPERATORS_STRING_FIELD_contains(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesnoter",
#         "contains",
#         "Tekstindholdet",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("10") and err == ""


# def test_OPERATORS_STRING_FIELD_equalTo(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesnoter",
#         "equalTo",
#         (
#             "Tekstindholdet af dette kartotekskort er afskrevet af frivillige"
#             ", men selve kortet er ikke digitaliseret."
#         ),
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("10") and err == ""


# # --------OPERATORS_DICT_FIELD--------------------------------------------------------------------------
# def test_OPERATORS_DICT_FIELD_regex(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesdata",
#         "regex",
#         "Aarhus Stiftstidende$",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("8") and err == ""


# def test_OPERATORS_DICT_FIELD_contains(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesdata",
#         "contains",
#         "Typer:Farve",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("2") and err == ""


# def test_OPERATORS_DICT_FIELD_hasKey(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesdata",
#         "hasKey",
#         "Typer",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("2") and err == ""


# def test_OPERATORS_DICT_FIELD_contains_two_filters_w_datefield(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Beskrivelsesdata",
#         "contains",
#         "Typer:Farve",
#         "--filter",
#         "Startdato",
#         "lessThan",
#         "2000",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("1") and err == ""


# # --------OPERATORS_STRING_FIELD_LIST--------------------------------------------------------------------------
# def test_OPERATORS_STRING_FIELD_LIST_regex(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Stregkode",
#         "regex",
#         "8025866751",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("2") and err == ""


# def test_OPERATORS_STRING_FIELD_LIST_equalTo(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Stregkode",
#         "equalTo",
#         "8025866751",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("2") and err == ""


# def test_OPERATORS_STRING_FIELD_LIST_contains_on_two_barcodes(capfd):
#     CSV_PATH = "./tests/test_data/testdata.csv"

#     TEST_PATH_OUTPUT = "./tests/test_data/"

#     args = [
#         "search",
#         CSV_PATH,
#         TEST_PATH_OUTPUT,
#         "--filter",
#         "Stregkode",
#         "contains",
#         "80258",
#         "--filter",
#         "Stregkode",
#         "contains",
#         "11",
#     ]

#     main(args)

#     out, err = capfd.readouterr()

#     assert out.__contains__("1") and err == ""
