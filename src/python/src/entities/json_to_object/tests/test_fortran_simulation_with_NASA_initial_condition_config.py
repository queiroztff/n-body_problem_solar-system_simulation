import json
import pytest
from entities.json_to_object.fortran_simulation_with_NASA_initial_condition_config import FortranSimulationWithNasaInitialConditionConfig

JSON_FILE = '''
{
    "simulation":[
        {
            "name":"Solar_System",

            "body":{
                "pln":["Sun", "Mercury", "Venus", 
                "Earth", "Mars", "Jupiter", 
                "Saturn", "Uranus", "Neptune"],
        
                "sat":["Moon"]
            },

            "calendar":{
                "model":"cd",
                "start_time":"2000-01-01 00:00",
                "stop_time": "2001-01-01 00:00"
            },

            "center":"500@0",
            "step_size":"3d",
            "out_units":"KM-D",
        
            "relative_time":true,

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

            }
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
    obj = FortranSimulationWithNasaInitialConditionConfig(path=path_json)
    return obj


def test_Config_isinstace(Obj):
    expected = True
    result = isinstance(Obj, FortranSimulationWithNasaInitialConditionConfig)

    assert result == expected

def test_Config_attributes(Obj, json_data):
    expected = set(Obj.__dict__.keys())
    result = set(json_data.keys())

    assert result.issubset(expected)
