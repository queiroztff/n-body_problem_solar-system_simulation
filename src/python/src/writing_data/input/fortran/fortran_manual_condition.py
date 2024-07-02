import os
from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import List, Optional
from entities.json_to_object.fortran_simulation_manual_insert_initial_condition import Itens
from .functions import simulation_list_manual_insert

@dataclass
class FortranManualInsert:
    """
    Classe responsável por escrever os arquivos de entrada para o código Fortran
    que simula o problema de N-corpos.

    Os arquivos de entrada são gerados a partir de uma lista de simulações
    definidas em um arquivo JSON. Cada simulação contém informações sobre
    o método numérico a ser utilizado, as condições iniciais dos corpos
    e o período de tempo a ser simulado.

    Attributes:
        list_of_simulation: Optional[List[str]] = None
            Lista de nomes de simulações específicas a serem escritas, as quais devem estar
            contidadas no arquivo 'data/input/python/fortran_simulation_manual_insert_initial_condition.json'
            caso nenhuma lista seja informado, todas as simulações serão execultadas

    Methods:
        writing_init -> None: 
            Escreve o arquivo '__init__.sim' no diretório 'data/input/fortran'.

        writing_config() -> None: 
            Escreve os arquivos de configuração para cada simulação no diretório 'data/input/fortran'.
            
        writing_ic() -> None:
            Escreve os arquivos de condições iniciais para cada simulação no diretório 'data/input/fortran'.
    """
    
    list_of_simulation: Optional[List[str]] = field(default=None)

    __simulation_list: List[Itens] = field(init=False, repr=False)
    __input_fortran_path: str = field(init=False, repr=False)
    __log: Logger = field(init=False, repr=False, default=getLogger(__name__))

    def __post_init__(self) -> None:

        # Definindo lista que os objetos objetos selecionados da função simulation_list 
        #___________________________________________________________
        self.__simulation_list = simulation_list_manual_insert(self.list_of_simulation)
        #___________________________________________________________

        # Definindo caminho absoluto para o diretório 'data/input'
        #___________________________________________________________
        absollute_path = os.path.dirname(__file__)
        relative_path = '../../../../../../' + 'data/input/fortran'
        self.__input_fortran_path = os.path.abspath(os.path.join(absollute_path, relative_path))
        #___________________________________________________________

        self.__log.debug('Started')
    
    def writing_init(self) -> None:
        """
        Este método escreve o arquivo '__init__.sim' no diretório 'data/input/fortran'.
        O arquivo '__init__.sim' contém a lista de nomes das simulações que serão
        executadas pelo código Fortran.
        """

        path_init_sim = self.__input_fortran_path + '/' + '__init__.sim'
        
        with open(file=path_init_sim, mode='w') as file:
            for simulation in self.__simulation_list:
                file.write(f'{simulation.name} \n')
        
        self.__log.debug('Executed')
    

    def writing_config(self) -> None:
        """
        Este método escreve os arquivos de configuração para cada simulação
        <simulation_name*>.config no diretório 'data/input/fortran'.
        Cada arquivo de configuração contém as informações sobre o método numérico
        a ser utilizado, os parâmetros do método numérico e as unidades de
        conversão.
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
        Este método escreve os arquivos de condições iniciais para cada simulação
        <simulation_name*>.ic no diretório 'data/input/fortran'.
        Cada arquivo de condições iniciais contém as informações sobre o período
        de tempo a ser simulado e as condições iniciais de cada corpo do sistema
        solar.
        """
        for simulation in self.__simulation_list:
            path_simulation_ic = self.__input_fortran_path + '/' + simulation.name + '.ic'

            with open(file=path_simulation_ic, mode='w') as file:
                file.write(f'{simulation.domain.t0} {simulation.domain.tf} \n')

                for ic in simulation.initial_condition:
                    file.write(f'{ic.body} {ic.mass} {' '.join(str(coordinates) for coordinates in ic.s0)} {' '.join(str(coordinates) for coordinates in ic.v0)} \n')

        self.__log.debug('Executed')