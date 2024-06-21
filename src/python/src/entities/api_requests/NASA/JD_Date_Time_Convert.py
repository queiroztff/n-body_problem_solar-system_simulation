import json
import requests
from dataclasses import dataclass, field
from functools import cache
from logging import Logger, getLogger
from typing import Dict, Union
from .functions import datetime_validation
from entities.interfaces import IJdDateTimeConvert

# JD Date/Time Converter API
@dataclass(frozen=True)
class DateTimeConverter(IJdDateTimeConvert):
    """
    Esta classe realiza um requisição na API JD Date/Time Converter,
    dado um número do dia juliano (JD), ela retorna a data/hora do calendário
    gregroriano. Dada uma data/hora do calendário gregroriano, ela retorne o número do dia 
    juliano correspondente.

    Attributes
    ----------
    date : str|float

        date : str
            String que receberá uma data/hora do calendário gregroriano
            Onde o formato desta entrada será da forma:

            Calendar format:

            tipo      Formato                                  Significado      
            1     YYYY-MM-DD.DDDDD                   ano, mês, dias com casa decimais  (casas decimais sào opcionais)
            2     YYYY-MM-DD hh:mm.m                 ano, mês, dias, horas e minutos com casa decimais (casas decimais sào opcionais)
            3     YYYY-MM-DD hh:mm:ss.s              ano, mês, dias, horas, minutos e segundos com casa decimais (casas decimais sào opcionais)
            
            O mês pode ser especificado usando as abreviações de mês de 3 caracteres , conforme definido nos EUA:
            (case insensitive) (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec) ou (01, 02, 03, 05, 06, 
            07, 08, 09, 10, 11, 12).

        date : float
            Float que receberá o número do dia juliano
            Onde o formato desta entrada séra da forma:

             Julian Day Number:
        
             {integer}.{integer}

             

    Methods
    -------
    get_data() -> Dict[str, Union[str, Dict[str,str]]]
        Retorna um dicionário/json com a conversão e dados adicionais formatados
    """
    date: Union[str, float]
    
    __format_cal: str = field(init=False, repr=False, default='s.3')
    __format_jd: str = field(init=False, repr=False, default='jd.7')
    __log: Logger = field(init=False, repr=False, default=getLogger(__name__))

    def __post_init__(self) -> None:
        
     #                               Tratamento de exeções
     #---------------------------------------------------------------------------------
      #______________date____________________
        datetime_validation(self.date)
      #Fim___________date____________________  
     #---------------------------------------------------------------------------------
        
        self.__log.debug('Started')
    
    @cache
    def get_data(self) -> Dict[str, Union[str, Dict[str,str]]]:
        """
        Retorna um dicionário/json com a conversão e dados adicionais formatados, o qual possui as seguintes chaves:
            {
                "cd": str,            (String de data/hora do calendário formatada conforme solicitado)
                "year": int,          (O ano do resultado cd)
               ?"month": int,         (Mês numérico (por exemplo, 02), (caso a conversão seja cd para jd))
                "month_name": str,    (Abreviatura do mês com 3 caracteres (por exemplo, Feb))
                "doy": int,           (Dia do ano (por exemplo, 247))
                "dow": int,           (Dia da semana (1 a 7  com 1=domingo)) 
                "dow_name": str,      (Nome do dia da semana (por exemplo, 'segunda-feira')) 
                "day_and_time": str,  (String formatada apenas para dia e hora (útil para formatar resultados personalizados))
               ?"jd": str],           (String do número do dia juliano (caso a conversão seja cd para jd))

                "signature" : {
                    "source" : str,
                    "version" : str
                }
            }
        """

        url = 'https://ssd-api.jpl.nasa.gov/jd_cal.api?'
        if(isinstance(self.date, str)):
            url += f'cd={self.date}&format={self.__format_jd}'
        if(isinstance(self.date, float)):
            url += f'jd={str(self.date)}&format={self.__format_cal}'
        
        response = requests.get(url)

        match(response.status_code):
            case 200:
                message = '''
                OK: normal successful result, data returned
                '''
                self.__log.info(message)
                pass

            case 400:
                message = '''
                Bad Request: the request contained invalid keywords 
                and/or content, details returned
                '''
                self.__log.error(message)
                raise Exception(message)

            case 405:
                message = '''
                Method Not Allowed: the request used an incorrect method 
                (see the HTTP Request section)
                '''
                self.__log.error(message)
                raise Exception(message)
            
            case 500:
                message = '''
                Internal Server Error: the server is not available at the time of 
                the request
                '''
                self.__log.error(message)
                raise Exception(message)
            
            case 503:
                message = '''
                Service Unavailable: the server is currently unable to handle the request 
                due to a temporary overloading or maintenance of the server, which will likely 
                be alleviated after some delay
                '''
                self.__log.error(message)
                raise Exception(message)
        
        try:
            data = json.loads(response.text)
            self.__log.debug('Executed')
        except:
            message = 'Não é possível decodificar os resultados do arquivo json'
            self.__log.error(message)
            raise ValueError(message)
        
        return data




