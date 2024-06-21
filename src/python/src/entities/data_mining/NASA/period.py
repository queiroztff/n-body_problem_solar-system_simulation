import re
import logging
from entities.data_mining.interfaces import IPeriod

class Period(IPeriod):
    def __init__(self, report: str) -> None:
        self.__report = report

        self.__log = logging.getLogger(__name__)
        self.__log.debug('Started')
    
    def period(self) -> dict[str, float]:
        '''
        Retorna um dicinário do tipo {'period-(d)':float}
        do objeto pesquisado:
            key: period-(d)
                |       |--->Unidade de medida 'dia' d a qual equivale 86400s 
                |
                |---> Periodo (se refere a quanto tempo um corpo 
                                leva para completar um ciclo de revolução)
            valor: float
        '''

        prefix_pln = r'(?:(?:Mean\ssidereal|Sidereal)\s(?:orb[.]*|orbit)\s(?:per[.,]*|period)\s*[d]*)'
        prefix_sat = r'(?:(?:Orbit|Orbital)\speriod)'
        prefix = r'(?:'+prefix_pln+r'|'+prefix_sat+r')'
        infix = r'(?:\s*(?:=|~)\s*)'
        sulfix = r'(?:([\d.]+)(?:\sd*|\s\s+))'

        period_search = f'{prefix}{infix}{sulfix}'
        find_period = re.compile(period_search)

        try:
            data = find_period.findall(self.__report)[0]
            period = float(data)
        except:
            message = '''
            Não foi possível extrair o 'período' do objeto do relatório
            '''
            self.__log.info(message)
            period = None
        
        self.__log.debug('Successfully executed')
        return {'period-(d)':period}

       