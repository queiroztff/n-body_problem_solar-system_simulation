from logging import Logger, getLogger
from typing import List, Tuple, Union

def tuple_str_to_float(t:Tuple[str]) -> Tuple[Union[float, str]]:
    '''
    Dada um tupla com representação numerica em string está função convete
    estes valores para float

    Parameter
    ---------
        t: Tuple[str]
            Tupla com valores númericos em string e simbolos referente a massa

    Returns
    --------
        Tuple[Union[float, str]]


    '''
    log: Logger = getLogger(__name__)

    l: List[str] = list(t)

    for i in range(len(l)):
        try:
            l[i] = float(l[i])
        except:
            if (l[i] == ''):
                l[i] = None
            elif(l[i] in ['kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg']):
                l[i] = l[i]
            else:
                message = '''
                Tupla deve conter apenas conter valores númericos em string,
                ou as unidades de massa ['kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg']
                '''
                log.error(message)
                raise message
    
    log.debug('Executed')

    return tuple(l)

