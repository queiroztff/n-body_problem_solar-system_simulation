import re
from logging import Logger, getLogger
from entities.api_requests import Lookup
from entities.json_to_object import ObjectLookup

def search_spkid(body: str, group: str) -> int:
    """
    Especificado o nome de um corpo celeste e o grupo que ele faz parte 
    esta função retorna o SPK-ID do mesmo, caso o SPK-ID não seja encontrado 
    é levantado um erro.
    Arguments:
    ---------
        body: str
            Nome do corpo celeste a ser pesquisado

        group: str
            grupo o qual este compo faz parte
            para mais informações consulte a documentação do modúlo
            entities.json_to_object -> ObjectLookup
    Return:
    -------
        int:
            retorna uma string do SPK-ID do body pesquisado
            caso o SPK-ID não seja encontrado um erro é levantado 
    """
    log: Logger = getLogger(__name__)

    search_id = ObjectLookup(Lookup(sstr=body, group=group))
    exact_name = re.compile(r'^'+body+'$', flags = re.IGNORECASE)

    try: 
        for item in range(search_id.count):
            if(exact_name.search(search_id.result[item].name)):
                id = search_id.result[item].spkid
                break
            else:
                continue
        log.debug('Executed')
        return int(id)
    except:
        log.error('Corpo não encontrado')
        raise Exception('Corpo não encontrado')

