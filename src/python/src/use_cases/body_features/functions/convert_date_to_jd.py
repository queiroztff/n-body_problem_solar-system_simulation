from logging import Logger, getLogger
from typing import Union
from entities.api_requests import DateTimeConverter
from entities.json_to_object import ObjectDateTimeConverter

def date_to_jd(date: Union[str, float]) -> float:
    """
    Esta função converte uma data de caledário [type str] para o calendário juliano [type float],
    caso a data seja do calendário juliana nada é feito
    Arguments:
    ---------
        date: str|float
    
    Return:
    -------
        float
        retorna uma data juliana
    """

    log: Logger = getLogger(__name__)
    log.debug('Started')

    if(type(date) == str):
        time = ObjectDateTimeConverter(DateTimeConverter(date=date))
        dt = float(time.jd)
    else:
        dt = date
    
    log.debug('Executed')

    return dt
        
