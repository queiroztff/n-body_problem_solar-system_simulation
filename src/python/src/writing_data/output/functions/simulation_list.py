from logging import Logger, getLogger
from typing import List, Optional, Type
from entities.json_to_object.NASA_simulation_config import NasaSimulationConfig
from entities.json_to_object.NASA_simulation_config import Itens

def simulation_list(name:Optional[List[str]] = None, 
                    _nasa = NasaSimulationConfig()) -> List[Itens]:
    """
    Dada um nome ou uma lista de nomes, essa função verifica se os mesmos está(ão) contidos 
    em NASA_simulation_config.json, caso esteja uma lista com os objetos com nomes da simulações é retornado, caso não esteja um erro é levantado. 
    Caso name = None, a lista contendo os nomes das simulações em NASA_simulation_config.json é retornado

    Parameters
    ----------
        name: Optional[List[str]] = None
            Se informado, nome ou uma lista de nomes de simulações contidos em 
            em um arquivo json com o mesmo esquema do arquivoNASA_simulation_config.json
    
    Return
    ------
        Type[Itens]
            Contém uma lista, contendo os o nomes de simulação especificados 

    Raises
    ------
        NotImplementedError 
            Lista de nomes de simulações não está contido em NASA_simulation_config.json
    """
    
    log: Logger = getLogger(__name__)

    #Listando todos os nomes de simulações do json NASA_simulation_config.json
    #___________________________________________________________
    list_nasa_simulation_name = [_nasa.simulation[i].name for i in range(len(_nasa.simulation))]
    #___________________________________________________________

    if(name is None):
        list_name = _nasa.simulation
    elif(set(name) <= set(list_nasa_simulation_name)):
        list_name = [itens for itens in _nasa.simulation if(itens.name in name)]
    else:
        message = f'''
        Lista de nomes de simulações {name} não está contido
        na lista de nomes {list_nasa_simulation_name} provenientes
        NASA_simulation_config.json
        '''
        log.error(message)
        raise(TypeError(message))
    
    log.debug('Executed')
    
    return list_name
