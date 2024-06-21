import json
import pytest
from entities.json_to_object.report import Report

JSON_FILE = '''
{
    "runtime" :        0.616,
    "simulation" : {
        "name" : "figure_8",
            "method" : {
                "name" : "rkdp",
                "eps" : 1.000E-3,
                "tol" : 1.000E-16,
                "step" : {
                    "hmin" : 1.000E-5,
                    "hmax" : 1.000E-3
                }
            },
        "domain" : {
            "t0" :   0.00000000,
            "tf" :   6.32444900
            },
        "dms" : 2,
        "nbody" : 3,
        "state" : [
            {
                "body" : "pm_01",
                "mass" : 1.000E+0,
                "local_storage" : "pm_01.sob"
            },
            {
                "body" : "pm_02",
                "mass" : 1.000E+0,
                "local_storage" : "pm_02.sob"
            },
            {
                "body" : "pm_03",
                "mass" : 1.000E+0,
                "local_storage" : "pm_03.sob"
            }
        ]
    }
}
'''

@pytest.fixture
def json_data():
    try:
        data:dict = json.loads(JSON_FILE)
    except:
        message = '''
        Não foi possível realizar o decode do arquivo json
        '''
        raise FileNotFoundError(message)
    
    return data

@pytest.fixture(scope="session")
def path_json(tmp_path_factory):
    p = tmp_path_factory.mktemp("data")/"report.json"
    p.write_text(JSON_FILE)
    return p

@pytest.fixture()
def Obj(path_json):
    obj = Report(path=path_json)
    return obj


def test_Config_isinstace(Obj):
    expected = True
    result = isinstance(Obj, Report)

    assert result == expected

def test_Config_attributes(Obj, json_data):
    expected = set(Obj.__dict__.keys())
    result = set(json_data.keys())

    assert result.issubset(expected)