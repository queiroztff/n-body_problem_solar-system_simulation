import re
import logging
from entities.data_mining.interfaces import IMass
from .functions import mass_convert_factor, tuple_str_to_float

class Mass(IMass):

    def __init__(self, report: str) -> None:
        self.__report = report

        self.__log = logging.getLogger(__name__)
        self.__log.debug('Started')
    
    def mass(self) -> dict[str,float]:
        '''
        Property:
        ---------
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
        '''

        prefix = r'(?:Mass)'
        infix = r'(?:[,\sx(]+)(?:([\d]+)\^)([\d]+)(?:\s+\(*(kg|g)\s*\)*)(?:\s*=\s*)'
        sufix = r'(?:~*([\d.]+)\s*[+-]*\s*([\d.]*))'

        mass_search = f'{prefix}{infix}{sufix}'
        find_mass = re.compile(mass_search)

        try:
            data = find_mass.findall(self.__report)[0]
            base, exponent, unit, coefficiente, uncertainty = tuple_str_to_float(data)

            if (uncertainty != None):
                mass = (coefficiente * base**exponent)*mass_convert_factor(unit, 'kg')
                sigma_mass = (uncertainty * base**exponent)*mass_convert_factor(unit, 'kg')
            else:
                mass = (coefficiente * base**exponent)*mass_convert_factor(unit, 'kg')    
                sigma_mass = None
        except:
            message = '''
            Não foi possível extrair a 'massa' do objeto do relatório
            '''
            self.__log.info(message)
            mass = None
            sigma_mass =None
        
        self.__log.debug('Successfully executed')
        return {'mass-(kg)':mass, 'sigma_mass-(kg)':sigma_mass}
