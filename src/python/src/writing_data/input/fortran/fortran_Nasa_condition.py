import os
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List, Optional, Type
from use_cases.body_features import BodyFeatures
from use_cases.body_features import date_to_jd
from entities.json_to_object.fortran_simulation_with_NASA_initial_condition_config import Itens
from .functions import simulation_list_nasa_insert

@dataclass
class FortranNasaInsert:
    """
    Classe responsável por escrever os arquivos de entrada para o código Fortran
    que simula o problema de N-corpos.

    Os arquivos de entrada são gerados a partir de um arquivo de configuração JSON
    que define as condições iniciais da simulação apartir da base de dados da Nasa.

    A classe FortranNasaInsert utiliza a classe BodyFeatures para obter
    as informações sobre os corpos do sistema solar.

    Attributes:
        list_of_simulation (Optional[List[str]]): Lista de nomes das simulações
            a serem escritas. Se None, todas as simulações definidas no arquivo
            JSON serão escritas.

    Methods:
        writing_init() -> None: 
            Escreve o arquivo '__init__.sim' no diretório 'data/input/fortran'.

        writing_config() -> None: 
            Escreve os arquivos de configuração das simulações no diretório 'data/input/fortran'.

        writing_ic() -> None: 
            Escreve os arquivos de condições iniciais das simulações no diretório 'data/input/fortran'
    """
    
    list_of_simulation: Optional[List[str]] = field(default=None)

    __simulation_list: List[Itens] = field(init=False, repr=False)
    __input_fortran_path: str = field(init=False, repr=False)
    __log: Logger = field(init=False, repr=False, default=getLogger(__name__))

    def __post_init__(self) -> None:

        # Definindo lista que os objetos objetos selecionados da função simulation_list 
        #___________________________________________________________
        self.__simulation_list = simulation_list_nasa_insert(self.list_of_simulation)
        #___________________________________________________________

        # Definindo caminho absoluto para o diretório 'data/input'
        #___________________________________________________________
        absollute_path = os.path.dirname(__file__)
        relative_path = '../../../../../../' + 'data/input/fortran'
        self.__input_fortran_path = os.path.abspath(os.path.join(absollute_path, relative_path))
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
                            make_ephem=False,
                            center=inject.center,
                            out_units=inject.out_units,
                            start_time=inject.calendar.start_time)
        
        self.__log.debug('Executed')

        return body
    
    def writing_init(self) -> None:
        """
        Escreve o arquivo '__init__.sim' no diretório 'data/input/fortran'.

        O arquivo '__init__.sim' contém a lista de nomes das simulações
        que serão executadas.
        """

        path_init_sim = self.__input_fortran_path + '/' + '__init__.sim'
        
        with open(file=path_init_sim, mode='w') as file:
            for simulation in self.__simulation_list:
                file.write(f'{simulation.name} \n')
        
        self.__log.debug('Executed')
    

    def writing_config(self) -> None:
        """
        Escreve os arquivos de configuração das simulações no diretório 'data/input/fortran'.

        Os arquivos de configuração das simulações têm o nome '<simulation_name*>.config'
        e contém as informações sobre os parâmetros da simulação, como o método de integração,
        a tolerância, o passo de integração, a constante gravitacional, etc.
        """

        for simulation in self.__simulation_list:
            path_simulation_config = self.__input_fortran_path + '/' + simulation.name + '.config'

            with open(file=path_simulation_config, mode='w') as file:
                file.write(f'{simulation.method.name} \n')
                file.write(f'{simulation.method.eps} \n')
                file.write(f'{simulation.method.tol} \n')
                file.write(f'{simulation.method.step.hmax} {simulation.method.step.hmin} \n')
                file.write(f'{simulation.method.G} \n')
                file.write(f'{simulation.method.conversion_factor.distance} \n')
                file.write(f'{simulation.method.conversion_factor.mass} \n')
                file.write(f'{simulation.method.conversion_factor.time} \n')
    
        self.__log.debug('Executed')

    def writing_ic(self) -> None:
        """
        Escreve os arquivos de condições iniciais das simulações no diretório 'data/input/fortran'.

        Os arquivos de condições iniciais das simulações têm o nome '<simulation_name*>.ic'
        e contém as informações sobre as condições iniciais dos corpos do sistema solar,
        como a massa, a posição e a velocidade.
        """

        for simulation in self.__simulation_list:

            path_simulation_ic = self.__input_fortran_path + '/' + simulation.name + '.ic'

            with open(file=path_simulation_ic, mode='w') as file:

                # Escreven o dóminio da simulação no arquivo <simulation_name>.ic
                t0 = date_to_jd(simulation.calendar.start_time)
                tf = date_to_jd(simulation.calendar.stop_time)

                if(simulation.relative_time == True):
                    file.write(f'{t0 -t0} {tf - t0} \n')
                else:
                    file.write(f'{t0} {tf} \n')
                

                # Escrevendo as condições iniciais dos corpos
                if(simulation.body.ast is not None):
                    for ast in simulation.body.ast:
                        body = self.__body_fetures(body_name = ast,
                                                   group = 'ast',
                                                   inject = simulation)
                        
                        mass = body.mass()['mass-(kg)']
                        x0, y0, z0, vx0, vy0, vz0 = body.initial_state()['Initial_State']

                        file.write(f'{ast} {mass} {x0} {y0} {z0} {vx0} {vy0} {vz0} \n')
                
                if(simulation.body.com is not None):
                    for com in simulation.body.com:
                        body = self.__body_fetures(body_name = com,
                                                   group = 'com',
                                                   inject = simulation)
                        
                        mass = body.mass()['mass-(kg)']
                        x0, y0, z0, vx0, vy0, vz0 = body.initial_state()['Initial_State']

                        file.write(f'{com} {mass} {x0} {y0} {z0} {vx0} {vy0} {vz0} \n')
                
                if(simulation.body.pln is not None):
                    for pln in simulation.body.pln:
                        body = self.__body_fetures(body_name = pln,
                                                   group = 'pln',
                                                   inject = simulation)
                        
                        mass = body.mass()['mass-(kg)']
                        x0, y0, z0, vx0, vy0, vz0 = body.initial_state()['Initial_State']

                        file.write(f'{pln} {mass} {x0} {y0} {z0} {vx0} {vy0} {vz0} \n')

                if(simulation.body.sat is not None):
                    for sat in simulation.body.sat:
                        body = self.__body_fetures(body_name = sat,
                                                   group = 'sat',
                                                   inject = simulation)
                        
                        mass = body.mass()['mass-(kg)']
                        x0, y0, z0, vx0, vy0, vz0 = body.initial_state()['Initial_State']

                        file.write(f'{sat} {mass} {x0} {y0} {z0} {vx0} {vy0} {vz0} \n')
                
        self.__log.debug('Executed')


