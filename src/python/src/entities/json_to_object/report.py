import json
import os
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List

@dataclass(kw_only=True)
class Step:
    hmin: float
    hmax: float

@dataclass(kw_only=True)
class Method:
    name: str
    eps: float
    tol: float
    step: Step

    def __post_init__(self) -> None:
        self.step = Step(**self.step)

@dataclass(kw_only=True)
class Domain:
    t0: float
    tf: float

@dataclass(kw_only=True)
class State:
    body: str
    mass: float
    local_storage: str

@dataclass(kw_only=True)
class Simulation:
    name: str
    dms: int
    nbody: int
    method: Method
    domain: Domain
    state: List[State] = field(default_factory=List)

    def __post_init__(self) -> None:
        self.method = Method(**self.method)
        self.domain = Domain(**self.domain)
        self.state = [State(**item) for item in self.state]

@dataclass(kw_only=True)
class Join:
    runtime: float
    simulation: Simulation

    def __post_init__(self) -> None:
        self.simulation = Simulation(**self.simulation)

class Report(Join):
    """
    Dado um caminho 'path' que contenha o aquivo report.json, esta classe 
    transforma o mesmo em objeto

    Attributes
    ----------
        path: str 
            Caminho que contem o arquivo report.json
    """

    def __init__(self, path:str) -> None:
        self.__path = path
        self.__log: Logger = getLogger(__name__)

        absollute_path = os.path.dirname(__file__)
        relative_path = self.__path
        json_file = os.path.abspath(os.path.join(absollute_path, relative_path))

        try: 
            with open(json_file, 'r') as file:
                data:dict = json.load(file)
        except:
            message = f'''
            Arquivo contido no caminho {json_file} não foi encontrado
            '''
            self.__log.error(message)
            raise FileNotFoundError(message)
        
        Join.__init__(self, **data)

        self.__log.debug('Started')

    

