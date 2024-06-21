import re
import requests
from dataclasses import dataclass, field
from functools import cache
from logging import Logger, getLogger
from typing import Union
from .functions import datetime_validation
from entities.interfaces import IBodyFeatures

#Horizons File API
@dataclass(frozen=True)
class HorizonsFile(IBodyFeatures):
    """
    Esta classe realiza uma requisição na API Horizons File, processa um SPK-ID
    especificado pelo o usuario, e parametros de configurção e retorna uma string
    contendo propriedades físicas ou a efeméride do objeto espicificado

    Attributes
    ----------

    command : int
        String de pesquisa contendo SPK-ID do objeto

    object_data : bool
        object_data = True
            Retorna dados contendo propriedades do objeto pesquisado
        
        object_data = False
            Retorna dados contendo propriedades do objeto pesquisado

        
    make_ephemeris : bool
        make_ephemeris = True
            Gera enfemérides do objeto pesquisado
            e os seguintes atributos serão obrigatórios:


        make_ephemeris = False
            Não gera enfemérides do objeto pesquisado
            e o seguinte atributo será obrigatório:
    

    center : str
        String que seleciona a origem do sistema de coordenada da efeméride
        Para mais informações consulte o link: https://ssd.jpl.nasa.gov/horizons/manual.html#center

        
    start_time : str
        String que especifica o início da efeméride.
        Onde o formato da entrada será da forma:
        
        Calendar format:

        tipo      Formato                                  Significado      
        1     YYYY-MM-DD.DDDDD                   ano, mês, dias com casa decimais  (casas decimais sào opcionais)
        2     YYYY-MM-DD hh:mm.m                 ano, mês, dias, horas e minutos com casa decimais (casas decimais sào opcionais)
        3     YYYY-MM-DD hh:mm:ss.s              ano, mês, dias, horas, minutos e segundos com casa decimais (casas decimais sào opcionais)
        
        O mês pode ser especificado usando as abreviações de mês de 3 caracteres , conforme definido nos EUA:
        (case insensitive) (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec) ou (01, 02, 03, 05, 06, 
        07, 08, 09, 10, 11, 12).

        Julian Day Number:
        JD {integer}.{integer}

                                YOUR INPUT             PROGRAM INTERPRETATION
                    ------------------------   ---------------------------

            Calendar formats:

                            2027-May-5 12:30:23.3348   ( 2027-May-5 12:30:23.334 )
                            1965-Jan-27.47083333       ( 1965-Jan-27 11:18:00.000 )
                            2028-05-04 18:00           ( 2028-May-04 18:00.00.000 )

            Julian Day Number:
                            JD 2451545.                ( 2000-Jan-01 12:00:00.000 )
                            JD2451545.                 ( 2000-Jan-01 12:00:00.000 )
                            JD 2433282.42345905        ( 1949-Dec-31 22:09:46.862 )

                            
    stop_time : str
        String que especifica o final da efeméride.
        Onde o formato da entrada será da forma:
        
        Calendar format:

        tipo      Formato                                  Significado      
        1     YYYY-MM-DD.DDDDD                   ano, mês, dias com casa decimais (casas decimais sào opcionais)
        2     YYYY-MM-DD hh:mm.m                 ano, mês, dias, horas e minutos com casa decimais (casas decimais sào opcionais)
        3     YYYY-MM-DD hh:mm:ss.s              ano, mês, dias, horas, minutos e segundos com casa decimais (casas decimais sào opcionais)
        
        O mês pode ser especificado usando as abreviações de mês de 3 caracteres , conforme definido nos EUA:
        (case insensitive) (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec) ou (01, 02, 03, 05, 06, 
        07, 08, 09, 10, 11, 12).

        Julian Day Number:
        JD {integer}.{integer}

                                YOUR INPUT             PROGRAM INTERPRETATION
                    ------------------------   ---------------------------

            Calendar formats:

                            2027-May-5 12:30:23.3348   ( 2027-May-5 12:30:23.334 )
                            1965-Jan-27.47083333       ( 1965-Jan-27 11:18:00.000 )
                            2028-05-04 18:00           ( 2028-May-04 18:00.00.000 )

            Julian Day Number:
                            JD 2451545.                ( 2000-Jan-01 12:00:00.000 )
                            JD2451545.                 ( 2000-Jan-01 12:00:00.000 )
                            JD 2433282.42345905        ( 1949-Dec-31 22:09:46.862 )


    step_size: str
        String que especifica o intervalo entre cada ponto da efeméride.
        Onde o formato da entrada seŕa da forma  integer {units}:

            {units}	Minimum Abbreviation	Description	        Example
            days	d	                    fixed interval	    STEP_SIZE='1d'
            hours	h	                    fixed interval	    STEP_SIZE='3%20h' (w/URL-encoded space)
            minutes	m	                    fixed interval	    STEP_SIZE='10m'
            years	y	                    calendar stepping	STEP_SIZE='1 y'
            months	mo	                    calendar stepping	STEP_SIZE='1 mo'
            unitless                        fixed intervals	    STEP_SIZE='86400' (1 second output given 1 day between start/stop)

        Para mais informações consulte o link: https://ssd-api.jpl.nasa.gov/doc/horizons.html#stepping

    out_units : str
        String que possui os valores reservados 'km-s'|'km-d'|'AU-d', a qual
        seleciona as unidades físicas de distância e tempo da efeméride, onde 'km-s'
        seleciona as unidades quilometros e segundos, 'km-d' seleciona as unidades 
        quilometros e dias, 'AU-D' seleciona as unidades astronômicas e dias 

    Methods
    -------
    get_data() -> str:
        retorna uma string contendo as propriedades físicas e/ou as 
        efeméride do SPK-ID especificado  

    """

    shape: str = field(init=False, default='text')
    command: int
    obj_data: bool
    make_ephem: bool
    ephem_type: str = field(init=False, default='VECTORS')

    center: str
    start_time: Union[str, float]
    stop_time: Union[str, float]
    step_size: str
    out_units: str

    vec_table: str = field(init=False, default='2')
    cal_type: str = field(init=False, default='MIXED')
    cvs_format: str = field(init=False, default='YES')

    __log: Logger = field(init=False, repr=False, default=getLogger(__name__))

    def __post_init__(self) -> None:

     #                               Tratamento de exeções
     #---------------------------------------------------------------------------------
      #_____________start_time___________________
        datetime_validation(self.start_time)
      #Fim__________start_time___________________

      #_____________stop_time___________________
        datetime_validation(self.stop_time)
      #Fim__________stop_time___________________

        
      #_________________out_units_________________________
        out_units_valid_values = ('KM-S', 'KM-D', 'AU-D')
        if(self.out_units.upper() in out_units_valid_values):
            pass
        else:
            message = '''
            Valor inválido especificado para o parâmetro de consulta 'out_units'.
            out_units = 'KM-S' | 'KM-D' | 'AU-D'
            '''
            self.__log.error(message)
            raise ValueError(message)
      #Fim______________out_units_________________________

      #_________________step_size_________________________
        step_size = r'^(\d+)(\s?)((|m|h|d|mo|y)?)$'
        step_size_valid_format = re.compile(pattern=step_size, flags=re.IGNORECASE)
        step_size_is_valid = step_size_valid_format.search(self.step_size)

        if(step_size_is_valid):
            pass
        else:
            message = '''
            Valor inválido especificado para o parâmetro de consulta 'step_size'.
            consulte a documentação
            '''
            self.__log.error(message)
            raise ValueError(message)

      #Fim______________step_size_________________________
     #---------------------------------------------------------------------------------
    @cache
    def get_report(self) -> str:
        """
        retorna uma string contendo as propriedades físicas e/ou as 
        efeméride do SPK-ID especificado    
        """
        url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api?'

        config_api = f'''
        !$$SOF
        !
        format='{self.shape}'
        COMMAND='{self.command}'
        OBJ_DATA='{'YES' if(self.obj_data) else 'NO'}'
        MAKE_EPHEM='{'YES' if(self.make_ephem) else 'NO'}'
        EPHEM_TYPE='{self.ephem_type}'
        !
        VEC_TABLE='{self.vec_table}'
        CAL_TYPE='{self.cal_type}'
        CSV_FORMAT='{self.cvs_format}'
        !
        CENTER='{self.center}'
        START_TIME='{'JD'+str(self.start_time) if(type(self.start_time)==float) else self.start_time}'
        STOP_TIME='{'JD'+str(self.stop_time) if(type(self.stop_time)==float) else self.stop_time}'
        STEP_SIZE='{self.step_size}'
        OUT_UNITS='{self.out_units.upper()}'
        !$$EOF
        '''

        response = requests.post(url=url, data={'format':'text'}, files={'input':config_api})

        match (response.status_code):
            case 200:
                message = '''
                Ok: normal successful result
                '''
                self.__log.info(message)
                pass
            
            case 400:
                message = '''
                Bad Request: the request contained invalid keywords and/or content or used 
                             a request-method other than GET or POST (details returned in the 
                             JSON or text payload)
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
                Internal Server Error: the database is not available at the time of the request
                '''
                self.__log.error(message)
                raise Exception(message)

            case 503:
                message = '''
                Service Unavailable: the server is currently unable to handle the request due
                                     to a temporary overloading or maintenance of the server, 
                                     which will likely be alleviated after some delay

                '''
                self.__log.error(message)
                raise Exception(message)

        return response.text
    





            








