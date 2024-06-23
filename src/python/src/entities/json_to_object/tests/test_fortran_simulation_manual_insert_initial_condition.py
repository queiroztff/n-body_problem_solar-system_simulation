import json
import pytest
from entities.json_to_object.fortran_simulation_manual_insert_initial_condition import FortranSimulationManualInsertInitialCondition

JSON_FILE = '''
{
    "simulation":[
        {
            "name" : "figure_8",
            "method" : {
                "name" : "rkdp",
                "eps" : 1.000E-3,
                "tol" : 1.000E-16,
                "step" : {
                    "hmin" : 1.000E-5,
                    "hmax" : 1.000E-3
                },
                "G" : 1,
                "conversion_factor" : {
                    "distance" : 1,
                    "mass" : 1,
                    "time" : 1
                }
            },
            "domain" : {
                "t0" : 0.00000000,
                "tf" : 6.32444900
            },
            "initial_condition" : [
                {
                    "body" : "pm_01",
                    "mass" : 1.0 ,
                    "s0" : [ -1.0, 0.0],
                    "v0" : [0.347111, 0.532728]
                },
                {
                    "body" : "pm_02",
                    "mass" : 1.0,
                    "s0" : [1.0, 0.0],
                    "v0" : [0.347111, 0.532728]
                },
                {
                    "body" : "pm_03",
                    "mass" : 1.0,
                    "s0" : [0.0, 0.0],
                    "v0" : [-0.694222, -1.065456]
                }
            ]    
        }
    ]
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
    p = tmp_path_factory.mktemp("data")/"data.json"
    p.write_text(JSON_FILE)
    return p

@pytest.fixture()
def Obj(path_json):
    obj = FortranSimulationManualInsertInitialCondition(_path=path_json)
    return obj


def test_Config_isinstace(Obj):
    expected = True
    result = isinstance(Obj, FortranSimulationManualInsertInitialCondition)

    assert result == expected

def test_Config_attributes(Obj, json_data):
    expected = set(Obj.__dict__.keys())
    result = set(json_data.keys())

    assert result.issubset(expected)
