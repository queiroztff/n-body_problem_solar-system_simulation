import json
import requests
from dataclasses import dataclass, field
from functools import cache
from logging import Logger, getLogger
from typing import Dict, List, Union
from entities.interfaces import ISpkIdSearch

# Horizons Lookup API
@dataclass(frozen=True)
class Lookup(ISpkIdSearch):
    """
    Esta classe realiza uma requisição na API Horizons Lookup
    processa um nome especificado pelo usuário, designação, SPK-ID, número IAU,
    designaçao MPC, ou outro aliases histórico e retorna através de uma propriedade o SPK-ID
    do objeto especificado

    
    Attributes
    ----------
    sstr : str
        String de pesquisa contendo nome do objeto, designação, SPK-ID, número IAU 
        ou designação de formato compactado MPC
    
    group : str
        String que possui os valores reservados 'ast' | 'com' | 'pln' | 'sat' ,
        que serve como limitador de pesquisa, 'ast' limita a apesquisa para asteroide,
        'com' para cometas, 'pln' para planetas ou espaçonaves e 'sat' apenas para satélites
        planetários.
    
    Methods
    -------
    get_data() -> Dict[str, Union[str, List[Dict[str, str]]]]
        Retorna um dicionário/json com os possiveis objetos que foram pesquisados, o qual possui
        as seguintes chaves:
            {
                "count" : int,
                "result" : [
                    {
                        
                        "name" : str,
                        "pdes" : str,
                        "spkid" : str,
                        "alias" : str | List[str],
                    },
                    .
                    .
                    .
                ],
                 
                "signature" : {
                    "source" : str,
                    "version" : str
                }
            }
    """

    sstr: str
    group: str
    shape: str = field(init=False, default='json')

    __log: Logger = field(init=False, repr=False, default=getLogger(__name__))

    def __post_init__(self) -> None:

     #                               Tratamento de exeções
     #---------------------------------------------------------------------------------
      #_________________group___________________________
        group_valid_values = ('ast', 'com', 'pln', 'sat')
        if (self.group.lower() in group_valid_values):
            pass
        else:
            message = '''
            Valor inválido especificado para o parâmetro de consulta 'group'.
            group = 'ast' | 'com' | 'pln' | 'sat'
            '''
            self.__log.error(message)
            raise ValueError(message)
       #Fim______________group___________________________
     #---------------------------------------------------------------------------------

        self.__log.debug('Started')
    
    @cache
    def get_data(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Retorna um dicionário/json com os possiveis objetos que foram pesquisados, o qual possui
        as seguintes chaves:
            {
                "count" : int,
               ?"result" : [
                    {
                        "name" : str,               (Nome do objeto correspondente (para asteróides numerados, conterá o número IAU, bem como o nome IAU)
                        "pdes" : str,               (Designação provisória primária ( null se não conhecida))
                        "spkid" : str,              (ID SPK primário)
                        "alias" : str | List[str],  (Uma lista de designações alternativas, IDs SPK)
                    },
                    .
                    .
                    .
                ],
                 
                "signature" : {
                    "source" : str,
                    "version" : str
                }
            }
        """

        url = 'https://ssd.jpl.nasa.gov/api/horizons_lookup.api?'
        url += f'sstr={self.sstr}&group={self.group}&format={self.shape}'

        response = requests.get(url)

        match (response.status_code):
            case 200:
                message = '''
                Ok: normal result
                '''
                self.__log.info(message)
                pass

            case 400:
                message = '''
                Bad Request: request contained invalid keywords and/or content
                '''
                self.__log.error(message)
                raise Exception(message)
            
            case 405:
                message = '''
                Method Not Allowed: the request used an incorrect HTTP method 
                                    (see the HTTP Request section)
                '''
                self.__log.error(message)
                raise Exception(message)
            
            case 500:
                message = '''
                Internal Server Error: necessary databases are not available 
                                       (server-side error)
                '''
                self.__log.error(message)
                raise Exception(message)
            
            case 503:
                message = '''
                Service Unavailable: the server is currently unable to handle 
                                     the request due to a temporary overloading or 
                                     maintenance of the server, which will likely be 
                                     alleviated after some delay
                '''
                self.__log.error(message)
                raise Exception(message)

        try:
            data = json.loads(response.text)
            self.__log.debug('Executed')
        except:
            message = 'Não é possível decodificar os resultados do arquivo json'
            self.__log.error(message)
            raise ValueError(message)
        
        return data

        
