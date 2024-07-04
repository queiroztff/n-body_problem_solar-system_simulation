FROM fedora:40

# Instalando as ferramentas necessárias para a execução do código python e o binário gerado pelo compilador gfortran
RUN dnf install -y python3.12 && \
    dnf install -y python3.12-pip && \
    dnf install -y libgfortran-14.1.1 && \
    dnf clean all 

# Definindo o diretório de trabalho
WORKDIR /app

# Definindo volumes de input e output e logs
VOLUME /app/data/input/fortran
VOLUME /app/data/input/python
VOLUME /app/data/output
VOLUME /app/logs/python

# Copiando o código-fonte python para o contêiner
COPY  . /app/src/python/

# Copiando binário gerado gerado pelo subsystema fortran
COPY --from=fortran_subsystem /app/build/fortran/bin/n-body.exe /app/build/fortran/bin/

# Mudando dirtório de trablho
WORKDIR /app/src/python/

RUN pip install --editable .