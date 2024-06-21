from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import Optional, Type
from entities.interfaces import IJdDateTimeConvert

@dataclass(kw_only=True)
class Signature:
    source: str
    version: str

@dataclass(kw_only=True)
class Join:
    cd: str
    year: str
    month: Optional[int] = field(default=None)
    month_name: str
    doy: int
    dow: int
    dow_name: str
    day_and_time:str
    jd: Optional[str] = field(default=None)
    signature: Signature

    def __post_init__(self) -> None:
        self.signature = Signature(**self.signature)

class ObjectDateTimeConverter(Join):
    '''
    Esta classe converte a resposta da API JD Date/Time Converter em objeto, a qual deve ser injetada nesta
    classe
    '''
    def __init__(self, inject: Type[IJdDateTimeConvert]) -> None:
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
    
