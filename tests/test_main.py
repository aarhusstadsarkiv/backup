import pytest
import sys
import os
from backupsearch import main


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

CSV_PATH = "./tests/test_data/testdata.csv"
TEST_PATH_OUTPUT = "./tests/test_data/"


def test_default(capsys):
    with pytest.raises(SystemExit) as e:
        main.main([])
    print(e.value.code)
    assert e.value.code != 0
    assert capsys.readouterr().out.__contains__("search")


def test_help(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["-h"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("backup")


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["--version"])
    assert e.value.code == 0
    assert str(capsys.readouterr().out.split(".")[1]).isnumeric()


# def test_list(capsys):
#     with pytest.raises(SystemExit) as e:
#         main.main(["list"])
#     assert e.value.code == 0
#     assert capsys.readouterr().out.__contains__("Persondata")


def test_list_help(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["list", "-h"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("fields")


def test_search_help(capsys):
    with pytest.raises(SystemExit) as e:
        main.main(["search", "-h"])
    assert e.value.code == 0
    assert capsys.readouterr().out.__contains__("filestem")
