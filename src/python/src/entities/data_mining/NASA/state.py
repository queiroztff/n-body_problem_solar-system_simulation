import re
import logging
from typing import List, Tuple
from entities.data_mining.interfaces import IState

class State(IState):

    def __init__(self, report: str) -> None:
        self.__report = report

        self.__log = logging.getLogger(__name__)
        self.__log.debug('Started')
    
    def state(self) -> dict[str, List[Tuple[str]]]:
        '''
        Retorna um dicinário do tipo {'State':[(t0, x0, y0, z0, vx0, vy0, vz0),
                                              (t1, x1, y1, z1, vx1, vy1, vz1),
                                               .
                                               .
                                               .
                                              (tn, xn, yn, zn, vxn, vyn, vzn)]}  n-esimo
        contendo o estado do objeto pesquisado, onde:
            t : str 
                Tempo no calendário juliano
            x, y, z : str 
                São coordenadas cartezianas referente a POSIÇÃO verorial do corpo
            vx, vy, vz : str 
                São coordenadas cartezianas referente a VELOCIDADE vetorial de corpo
        '''

        jdtdb = r'([\d.]+)'
        calendar_date = r'(?:A\.D\. \d{4}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}\.\d{4})'
        coordinates = r'([\+\-\d.E]+)'
        separator = r'(?:,\s*)'

        state_search = r'^'+jdtdb+separator+calendar_date+separator+(coordinates+separator)*6+r'$'
        find_state = re.compile(state_search, flags=re.MULTILINE)

        try:
            state = find_state.findall(self.__report)
        except:
            message = '''
            Não foi possível extrair a 'massa' do objeto do relatório
            '''
            self.__log.info(message)

        self.__log.debug('Successfully executed')
        return {'State':state}

