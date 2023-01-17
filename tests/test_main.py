from filter_csv_generic import main


# --------OPERATORS_ID_FIELD-------------------------------------------------------------------------
def test_OPERATORS_ID_FIELD_regex(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "collection",
        "regex",
        "\(1700-1970\)",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""



def test_OPERATORS_ID_FIELD_contains(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "collection",
        "contains",
        "Sejrs Sedler",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("9") and err == ""


def test_OPERATORS_ID_FIELD_notEqualTo(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "collection",
        "notEqualTo",
        "2",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("8") and err == ""


def test_OPERATORS_ID_FIELD_equalTo(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "collection",
        "equalTo",
        "2",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("4") and err == ""


# --------OPERATORS_ID_FIELD_LIST--------------------------------------------------------------------------


def test_OPERATORS_ID_FIELD_LIST_equalTo(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [csv_path, test_path_output, "--filter", "curators", "equalTo", "3"]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_ID_FIELD_LIST_contains_two_filters(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "curators",
        "contains",
        "Test",
        "--filter",
        "curators",
        "equalTo",
        "1",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_ID_FIELD_LIST_greaterThan(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "curators",
        "greaterThan",
        "1",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_ID_FIELD_LIST_lessThan(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "curators",
        "lessThan",
        "2",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("12") and err == ""


# --------OPERATORS_DATE_FIELD---------------------------------------------------------------------------


def test_OPERATORS_DATE_FIELD_equalTo(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "date_from",
        "equalTo",
        "1877-04-17",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


def test_OPERATORS_DATE_FIELD_greaterThan(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "date_from",
        "greaterThan",
        "1877-04-17",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


def test_OPERATORS_DATE_FIELD_lessThan(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "date_from",
        "lessThan",
        "1877-04-17",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


# --------OPERATORS_STRING_FIELD--------------------------------------------------------------------------


def test_OPERATORS_STRING_FIELD_contains(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "desc_notes",
        "contains",
        "Tekstindholdet",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


def test_OPERATORS_STRING_FIELD_equalTo(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "desc_notes",
        "equalTo",
        (
            "Tekstindholdet af dette kartotekskort er afskrevet af frivillige"
            ", men selve kortet er ikke digitaliseret."
        ),
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("10") and err == ""


# --------OPERATORS_DICT_FIELD--------------------------------------------------------------------------


def test_OPERATORS_DICT_FIELD_contains(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "desc_data",
        "contains",
        "Typer:Farve",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_DICT_FIELD_hasKey(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "desc_data",
        "hasKey",
        "Typer",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_DICT_FIELD_contains_two_filters_w_datefield(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "desc_data",
        "contains",
        "Typer:Farve",
        "--filter",
        "date_from",
        "lessThan",
        "2000",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""


# --------OPERATORS_STRING_FIELD_LIST--------------------------------------------------------------------------


def test_OPERATORS_STRING_FIELD_LIST_equalTo(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "barcode",
        "equalTo",
        "8025866751",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("2") and err == ""


def test_OPERATORS_STRING_FIELD_LIST_contains_on_two_barcodes(capfd):

    csv_path = "./tests/test_data/testdata.csv"

    test_path_output = "./tests/test_data/"

    args = [
        csv_path,
        test_path_output,
        "--filter",
        "barcode",
        "contains",
        "80258",
        "--filter",
        "barcode",
        "contains",
        "11",
    ]

    main.main(args)

    out, err = capfd.readouterr()

    assert out.__contains__("1") and err == ""
