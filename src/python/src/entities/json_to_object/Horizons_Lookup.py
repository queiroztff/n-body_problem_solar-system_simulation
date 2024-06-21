from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List, Optional, Union, Type
from entities.interfaces import ISpkIdSearch    


@dataclass(kw_only=True)
class Signature:
    source: str
    version: str


@dataclass(kw_only=True)
class Result:
    alias: List[str]
    name: str
    spkid: str
    pdes: str

@dataclass(kw_only=True)
class Join:
    count: Union[str, int]
    result: Optional[List[Result]] = field(default=None)
    signature: Signature

    def __post_init__(self) -> None:
        self.result = [Result(**item) for item in self.result]
        self.signature = Signature(**self.signature)

class ObjectLookup(Join):
    '''
    Esta classe converte a resposta da API Horizons_Lookup em objeto
    '''
    def __init__(self, inject: Type[ISpkIdSearch]) -> None:
        self.__inject = inject
        self.__log: Logger = getLogger(__name__)

        try:
            Join.__init__(self, **self.__inject.get_data())
        except:
            message = '''
            Erro de injeção de dependencia
            '''
            self.__log.error(message)
            raise Exception(message)
        
        self.__log.debug('Started')
    

