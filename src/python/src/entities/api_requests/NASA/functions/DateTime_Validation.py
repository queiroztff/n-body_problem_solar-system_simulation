import re
from logging import getLogger
from typing import Union

def datetime_validation(datetime: Union[str, float]) -> None:
    """
    Dada uma data/tempo, esta função verifica se sua formatação encontra-se nas especificações da API da NASA,
    caso esteja pass
    caso não esteja um erro de ValueError é levantado
    Arguments:
    ---------
    datetime : str|float
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
    Return:
    -------
        None
    """

    log = getLogger(__name__)

    if(isinstance(datetime, str)):
        year = r'(\b\d{4}\b)'

        months = r'(\bjan\b|\bfeb\b|\bmar\b|\bapr\b'\
            r'|\bmay\b|\bjun\b|\bjul\b|\bagu\b'\
            r'|\bsep\b|\boct\b|\bnov\b|\bdec\b'\
            r'|\b0[1-9]\b|\b1[0-2]\b)'

        days = r'([0-2]\d|3[0-1])((\.\d+)?)'
        hours = r'([0-1]\d|2[0-3])'
        minutes = r'([0-5]\d)((\.\d+)?)'
        seconds = r'(\d+)((\.\d+)?)'


        calendar_type_1 = fr'^{year}-{months}-{days}$'
        calendar_type_2 = fr'^{year}-{months}-{days}\s{hours}:{minutes}$'
        calendar_type_3 = fr'^{year}-{months}-{days}\s{hours}:{minutes}:{seconds}$'
        calendar = fr'({calendar_type_1})|({calendar_type_2})|({calendar_type_3})'
    
        calendar_valid_format = re.compile(calendar, flags=re.IGNORECASE)
        calendar_is_valid = calendar_valid_format.search(str(datetime))
        
        if(calendar_is_valid):
            pass
        else:
            message = f'''
            Valor inválido especificado para o parâmetro de consulta 'datetime = {datetime}: str'
            consulte a documentação para verificar a formatação correta deste parametro
            '''
            log.error(message)
            raise ValueError(message)
        
    elif(isinstance(datetime, float)):

        julian_day = r'(^\d+\.\d*$)'
        julian_day_valid_format = re.compile(julian_day, flags=re.IGNORECASE)
        julian_day_is_valid = julian_day_valid_format.search(str(datetime))

        if(julian_day_is_valid):
            pass
        else:
            message = f'''
            Valor inválido especificado para o parâmetro de consulta 'datetime = {datetime}: float'
            consulte a documentação para verificar a formatação correta deste parametro
            '''
            log.error(message)
            raise ValueError(message)
    
    else:
        message = f'''
        Valor inválido especificado para o parâmetro de consulta 'datetime = {datetime}: str|float'
        consulte a documentação para verificar a formatação correta deste parametro
        '''
        log.error(message)
        raise ValueError(message)


    




       


