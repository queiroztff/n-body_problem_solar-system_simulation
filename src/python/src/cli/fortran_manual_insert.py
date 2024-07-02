import argparse
from logging import getLogger
from use_cases.execute_binary import BinaryNbody
from writing_data.input import FortranManualInsert

def cli_fortran_manual_insert() -> None:
    """
    Cria uma interface de linha de comando (CLI) usando argparse para gerar os arquivos de entrada
    para a simulação Fortran e executar o binário n-body.exe.

    Esta CLI utiliza um arquivo JSON localizado em "data/input/python/fortran_simulation_manual_insert_initial_condition.json"
    que contém uma lista de simulações. Cada simulação define informações como o método numérico,
    condições iniciais dos corpos e o período de tempo a ser simulado.

    A CLI permite que o usuário especifique uma ou mais simulações a serem executadas.
    Se nenhuma simulação for especificada, todas as simulações definidas no arquivo JSON serão executadas.

    Args:
        simulation (str): execulta a simualação.
        -l, --list (list, optional): Lista de nomes de simulações a serem executadas.
            Se não for especificado, todas as simulações serão executadas.
    """

    log = getLogger(__name__)

    parse = argparse.ArgumentParser(prog = 'FortranManualInsert',
                                    description = 'Cria os arquivos de entradas para a simulação fortran ' 
                                                  'e execulta o binário n-body.exe',
                                    epilog = 'Este cli responsável por escrever os arquivos de entrada para o código Fortran, '
                                             'que simula o problema de N-corpos e executa o binário n-body.exe. '
                                             'Os arquivos de entrada são gerados a partir de uma lista de simulações '
                                             'definidas em um arquivo JSON localizado no caminho ' 
                                             'data/input/python/fortran_simulation_manual_insert_initial_condition.json .'
                                             'Cada simulação contém informações sobre '
                                             'o método numérico a ser utilizado, as condições iniciais dos corpos '
                                             'e o período de tempo a ser simulado.')

    parse.add_argument('simulation', 
                       help='Execulta a simulação')
    
    parse.add_argument('-l',
                       '--list',
                       action = 'store',
                       nargs = '+',
                       default = None,
                       type = str,
                       help = 'Lista de nomes de simulações a serem escritas. ' 
                              'Se não for especificado, todas as simulações serão escritas.')
    
    args = parse.parse_args()

    fortran_manual_insert = FortranManualInsert(list_of_simulation = args.list)
    execute_binary = BinaryNbody()

    fortran_manual_insert.writing_init()
    fortran_manual_insert.writing_config()
    fortran_manual_insert.writing_ic()
    execute_binary.exe()

    log.debug('Executed')

