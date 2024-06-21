import os
import subprocess
from logging import Logger, getLogger

class BinaryNbody:
    """
    Esta classe tem por objetivo execultar o binário n-body.exe

    Methods
    -------
    exe() -> None
        este método executa um binário n-body.exe localizado no caminho
        build/fortran/bin/n-body.exe relativo a raiz do sistema, caso não seja possível
        a execução um erro é levantado
    """

    def __init__(self) -> None:
        self.__log: Logger = getLogger(__name__)

        self.__log.debug('Started')

    def exe(self) -> None:
        """
        Este método execulta o binário n-body.exe
        """

        absollute_path = os.path.dirname(__file__)
        relative_path_bin_folder = '../../../../../' + 'build/fortran/bin'
        relative_path_binary_file = '../../../../../' + 'build/fortran/bin/n-body.exe'

        bin_folder = os.path.abspath(os.path.join(absollute_path, relative_path_bin_folder))
        bin_file = os.path.abspath(os.path.join(absollute_path, relative_path_binary_file))

        try:
            subprocess.run(args=f'cd {bin_folder} && {bin_file}', 
                           shell=True, 
                           check=True, 
                           capture_output=True,
                           universal_newlines=True)
            
            self.__log.debug('Executed')

        except subprocess.CalledProcessError as e:
            message = f'''
            Houve um erro ao executar o binário n-body.exe 
            localizado no caminho fortran/bin/n-body.exe relativo a raiz do sistema
            Error = {e.stderr}
            '''
            self.__log.error(message)
            raise(Exception(message))