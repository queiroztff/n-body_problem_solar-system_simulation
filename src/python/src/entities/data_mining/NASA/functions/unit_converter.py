from logging import Logger, getLogger

def mass_convert_factor(unit_in:str, unit_out:str) -> float:
    '''
    Dada duas unidades de massa (presente na tabela de unidades) esta função retorna o fator 
    de converção

    table_units = ['kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg']
    Parameter
    ---------
        unit_in: str
        unidades da orginal grandeza

        unit_out: str
        unidades da grandeza que deseja fazer a converção

    Returns
    --------
        float
        número do fator de converção

    '''

    log: Logger = getLogger(__name__)

    table_units = {'kg':1000, 'hg':100, 'dag':10, 'g':1, 'dg':0.1, 'cg':0.01, 'mg':0.001}

    if (unit_in in table_units) and (unit_out in table_units):
        factor = table_units[unit_in]/table_units[unit_out]
        log.debug('Executed')
    else:
        message = 'Unidades de conversão invalidas'
        log.error(message)
        raise message
    return factor
