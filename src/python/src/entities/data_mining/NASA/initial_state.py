import re
import logging
from typing import Tuple
from entities.data_mining.interfaces import IInitialState

class InitialState(IInitialState):

    def __init__(self, report: str) -> None:
        self.__report = report
        
        self.__log = logging.getLogger(__name__)
        self.__log.debug('Started')
    
    def initial_state(self) -> dict[str, Tuple[str]]:
        '''
        Property:
        ---------
        Retorna um dicinário do tipo {'Initial_State':(x, y, z, vx, vy, vz)}
        do objeto pesquisado, onde:
            x, y, z : str
                São coordenadas cartezianas referente a POSIÇÃO verorial do corpo
            vx, vy, vz : str 
                são coordenadas cartezianas referente a VELOCIDADE vetorial de corpo
        '''
        
        jdtdb = r'(?:[\d.]+)'
        calendar_date = r'(?:A\.D\. \d{4}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}\.\d{4})'
        coordinates = r'([\+\-\d.E]+)'
        separator = r'(?:,\s*)' 

        init_conditions_search = r'^'+jdtdb+separator+calendar_date+separator+(coordinates+separator)*6+r'$'
        find_init_conditions = re.compile(init_conditions_search, flags=re.MULTILINE)

        try:
            init_conditions = find_init_conditions.findall(self.__report)[0]
        except:
            message = '''
            Não foi possível extrair o 'estado inicial' do corpo do relatório
            '''
            self.__log.info(message)
            init_conditions = None


        self.__log.debug('Successfully executed')
        return {'Initial_State':init_conditions}
    
