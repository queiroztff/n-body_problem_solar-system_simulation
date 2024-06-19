FROM fedora:40

# Instalando as ferramentas necessárias para a execução do código fortran
RUN dnf update -y && \
    dnf install -y gcc-gfortran-14.1.1 && \
    dnf install -y make-4.4.1 && \
    dnf clean all 

# Definindo o diretório de trabalho
WORKDIR /app

# Criando árvore de diretório
RUN mkdir -p build/fortran/{bin,mod,obj} && \
    mkdir -p src/fortran

# Definindo volumes de input e output
VOLUME /app/data/input/fortran
VOLUME /app/data/output

# Copiando o código-fonte para o contêiner
COPY . /app/src/fortran/

# Mudando dirtório de trablho
WORKDIR /app/src/fortran/

# Compilando código Fortran
RUN make

# Comando para executar o binário Fortran
ENTRYPOINT [ "sh", "-c" ]
CMD [ "make run" ]

