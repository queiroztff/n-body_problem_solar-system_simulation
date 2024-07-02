import os
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List, Optional, Type
from use_cases.body_features import BodyFeatures
from entities.json_to_object.NASA_simulation_config import Itens
from .functions import simulation_list

@dataclass
class NasaSimulation:
    """
    Classe responsável por escrever os dados de uma simulação do sistema solar proveniente
    da base de dados da Nasa, em arquivos .sob.

    Attributes:
        list_of_simulation: (Optional[List[str]]) = None 
            Lista de nomes de simulações contidas no arquivo 'data/input/python/NASA_simulation_config.json'
            a serem escritas. Se None, todas as simulações serão escritas.

     Methods:
        writing_simulation() -> None:
            Escreve o estado dos corpos em arquivos .sob, 
            organizados em subpastas com o nome dos corpos, na pasta com o nome da simulação.
    """
    
    list_of_simulation: Optional[List[str]] = field(default=None)

    __simulation_list: List[Itens] = field(init=False, repr=False)
    __output_path: str = field(init=False, repr=False)
    __log: Logger = field(init=False, repr=False, default=getLogger(__name__))

    def __post_init__(self) -> None:

        # Definindo lista que os objetos objetos selecionados da função simulation_list 
        #___________________________________________________________
        self.__simulation_list = simulation_list(self.list_of_simulation)
        #___________________________________________________________

        # Definindo caminho absoluto para o diretório 'data/output'
        #___________________________________________________________
        absollute_path = os.path.dirname(__file__)
        relative_path = '../../../../../' + 'data/output'
        self.__output_path = os.path.abspath(os.path.join(absollute_path, relative_path))
        #___________________________________________________________

        self.__log.debug('Started')

    def __body_fetures(self, 
                       body_name:str, 
                       group:str,
                       inject:Type[Itens]) -> Type[BodyFeatures]:
        """
        Esta função realiza a instância da classe BodyFeatures
        e retorna um objeto com caracteristicas do corpo pesquisado
        """

        body = BodyFeatures(body=body_name,
                            group=group,
                            obj_data=True,
                            initial_state=True,
                            make_ephem=True,
                            center=inject.center,
                            out_units=inject.out_units,
                            start_time=inject.calendar.start_time,
                            stop_time=inject.calendar.stop_time,
                            step_size=inject.step_size)
        
        self.__log.debug('Executed')

        return body
    
    def __writing_state(self, 
                        path:str, 
                        relative_time:bool, 
                        inject_features: Type[BodyFeatures]) -> None:
        """
        Dado o nome de um caminho de um arquivo 'path' que representa o nome de um corpo 
        e o estado deste corpo, esta função escreve o estado do corpo neste arquivo
        """

        if(relative_time):
            t0 = float(inject_features.state()['State'][0][0])
        else:
            t0 = float(0)

        with open(file=path, mode='w') as file:
            for t, x, y, z, vx, vy, vz in inject_features.state()['State']:
                file.write(f"{float(t) - t0} {x} {y} {z} {vx} {vy} {vz} \n")

        self.__log.debug('Executed')

    def writing_simulation(self) -> None:
        """
        Esta função escreve o estado dos corpos em arquivos .sob, 
        organizados em pastas com o nome da simulação.
        """

        for simulation in self.__simulation_list:

            # Criando diretório com nome das simulações
            simulation_name = self.__output_path + '/' + simulation.name
            os.makedirs(name=simulation_name, 
                        mode=511, 
                        exist_ok=True)

            # Escrevendo o estado dos corpos nos arquivos
            if(simulation.body.ast is not None):
                for ast in simulation.body.ast:
                    path_ast_name = simulation_name + '/' + ast + '.sob'
                    self.__writing_state(path = path_ast_name,
                                         relative_time = simulation.relative_time,
                                         inject_features = self.__body_fetures(body_name = ast,
                                                                               group = 'ast',
                                                                               inject = simulation))
                    
            if(simulation.body.com is not None):
                for com in simulation.body.com:
                    path_com_name = simulation_name + '/' + com + '.sob'
                    self.__writing_state(path = path_com_name,
                                         relative_time = simulation.relative_time,
                                         inject_features = self.__body_fetures(body_name = com,
                                                                               group = 'com',
                                                                               inject = simulation))

            if(simulation.body.pln is not None):
                for pln in simulation.body.pln:
                    path_pln_name = simulation_name + '/' + pln + '.sob'
                    self.__writing_state(path = path_pln_name,
                                         relative_time = simulation.relative_time,
                                         inject_features = self.__body_fetures(body_name = pln,
                                                                               group = 'pln',
                                                                               inject = simulation))
                    
            if(simulation.body.sat is not None):
                for sat in simulation.body.sat:
                    path_sat_name = simulation_name + '/' + sat + '.sob'
                    self.__writing_state(path = path_sat_name,
                                         relative_time = simulation.relative_time,
                                         inject_features = self.__body_fetures(body_name = sat,
                                                                               group = 'sat',
                                                                               inject = simulation))
        
        self.__log.debug('Executed')
