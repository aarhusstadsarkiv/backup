import pytest
import sys
import os
from backupsearch import backup


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

CSV_PATH = "./tests/test_data/testdata.csv"
TEST_PATH_OUTPUT = "./tests/test_data/"


def test_default(capsys):
    with pytest.raises(SystemExit) as e:
        backup.main([])
    print(e.value.code)
    assert e.value.code != 0
    assert capsys.readouterr().out.__contains__("search")


def test_help(capsys):
    with pytest.raises(SystemExit) as e:
        backup.main(["-h"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("backup")


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        backup.main(["--version"])
    assert e.value.code == 0
    assert str(capsys.readouterr().out.split(".")[1]).isnumeric()


# def test_list(capsys):
#     with pytest.raises(SystemExit) as e:
#         main.main(["list"])
#     assert e.value.code == 0
#     assert capsys.readouterr().out.__contains__("Persondata")


def test_list_help(capsys):
    with pytest.raises(SystemExit) as e:
        backup.main(["list", "-h"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("fields")


def test_search_help(capsys):
    with pytest.raises(SystemExit) as e:
        backup.main(["search", "-h"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("filestem")


# ---------OR-----------------------------------------------------------------------------------------


def test_OPERATORS_DICT_FIELD_or(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesdata",
        "regex",
        "Aarhus Stiftstidende$",  # 8 results
        "--filter",
        "Skematype",
        "contains",
        "Analog",  # 13 results
        "--or_",  # or
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("14") and err == ""


# --------OPERATORS_ID_FIELD-------------------------------------------------------------------------
def test_OPERATORS_ID_FIELD_regex(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Samling",
        "regex",
        "\\(1700-1970\\)",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


def test_OPERATORS_ID_FIELD_contains(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Samling",
        "contains",
        "Sejrs Sedler",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("9") and err == ""


def test_OPERATORS_ID_FIELD_notEqualTo(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Samling",
        "notEqualTo",
        "2",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("8") and err == ""


def test_OPERATORS_ID_FIELD_equalTo(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Samling",
        "equalTo",
        "2",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("4") and err == ""


# --------OPERATORS_ID_FIELD_LIST--------------------------------------------------------------------------
def test_OPERATORS_ID_FIELD_LIST_regex(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Kurator",
        "regex",
        "1",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("14") and err == ""


def test_OPERATORS_ID_FIELD_LIST_equalTo(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Kurator",
        "equalTo",
        "3",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_ID_FIELD_LIST_contains_two_filters(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Kurator",
        "contains",
        "Test",
        "--filter",
        "Kurator",
        "equalTo",
        "1",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_ID_FIELD_LIST_greaterThan(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Kurator",
        "greaterThan",
        "1",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_ID_FIELD_LIST_lessThan(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Kurator",
        "lessThan",
        "2",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("14") and err == ""


# --------OPERATORS_DATE_FIELD---------------------------------------------------------------------------
def test_OPERATORS_DATE_FIELD_regex(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Startdato",
        "regex",
        "1877",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_DATE_FIELD_equalTo(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Startdato",
        "equalTo",
        "1877-04-17",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_DATE_FIELD_greaterThan(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Startdato",
        "greaterThan",
        "1877-04-17",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("11") and err == ""


def test_OPERATORS_DATE_FIELD_lessThan(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Startdato",
        "lessThan",
        "1877-04-17",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


# --------OPERATORS_STRING_FIELD--------------------------------------------------------------------------
def test_OPERATORS_STRING_FIELD_regex(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesnoter",
        "regex",
        "frivillige",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


def test_OPERATORS_STRING_FIELD_contains(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesnoter",
        "contains",
        "Tekstindholdet",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


def test_OPERATORS_STRING_FIELD_equalTo(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesnoter",
        "equalTo",
        (
            "Tekstindholdet af dette kartotekskort er afskrevet af frivillige"
            ", men selve kortet er ikke digitaliseret."
        ),
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


# --------OPERATORS_DICT_FIELD--------------------------------------------------------------------------
def test_OPERATORS_DICT_FIELD_regex(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesdata",
        "regex",
        "Aarhus Stiftstidende$",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("8") and err == ""


def test_OPERATORS_DICT_FIELD_contains(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesdata",
        "contains",
        "Typer:Farve",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_DICT_FIELD_hasKey(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesdata",
        "hasKey",
        "Typer",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_DICT_FIELD_contains_two_filters_w_datefield(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Beskrivelsesdata",
        "contains",
        "Typer:Farve",
        "--filter",
        "Startdato",
        "lessThan",
        "2000",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


# --------OPERATORS_STRING_FIELD_LIST--------------------------------------------------------------------------
def test_OPERATORS_STRING_FIELD_LIST_regex(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Stregkode",
        "regex",
        "8025866751",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_STRING_FIELD_LIST_equalTo(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Stregkode",
        "equalTo",
        "8025866751",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_STRING_FIELD_LIST_contains_on_two_barcodes(capfd):
    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        "search",
        csv_path,
        "--output-dir",
        test_path_output,
        "--filter",
        "Stregkode",
        "contains",
        "80258",
        "--filter",
        "Stregkode",
        "contains",
        "11",
    ]

    backup.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""
