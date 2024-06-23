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
class ConversionFactor:
    distance: float
    mass: float
    time: float

@dataclass(kw_only=True)
class Method:
    name: str
    eps: float
    tol: float
    G: float
    step: Step
    conversion_factor: ConversionFactor

    def __post_init__(self) -> None:
        self.step = Step(**self.step)
        self.conversion_factor = ConversionFactor(**self.conversion_factor)

@dataclass(kw_only=True)
class Domain:
    t0: float
    tf: float

@dataclass(kw_only=True)
class InitialCondition:
    body: str
    mass: float
    s0: List[float]
    v0: List[float]

@dataclass(kw_only=True)
class Itens:
    name: str
    method: Method
    domain: Domain
    initial_condition: List[InitialCondition] = field(default_factory = List)

    def __post_init__(self) -> None:
        self.method = Method(**self.method)
        self.domain = Domain(**self.domain)
        self.initial_condition = [InitialCondition(**item) for item in self.initial_condition]

@dataclass(kw_only=True)
class Join:
    simulation: List[Itens] = field(default_factory=List)
    
    def __post_init__(self) -> None:
        self.simulation = [Itens(**item) for item in self.simulation]
    
class FortranSimulationManualInsertInitialCondition(Join):
    """
    Dado um caminho 'path' que contenha o aquivo json com o mesmo esquema do json 
    do arquivo fortran_simulation_manual_insert_initial_condition.json, esta classe 
    transforma o mesmo em objeto

    Attributes
    ----------
        _path: str 
            Caminho que contem o arquivo com o mesmo esquema NASA_simulation_config.json
            (default = '../../../../../data/input/python/fortran_simulation_manual_insert_initial_condition.json'')
    """

    def __init__(self, 
                 _path:str = '../../../../../data/input/python/fortran_simulation_manual_insert_initial_condition.json') -> None:
        
        self.__path = _path
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

