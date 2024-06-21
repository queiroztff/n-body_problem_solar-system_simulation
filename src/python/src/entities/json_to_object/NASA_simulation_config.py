import json
import os
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List, Optional, Union

@dataclass(kw_only=True)
class Body:
    ast: Optional[List[str]] = field(default=None)
    com: Optional[List[str]] = field(default=None)
    pln: Optional[List[str]] = field(default=None)
    sat: Optional[List[str]] = field(default=None)

@dataclass(kw_only=True)
class Calendar:
    model: str
    start_time: Union[str, float]
    stop_time: Union[str, float]

@dataclass(kw_only=True)
class Itens:
    name: str
    center: str
    out_units: str
    step_size: str
    relative_time: bool
    body: Body
    calendar: Calendar

    def __post_init__(self) -> None:
        self.body = Body(**self.body)
        self.calendar = Calendar(**self.calendar)
    
@dataclass(kw_only=True)
class Join:
    simulation: List[Itens] = field(default_factory=List)

    def __post_init__(self) -> None:
        self.simulation = [Itens(**item) for item in self.simulation]

class NasaSimulationConfig(Join):
    """
    Dado um caminho 'path' que contenha o aquivo json com o mesmo esquema do json 
    do arquivo NASA_simulation_config.json, esta classe 
    transforma o mesmo em objeto

    Attributes
    ----------
        path: str 
            Caminho que contem o arquivo com o mesmo esquema NASA_simulation_config.json
            (default = '../../../../../data/input/python/NASA_simulation_config.json')
    """

    def __init__(self, 
                 path:str = '../../../../../data/input/python/NASA_simulation_config.json') -> None:
        
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