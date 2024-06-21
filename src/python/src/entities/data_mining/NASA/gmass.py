import re
import logging
from entities.data_mining.interfaces import IGmass
from .functions import tuple_str_to_float


class Gmass(IGmass):

    def __init__(self, report: str) -> None:
        self.__report = report
        
        self.__log = logging.getLogger(__name__)
        self.__log.debug('Satarted')
    
    def gmass(self) -> dict[str, float]:
        '''
        Property:
        ---------
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
        '''
        
        prefix_GM = r'(?:GM)'
        infix_GM = r'(?:[,\s]+)(?:\(*km\^3\/s\^2\)*)(?:\s*=\s*)'
        sulfix_GM = r'(?:([\d.]+)\s*[+-]*\s*([\d.]*))'

        GM_search = f'{prefix_GM}{infix_GM}{sulfix_GM}'
        find_GM = re.compile(GM_search)

        data = find_GM.findall(self.__report)[0]

        gm, uncertainty = tuple_str_to_float(data)
    
        if (uncertainty == None):
            prefix_sigma = r'(?:GM)'
            infix_sigma = r'(?:[,\s]+)(?:1-sigma)(?:[,\s]*)(?:\(*km\^3\/s\^2\)*)(?:\s*=\s*)'
            sulfix_sigma = r'(?:[+-]*\s*([\d.]+))'
            
            sigma_search = f'{prefix_sigma}{infix_sigma}{sulfix_sigma}'
            find_sigma = re.compile(sigma_search)

            if find_sigma.search(self.__report):
                uncertainty = float(find_sigma.findall(self.__report)[0])
            else:
                uncertainty = None
        else:
            pass

        self.__log.debug('Successfully executed')
        return {'GM-(km^3/s^2)':gm, 'sigma_GM-(km^3/s^2)':uncertainty}