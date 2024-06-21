import logging
import os

#Configurando o caminho onde o arquivo de log 'test.log' será escrito
#___________________________________________________________
absollute_path = os.path.dirname(__file__)
relative_path = '../test.log'
log_file = os.path.abspath(os.path.join(absollute_path, relative_path))
#___________________________________________________________

#Configurando o arquivo de logging
#___________________________________________________________
if (__name__ == 'conftest'):
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        format='%(asctime)s %(name)s %(levelname)s %(funcName)s %(message)s',
        level=logging.DEBUG)
#___________________________________________________________

#Inicializando logging
#___________________________________________________________
log = logging.getLogger(__name__)
log.info("Started")
#___________________________________________________________