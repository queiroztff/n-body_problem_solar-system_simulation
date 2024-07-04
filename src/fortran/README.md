# Subsistema Fortran

Este documento descreve o subsistema Fortran do projeto, abrangendo a compilação, execução, arquivos de entrada e saída (I/O) e o formato dos dados.

## Compilação do Código-Fonte (modo de desenvolvimento)

Para compilar o código-fonte Fortran, um ambiente Linux, e os pacotes **gfortran** e **make** são necessários.

1. **Compilação:** No diretório **src/fortran/**, execute o comando:
   ```bash
   make
   ```
   Este comando irá compilar o código-fonte e gerar um binário localizado em **build/fortran/bin/n-body.exe**.

2. **Execução:** O binário pode ser executado de duas maneiras:
   - Com **make run:** No diretório **src/fortran/**, execute o comando:
     ```bash
     make run
     ```
   - **Diretamente:** No diretório **build/fortran/bin/**, execute o comando:
     ```bash
     ./n-body.exe
     ```


## Execução via Container Docker (produção)
Para executar o subsistema Fortran em produção, utilize um contêiner Docker.

1. **Construção da Imagem Docker:** Na raiz do projeto, execute o comando:
   ```bash
   docker build -t fortran_subsystem src/fortran/
   ```
   Este comando irá criar uma imagem Docker com o nome `fortran_subsystem` a partir do Dockerfile em **src/fortran/**.

2. **Criação do Contêiner Docker:** Na raiz do projeto, execute o comando:
   ```bash
   docker container create \
   --name=n-body_simulation \
   --mount type=bind,source="$(pwd)"/data/input/fortran,target=/app/data/input/fortran \
   --mount type=bind,source="$(pwd)"/data/output,target=/app/data/output \
   fortran_subsystem
   ```
   Este comando irá criar um contêiner Docker com o nome `n-body_simulation` e montar os diretórios de entrada e saída do host no contêiner.

3. **Início do Contêiner Docker:** Execute o comando:
   ```bash
   docker container start n-body_simulation
   ```
   Este comando irá iniciar o contêiner Docker e executar o subsistema Fortran dentro dele.

## Arquivos de Entrada e Saı́da (i/o)

O subsistema Fortran utiliza arquivos de entrada e saída, para configurar as simulações e armazenar os resultados.

**Estrutura de Diretórios:**

```
.
├── src
│   ├── fortran
│   │   ├── lib/
│   │   ├── edo_nbody.f90
│   │   └── main.f90
│   ├── Dockerfile
│   ├── .dockerignore
│   └── Makefile
├── build
│   └── frotran
│       ├── bin
│       │   └── n-body.exe
│       ├── mod/
│       └── obj/
└── data
    ├── input
    │   └── fortran
    │       ├── __init__.sim
    │       ├── <simulation_name>.config
    │       ├── <simulation_name>.ic
    │       ├── .
    │       ├── .
    │       └── .
    └── output
        └── <simulation_name>
            ├── <body_name-1>.sob
            ├── <body_name-2>.sob
            ├── <body_name-3>.sob
            ├── .
            ├── .
            ├── .
            └── report.json

```
Ao executar o arquivo binário **n-body.exe** dentro do diretório **build/fortran/bin/** ou com `make run` no diretório **src/fortran/src/**, o programa principal irá procurar no diretório **data/input/fortran/** o arquivo **__init__.sim** e ler o mesmo. Este ficheiro contém o nome das simulações, as quais irão sevir como prefixo para o nome dos arquivos **\<simulation_name\>.config** e **\<simulation_name\>.ic**, os quais contém as configurações da simulação e as condições iniciais dos corpos envolvidos no problema. Após a leitura de todos os arquivos de entrada, o programa irá gerar os dados referente a solução do problema, os quais serão amarzenados no diretório **data/output/\<simulation_name\>/**.

### Arquivos de entrada

Localizados no diretório **data/input/fortran/**, os arquivos **__init__.sim**, **\<simulation_name\>.config** e **\<simulation_name\>.ic**. Contém o nome das simulações, as configurações do programa principal, as condições iniciais dos corpos envolvidos no problema e estão dispostos da seguinte forma:

* **\_\_init\_\_.sim** <br>
    Localizado em **data/input/fortran/**, este arquivo contém uma lista de nomes de simulações, que servirão como prefixo para os arquivos de configuração e condições iniciais. A ordem dos nomes no arquivo define a ordem de execução das simulações. <br>

    | Linha |\<registro\>|Descrição|
    |:------|:----------:|:--------|
    |1      |**simulation_name**|:**str** indica o prefixo do arquivo que contém as configurações e as condições iniciais dos corpos envolvidos no problema|
    |2      |**simulation_name-1**| ...|
    |3      |**simulation_name-2**| ...|
    |.<br>.<br>.|.<br>.<br>.| ...

* **\<simulation_name\>.config** <br> 
    Localizado em **data/input/fortran/**, este arquivo contém as configurações do programa principal para cada simulação.<br>

    | Linha |\<registro\>|Descrição|
    |:------|:----------:|:--------|
    |1      |**method_name**|:**str={rkdp, rkfb, rkfb7, rkvn}** indica o nome do método numérico a ser utilizado pela simulação|
    |2      |**eps**        |:**float** indica o delta entre dois valores consecutivos do resultado numérico da simulação, onde o resultado será escrito no arquivo de saída se e somente $\Delta \ge eps$|
    |3      |**tol**        |:**float** indica a tolerância do médodo numérico|
    |4      |**hmax hmin**  |:**float** indica o tamanho do passo maximo **hmax** e mínimo **hmin** do método numérico|
    |5      |**G_s**        |:**float** indica a constate gravitacional do sistema, ao qual deve estar na mesma unidades que as coondições iniciais|
    |6      |**distance_conversion_factor**|:**float** fator de conversão de distância|
    |7      |**mass_conversion_factor**|:**float** fator de conversão de massa|
    |8      |**time_conversion_factor**|:**float** fator de conversão de tempo|

* **\<simulation_name\>.ic** <br>
    Localizado em **data/input/fortran/**, este arquivo contém as condições iniciais dos corpos envolvidos na simulação.<br>

    | Linha |\<registro\>|Descrição|
    |:------|:----------:|:--------|
    |1      |$t_0$ $t_f$|:**float** indica o domínio em o problema será solucionado|
    |2      |**body_name_1** $m_1$ $x_1$ $y_1$ $z^*_1$ $vx_1$ $vy_1$ $vz^*_1$ |:**str** *:**float** Onde body_name_1 indica o nome do corpo,<br> $m_1$ a massa, $\vec{S}_0 = x_1\hat{e}_1 + y_1\hat{e}_2 + z^*_1\hat{e}_3$ a posição inicial,<br> e $\vec{V}_0 = vx_1\hat{e}_1 + vy_1\hat{e}_2 + vz^*_1\hat{e}_3$ a velocidade <br> do *corpo-1* em coordenadas cartesianas|
    |3      |**body_name_2**  $m_2$ $x_2$ $y_2$ $z^*_2$ $vx_2$ $vy_2$ $vz^*_2$|:**str** *:**float** indica o nome, a massa e ás condições iniciais do *corpo-2*|
    |.<br>.<br>.|.<br>.<br>. |...         |
    |n+1    |**body_name_n** $m_n$ $x_n$ $y_n$ $z^*_n$ $vx_n$ $vy_n$ $vz^*_n$|:**str** *:**float** indica o nome, a massa e ás condições iniciais do *n-ésimo corpo*|

    Table: \* No espaço bidimensional, estes registros não estarão presentes.

### Arquivos de saída

Os arquivos contidos em **data/output/<simulation_name>/**, possuem os resultados numéricos da solução do problema.

Os ficheiros estão dispostos da seguinte forma:

* **\<simulation_name-1\>.sob** <br>
    Contém a solução numérica do *corpo 1*, onde os registros estão dispostos da seguinte forma: <br>

    | Linha |\<registro\>|Descrição|
    |:------|:----------:|:--------|
    |1      |$t_0$ $x_0$ $y_0$ $z^*_0$ $vx_0$ $vy_0$ $vz^*_0$ $err\_S_0$ $err\_V_0$|...       |
    |.<br>.<br>.|.<br>.<br>.|         |
    |g      |$t_g$ $x_g$ $y_g$ $z^*_g$ $vx_g$ $vy_g$ $err\_S_g$ $err\_V_g$|:**float** Onde $\vec{S}_g = x_g\hat{e}_1 + y_g\hat{e}_2 + z^*_g\hat{e}_3$ <br> e $\vec{V}_g = vx_g\hat{e}_1 + vy_g\hat{e}_2 + vz^*_g\hat{e}_3$ <br> representa a posição e a velocidade vetorial do corpo no <br> instante $t_g$. Onde $err\_S_g$ $err\_V_g$ <br>representa o maior erro dentre as coordenadas da posição e da velocidade|
    |.<br>.<br>.|.<br>.<br>.|         |
    |n      |$t_n$ $x_n$ $y_n$ $z^*_n$ $vx_n$ $vy_n$ $err\_S_n$ $err\_V_n$|...      |

    Table: \* No espaço bidimensional, estes registros não estarão presentes.


* **\<simulation_name-2\>.sob** <br>
    Contém a solução numérica do *corpo 2*, onde os registros estão dispostos da mesma forma que o aterior.<br>.<br>.<br>.

* **\<simulation_name-2\>.sob** <br>
    Contém a solução numérica do *corpo n*, onde os registros estão dispostos da mesma forma que os demais.

* **report.json** <br>
    Localizado em **data/output/<simulation_name>/**, este arquivo contém informações gerais sobre a simulação.<br>
    Esse arquivo possui o seguite esquema:

    ```json
    {
        "runtime" : float,
        "simulation" : {
            "name" : str,
                "method" : {
                    "name" : \rkdp | rkfb | rkfb7 | rkvn\,
                    "eps" : float,
                    "tol" : float,
                    "step" : {
                        "hmin" : float,
                        "hmax" : float
                    }
                },
            "domain" : {
                "t0" : float,
                "tf" : float
                },
            "dms" : int,
            "nbody" : int,
            "state" : [
                {
                    "body" : str,
                    "mass" : float,
                    "local_storage" : "float"
                },
                .
                .
                .
                {
                    "body" : str,
                    "mass" : float,
                    "local_storage" : "float"
                }
            ]
        }
    }
    ```