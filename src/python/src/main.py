import logging
import os
from cli import cli_fortran_manual_insert
from cli import cli_fortran_nasa_insert
from cli import cli_nasa_simulation

#Configurando o caminho onde o arquivo de log será escrito
#___________________________________________________________
absollute_path = os.path.dirname(__file__)
relative_path = '../../../' + 'logs/python/' + 'Log'
log_file = os.path.abspath(os.path.join(absollute_path, relative_path))

#Configurando o arquivo de logging

logging.basicConfig(
    filename=log_file,
    filemode='w',
    format='%(asctime)s %(name)s %(levelname)s %(funcName)s %(message)s',
    level=logging.DEBUG)
#___________________________________________________________

def Nasa_Simulation() -> None:
    cli_nasa_simulation()


def Fortran_manual_insert() -> None:
    cli_fortran_manual_insert()

def Fortran_Nasa_insert() -> None:
    cli_fortran_nasa_insert()
