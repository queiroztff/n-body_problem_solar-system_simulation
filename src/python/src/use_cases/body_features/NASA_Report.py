from logging import Logger, getLogger
from typing import Optional, Union
from entities.api_requests import HorizonsFile
from entities.data_mining import (Gmass, InitialState, Mass, Period, State)
from .functions import date_to_jd, search_spkid

class BodyFeatures(HorizonsFile, Gmass, InitialState, Mass, Period, State):
    """

    Esta classe realiza uma requisição na API Horizons File, processa um nome
    especificado pelo o usuario, e parametros de configurção e retorna uma string
    contendo propriedades físicas ou a efeméride do objeto espicificado 

    Attributes
    ----------
    body : str
        String de pesquisa contendo nome do objeto, designação, SPK-ID, número IAU 
        ou designação de formato compactado MPC

    group : str
        String que possui os valores reservados 'ast' | 'com' | 'pln' | 'sat' ,
        que serve como limitador de pesquisa, 'ast' limita a apesquisa para asteroide,
        'com' para cometas, 'pln' para planetas ou espaçonaves e 'sat' apenas para satélites
        planetários.
    
    center : str
        String que seleciona a origem do sistema de coordenada da efeméride
        Para mais informações consulte o link: https://ssd.jpl.nasa.gov/horizons/manual.html#center

    object_data : bool
        Variável opcional Booleana com valor predefinido False, onde os seguintes valores
        são validos True|False

        object_data = True
            Retorna dados contendo propriedades do objeto pesquisado
        
        object_data = False
            Retorna dados contendo propriedades do objeto pesquisado
    
    initial_state : bool
        Variável opcional Booleana com valor predefinido False, onde os seguintes valores
        são validos True|False

        intial_state = True
            Retorna dados contendo o estado inicial do objeto pesquisado
            e os seguintes atributos serão obrigatórios:

            make_ephemeris : bool = False | True
            center : str
            start_time : str
            out_units : str
        
        intial_state = False
            Retorna dados contendo o estado inicial do objeto pesquisado
            e o seguinte atributo será obrigatório:

            object_data : bool = True 
            ou
            make_ephemeris : bool = True
        
    make_ephemeris : bool
        Variável opcional Booleana com valor predefinido True, onde os seguintes valores
        são validos True|False

        make_ephemeris = True
            Gera enfemérides do objeto pesquisado
            e os seguintes atributos serão obrigatórios:

            initial_state : bool = False
            center : str
            start_time : str
            stop_time : str
            step_size : str
            out_units : str

        make_ephemeris = False
            Não gera enfemérides do objeto pesquisado
            e o seguinte atributo será obrigatório:

            object_data : bool = True 
            ou
            initial_state : bool = True
    

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
                years	y	                    calendar stepping	STEP_SIZE='1 year'
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
    
        gmass -> dict[str, float]
            Retorna um dicionário do tipo {'GM-(km^3/s^2)':float, 'sigma_GM-(km^3/s^2)':float} 
            do objeto pesquisado, onde:
                key: GM-(km^3/s^2)
                    |      |--->Unidades da mediada
                    |
                    |--->Parâmetro gavitacional (produto da constante gravitacional e a massa de um massa 
                                                de um determinado corpo astronômico)
                valor: float

                key: sigma_GM-(km^3/s^2)
                    |           |---> Unidades de media
                    |
                    |--->Incerteza do Parâmetro Gravitacional
                valor: float|None
        
        initial_state -> dict[str, tuple]
            Retorna um dicinário do tipo {'Initial_State':(x, y, z, vx, vy, vz)}
            do objeto pesquisado, onde:
                x, y, z : str
                    São coordenadas cartezianas referente a POSIÇÃO verorial do corpo
                vx, vy, vz : str 
                    são coordenadas cartezianas referente a VELOCIDADE vetorial de corpo
        
        mass -> dict[str,float]
            Retorna um dicionário do tipo {'mass-(kg)':float, 'sigma_mass-(kg)':float}
            do objeto pesquisado, onde:
                key: mass-(kg)
                    |      |--->Unidades da mediada
                    |
                    |--->Massa do corpo
                valor: float

                key: sigma_GM-(km^3/s^2)
                    |           |---> Unidades de media
                    |
                    |--->Incerteza da massa do corpo
                valor: float|None
        
        period -> dict[str, float]:
            Retorna um dicinário do tipo {'period-(d)':float}
            do objeto pesquisado:
                key: period-(d)
                    |       |--->Unidade de medida 'dia' d a qual equivale 86400s 
                    |
                    |---> Periodo (se refere a quanto tempo um corpo 
                                    leva para completar um ciclo de revolução)
                valor: float
        
        state -> dict[str, tuple]
            Retorna um dicinário do tipo {'Initial_State':(t0, x0, y0, z0, vx0, vy0, vz0),
                                                        (t1, x1, y1, z1, vx1, vy1, vz1),
                                                        .
                                                        .
                                                        .
                                                        (tn, xn, yn, zn, vxn, vyn, vzn)}  n-esimo
            contendo o estado do objeto pesquisado, onde:
                t : str 
                    Tempo no calendário juliano
                x, y, z : str 
                    São coordenadas cartezianas referente a POSIÇÃO verorial do corpo
                vx, vy, vz : str 
                    São coordenadas cartezianas referente a VELOCIDADE vetorial de corpo
    """
    
    def __init__(self, 
                 body: str, 
                 group: str, 
                 obj_data: bool,
                 initial_state: bool, 
                 make_ephem: bool, 
                 center: str, 
                 out_units: str, 
                 start_time: Union[str, float], 
                 stop_time: Optional[Union[str, float]] = None, 
                 step_size: Optional[str] = None) -> None:

        super().__init__(command=search_spkid(body=body, group=group), 
                         obj_data=obj_data,
                         make_ephem=(True if(make_ephem or initial_state) else False), 
                         center=center, 
                         start_time=date_to_jd(start_time),
                         stop_time=((date_to_jd(stop_time)) if(stop_time != None) else (date_to_jd(start_time) + 1)),
                         step_size=((step_size) if(step_size != None) else ('1d')), 
                         out_units=out_units)
        
        if(obj_data):
            Gmass.__init__(self, report=self.get_report())
            Mass.__init__(self, report=self.get_report())
            Period.__init__(self, report=self.get_report())

        if(initial_state):
            InitialState.__init__(self, self.get_report())
        
        if(make_ephem):
            State.__init__(self, self.get_report())
    
        self.__log: Logger = getLogger(__name__)
        self.__log.debug('Started')


       
        
        
        


        
