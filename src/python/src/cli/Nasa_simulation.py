import argparse
from logging import getLogger
from writing_data.output import NasaSimulation

def cli_nasa_simulation() -> None:
    """
    Cria uma interface de linha de comando (CLI) usando argparse para executar o método
    'writing_simulation' da classe 'NasaSimulation'.

    Esta CLI permite que o usuário especifique uma ou mais simulações a serem escritas,
    utilizando o arquivo JSON "data/input/python/NASA_simulation_config.json" como fonte de
    configuração. Os dados das simulações são escritos em arquivos .sob, organizados em
    subpastas dentro do diretório "data/output/<simulation_name>/".

    Args:
        simulation (str): execulta a simulação.
        -l, --list (list, optional): lista de nomes de simulações a serem escritas.
            Se não for especificado, todas as simulações serão escritas
    """

    log = getLogger(__name__)

    parse = argparse.ArgumentParser(prog = 'NasaSimulation',
                                    description = 'Escrever os dados de uma simulação proveniente ' 
                                                  'da base de dados da Nasa, em arquivos .sob' ,
                                    epilog = 'Este CLI utiliza o arquivo JSON "data/input/python/NASA_simulation_config.json" ' 
                                             'que contém uma lista de simulações. Ele escreve os dados dessas simulações, '
                                             'provenientes da base de dados da NASA, em arquivos .sob. Localizados no caminho '
                                             'data/output/<simulation_name>/ com  em subpastas com os nomes dos corpos')
    
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

    nasa_simulation = NasaSimulation(list_of_simulation = args.list)
    nasa_simulation.writing_simulation()

    log.debug('Executed')