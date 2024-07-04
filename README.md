# Simulação do Problema n-corpos: Sistema Solar

Este repositório contém o código-fonte para uma simulação do problema de n-corpos, com foco na simulação do Sistema Solar. O projeto é dividido em dois subsistemas: Fortran e Python. O subsistema Fortran implementa o núcleo da simulação, utilizando métodos numéricos para integrar as equações de movimento dos corpos celestes. O subsistema Python fornece uma interface de linha de comando (CLI) para configurar e executar as simulações, além de ferramentas para processar os dados de saída.

## Execução via Container Docker
Para executar a simulação utilizando um container Docker, é necessário um ambiente Linux com o pacote Docker instalado. O processo de execução é dividido em duas etapas:

1. **Construção da Imagem Docker:** 
    Na raiz do projeto, execute o seguinte comando para construir a imagem Docker:

    ```bash
    docker-compose build
    ```

    Este comando irá utilizar o arquivo docker-compose.yml para construir a imagem Docker, que contém as dependências necessárias para executar o projeto.

2. **Criação e Execução do Contêiner Docker:** 
    Após a construção da imagem, execute o seguinte comando para criar e executar o contêiner Docker:

    ```bash
    docker-compose run python_subsytem
    ```
    Este comando irá iniciar um contêiner Docker baseado na imagem construída anteriormente, utilizando o serviço python_subsytem definido no arquivo docker-compose.yml. O contêiner irá executar o subsistema Python, que fornece a interface de linha de comando (CLI) para configurar e executar as simulações.

## CLI (Interface de Linha de Comando)

O subsistema python fornece uma interface de linha de comando (CLI) para executar simulações. A CLI oferece três comandos principais:

* **Inserção manual de condições iniciais no subsistema fortran**

    ```python
    fmi [-h] [-l --list LIST [LIST ...]] simulation

    Cria os arquivos de entradas para a simulação fortran e execulta o binário n-body.exe

    positional arguments:
    simulation            Execulta a simulação

    options:
    -h, --help            mostra mensagem de ajuda
    -l , --list LIST [LIST ...] Lista de nomes de simulações a serem escritas. Se não for especificado, todas as simulações serão escritas.
    ```

    Este **cli** responsável por escrever os arquivos de entrada para o subsistema Fortran, que simula o problema de n-corpos atraves de o determinado método numerico ao executar o binário n-body.exe. Os arquivos de entrada são gerados a partir de uma lista de simulações definidas em um arquivo JSON localizado no caminho `data/input/python/fortran_simulation_manual_insert_initial_condition.json` . Cada simulação contém informações sobre o método numérico a ser utilizado, as condições iniciais dos corpos, o período de tempo a ser simulado e as configurações do método númerico. <br>

* **Inserção de condições iniciais provenientes da base de dados da Nasa no subsistema fortran**
    ```python
    fni [-h] [-l --list LIST [LIST ...]] simulation

    Cria os arquivos de entradas para a simulação fortran e execulta o binário n-body.exe

    positional arguments:
    simulation            Execulta a simulação

    options:
    -h, --help            mostra mensagem de ajuda
    -l , --list LIST [LIST ...] Lista de nomes de simulações a serem escritas. Se não for especificado, todas as simulações serão escritas.
    ```

    Este **cli** responsável por escrever os arquivos de entrada para o código Fortran, que simula o problema de n-corpos atraves de o determinado método numerico ao executar o binário n-body.exe. Os arquivos de entrada são gerados a partir de uma lista de simulações onde as condições iniais são provenientes da base de dados da Nasa, as quais são definidas em um arquivo JSON localizado no caminho `data/input/python/fortran_simulation_with_NASA_initial_condition_config.json` .Cada simulação contém informações sobre o método numérico a ser utilizado, as condições iniciais dos corpos e o período de tempo a ser simulado.

* **Simulação provenientes da base de dados da Nasa**
    ```python
    ns [-h] [-l --list LIST [LIST ...]] simulation

    Cria os arquivos de entradas para a simulação fortran e execulta o binário n-body.exe

    positional arguments:
    simulation            Execulta a simulação

    options:
    -h, --help            mostra mensagem de ajuda
    -l , --list LIST [LIST ...] Lista de nomes de simulações a serem escritas. Se não for especificado, todas as simulações serão escritas.
    ```
    Este **cli** utiliza o arquivo JSON `data/input/python/NASA_simulation_config.json` que contém uma lista de simulações. Ele escreve os dados dessas simulações, provenientes da base de dados da NASA, em arquivos .sob. Localizados no caminho data/output/<simulation_name>/ com em subpastas com os nomes dos corpos


## Arquivos de Entrada e Saı́da (i/o)

O subsistema Fortran utiliza arquivos de entrada e saída, para configurar as simulações e armazenar os resultados.

**Estrutura de Diretórios:**

```
.
└── .
    ├── src
    │   ├── fortran/
    │   └── python
    │       ├── src/
    │       │   ├── .
    │       │   ├── .
    │       │   ├── .
    │       │   └── main.py
    │       ├── .dockerignore
    │       ├── Dockerfile
    │       └── pyproject.toml
    ├── build
    │   ├── fortran
    │   │   ├── bin
    │   │   │   └── n-body.exe
    │   │   ├── mod/
    │   │   └── obj/
    │   └── python
    │       └── .venv/
    └── data
        ├── input
        │   ├── fortran/
        │   └── python
        │       ├── fortran_simulation_manual_insert_initial_condition.json
        │       ├── fortran_simulation_with_NASA_initial_condition_config.json
        │       └── NASA_simulation_config.json
        ├── output
        │   ├── <simulation_name>
        │   ├── <body_name-1>.sob
        │   ├── <body_name-2>.sob
        │   ├── <body_name-3>.sob
        │   ├── .
        │   ├── .
        │   ├── .
        │   └── report.json
        └── logs
            └── python
                └── Logs
```

### Arquivos de entrada

Localizados no diretório **data/input/python/**, os arquivos **fortran_simulation_manual_insert_initial_condition.json** **fortran_simulation_with_NASA_initial_condition_config.json** e  **NASA_simulation_config.json**, são inputs para execução dos cli `fmi`, `fni` e `ns`. Este arquivos possuem o seguinte esquema.  

* **fortran_simulation_manual_insert_initial_condition.json** <br>
    ```json
    {
        "simulation":[
            {
                "name" : str,
                "method" : {
                    "name" : rkdp | rkfb | rkfb7 | rkvn, 
                    "eps" : float,
                    "tol" : float,
                    "step" : {
                        "hmin" : float,
                        "hmax" : float
                    },
                    "G" : float,
                    "conversion_factor" : {
                        "distance" : float,
                        "mass" : float,
                        "time" : float
                    }
                },
                "domain" : {
                    "t0" : float,
                    "tf" : float
                },
                "initial_condition" : [
                    {
                        "body" : str,
                        "mass" : float ,
                        "s0" : [ float, float, float*],
                        "v0" : [float, float, float*]
                    },
                    .
                    .
                    .
                    {
                        "body" : str,
                        "mass" : float ,
                        "s0" : [ float, float, float*],
                        "v0" : [float, float, float*]
                    },
                ]    
            }
            .
            .
            .
            {
                "name" : str, 
                .
                .
                .  
            }
        ]
    }
    ```

    Descrição dos atributos: <br>

    * **simulation**: Lista de objetos que contém informações sobre cada simulação, incluindo:
        * **name: str**: nome da simulação

        * **method**: Objeto que contém informações sobre o método numérico utilizado na simulação, incluindo:
            * **name: str={rkdp | rkfb | rkfb7 | rkvn}**: nome do método numérico, onde cada abrviação representa *rkdp = Runge-Kutta-Dormand-Prince*, *rkfb = Runge-kutta-Fehlberg*, *rkfb7 = Runge-kutta-Fehlberg-7-ordem*, *rkvn = Runge-kutta-Verner*
            * **eps: float**: tolerância do método numérico.
            * **tol: float**: tolerância do método numérico.

            * **step**: Objeto que contém informações sobre o passo de integração, incluindo:
                * **hmin: float**: passo de integração mínimo.
                * **hmax: float**: passo de integração máximo.
            * **G: float**: Constante gravitacional

            * **conversion_factor**: Objeto que contém informações sobre os fatores de conversão utilizados na simulação, incluindo:
                * **distance: float**: fator de conversão para distância.
                * **mass: float**: fator de conversão para massa.
                * **time: float**: fator de conversão para tempo.

        * **domain**: Objeto que contém informações sobre o domínio da simulação, incluindo:
            * **t0: float**: tempo inicial da simulação.
            * **tf: float**: tempo final da simulação.
        
        * **initial_condition**: Lista de objetos que contém informações sobre o estado inicial de cada corpo na simulação, incluindo:
            * **body: str**: nome do corpo.
            * **mass: str**: massa do corpo.
            * **s0: [float, float, *float]**: coordenadas que representa a posição inicial do corpo *(caso o sistema seja bidimencional não se faz presente).
            * **v0:[float, float, *float]**: coordenadas que representa a velocidade inicial do corpo *(caso o sistema seja bidimencional não se faz presente).

    Exemplo:

    ```json
    {
        "simulation":[
            {
                "name" : "figure_8",
                "method" : {
                    "name" : "rkdp",
                    "eps" : 1.000E-2,
                    "tol" : 1.000E-15,
                    "step" : {
                        "hmin" : 1.000E-8,
                        "hmax" : 1.000E-5
                    },
                    "G" : 1,
                    "conversion_factor" : {
                        "distance" : 1,
                        "mass" : 1,
                        "time" : 1
                    }
                },
                "domain" : {
                    "t0" : 0.00000000,
                    "tf" : 6.32444900
                },
                "initial_condition" : [
                    {
                        "body" : "pm_01",
                        "mass" : 1.0 ,
                        "s0" : [ -1.0, 0.0],
                        "v0" : [0.347111, 0.532728]
                    },
                    {
                        "body" : "pm_02",
                        "mass" : 1.0,
                        "s0" : [1.0, 0.0],
                        "v0" : [0.347111, 0.532728]
                    },
                    {
                        "body" : "pm_03",
                        "mass" : 1.0,
                        "s0" : [0.0, 0.0],
                        "v0" : [-0.694222, -1.065456]
                    }
                ]    
            }
        ]
    }
    ```
    <br>
* **fortran_simulation_with_NASA_initial_condition_config.json** <br>

    ```json
    {
        "simulation":[
            {
                "name":str,

                "body":{
                    "ast":Optional[List[str]],
                    "com":Optional[List[str]],
                    "pln":Optional[List[str]],
                    "sat":Optional[List[str]]
                },

                "calendar":{
                    "model":"cd"|"jd",
                    "start_time":str|float,
                    "stop_time":str|float
                },

                "center":"500@0",
                "out_units": "KM-S" | "AU-D" | "KM-D",
            
                "relative_time":bool,

                "method" : {
                    "name" : "rkdp" | "rkfb" | "rkfb7" | "rkvn", 
                    "eps" : float,
                    "tol" : float,
                    "step" : {
                        "hmin" : float,
                        "hmax" : float
                    },
                    "G" : float,
                    "conversion_factor" : {
                        "distance" : float,
                        "mass" : float,
                        "time" : float
                    }
                }
            },
            .
            .
            .
            {
                "name": str,
                .
                .
                .
            }
        ]
    }
    ```

    Descrição dos atributos: <br>

    * **simulation**: Lista de objetos que contém informações sobre cada simulação, incluindo:

        * **name: str**: nome da simulação

        * **body**: Objeto que contém informações sobre os corpos que serão simulados:
            * **ast: Optional[List[str]]**: lista de strings que contenha o nome dos asteroides que serão simulados.
            * **com: Optional[List[str]]**: lista de strings que contenha o nome os cometas que serão simulados.
            * **pln: Optional[List[str]]**: lista de strings que contenha o nome os planetas que serão simulados.
            * **sat: Optional[List[str]]**: lista de strings que contenha o nome os satélites que serão simulados.
        
        * **calendar**: Objeto que contém informações sobre o calendário utilizado na simulação:
            * **model: str={cd | jd}**: modelo de calendário utilizado, onde *cd* representa *calendário* e *jd* representa *calendário juliano*, 
            * **start_time: str|float**: tempo inicial da simulação a ser realizada pelo subsistema fortran.<br>
                ```
                date : str 
                String que receberá uma data/hora do calendário gregroriano
                Onde o formato desta entrada será da forma:

                Calendar format:

                tipo      Formato                                  Significado      
                1     YYYY-MM-DD.DDDDD                   ano, mês, dias com casa decimais  (casas decimais sào opcionais)
                2     YYYY-MM-DD hh:mm.m                 ano, mês, dias, horas e minutos com casa decimais (casas decimais sào opcionais)
                3     YYYY-MM-DD hh:mm:ss.s              ano, mês, dias, horas, minutos e segundos com casa decimais (casas decimais sào opcionais)
                
                O mês pode ser especificado usando as abreviações de mês de 3 caracteres , conforme definido nos EUA:
                (case insensitive) (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec) ou (01, 02, 03, 05, 06, 
                07, 08, 09, 10, 11, 12).

                date : float
                    Float que receberá o número do dia juliano
                    Onde o formato desta entrada séra da forma:

                    Julian Day Number:
                
                    {integer}.{integer}
                ```
            * **stop_time: str|float**: tempo final da simulação a ser realizada pelo subsistema fortran
        
        * **center: str = 500@0**: origem do sistema de coordenadas (500@0 representa o centro de massas do sistema solar), para mais informações consulte [https://ssd.jpl.nasa.gov/horizons/manual.html#center](https://ssd.jpl.nasa.gov/horizons/manual.html#center)
        * **out_units: str={KM-S | AU-D | KM-D}**: unidades  de distância e tempo suportadas, sabendo que a massa sempre estará em kg.
        * **relative_time: bool**: tempo relativo, se *true* t0 = 0.0 e tf = stop_time - start_time  caso contrario *false* t0 = start_time e tf = stop_time.

        * **method**: Objeto que contém informações sobre o método numérico utilizado na simulação, incluindo:
            * **name: str={rkdp | rkfb | rkfb7 | rkvn}**: nome do método numérico, onde cada abrviação representa *rkdp = Runge-Kutta-Dormand-Prince*, *rkfb = Runge-kutta-Fehlberg*, *rkfb7 = Runge-kutta-Fehlberg-7-ordem*, *rkvn = Runge-kutta-Verner*
            * **eps: float**: tolerância do método numérico.
            * **tol: float**: tolerância do método numérico.

            * **step**: Objeto que contém informações sobre o passo de integração, incluindo:
                * **hmin: float**: passo de integração mínimo.
                * **hmax: float**: passo de integração máximo.

            * **G: float**: Constante gravitacional

            * **conversion_factor**: Objeto que contém informações sobre os fatores de conversão utilizados na simulação, incluindo:
                * **distance: float**: fator de conversão para distância.
                * **mass: float**: fator de conversão para massa.
                * **time: float**: fator de conversão para tempo.
    
    Exemplo:

    ```json
    {
        "simulation":[
            {
                "name":"Solar_System",

                "body":{
                    "pln":["Sun", "Mercury", "Venus", 
                    "Earth", "Mars", "Jupiter", 
                    "Saturn", "Uranus", "Neptune"],
            
                    "sat":["Moon"]
                },

                "calendar":{
                    "model":"cd",
                    "start_time":"2000-01-01 00:00",
                    "stop_time": "2001-01-01 00:00"
                },

                "center":"500@0",
                "step_size":"3d",
                "out_units":"KM-D",
            
                "relative_time":true,

                "method" : {
                    "name" : "rkdp",
                    "eps" : 1.000E-2,
                    "tol" : 1.000E-15,
                    "step" : {
                        "hmin" : 1.000E-8,
                        "hmax" : 1.000E-5
                    },
                    "G" : 4.982339E-10,
                    "conversion_factor" : {
                        "distance" : 6.685E-9,
                        "mass" : 5.972E24,
                        "time" : 1
                    }

                }
            }
        ]
    }
    ```
    <br>

* **NASA_simulation_config.json**

    ```json
    {
        "simulation" : [
            {    Descrição dos atributos: <br>
                "name":str,

                "body":{
                    "ast":Optional[List[str]],
                    "com":Optional[List[str]],
                    "pln":Optional[List[str]],
                    "sat":Optional[List[str]]
                },

                "calendar":{
                    "model":"cd"|"jd",
                    "start_time":str|float,
                    "stop_time":str|float
                },

                "center":"500@0",
                "out_units":"KM-S" | "AU-D" | "KM-D",
                "step_size" : str,            
                "relative_time":bool,
            },
            .
            .
            .
            {
                "name": str
                .
                .
                .
            }
        ]
    }
    ```

    Descrição dos atributos: <br>

    * **simulation**: Lista de objetos que contém informações sobre cada simulação, incluindo:

        * **name: str**: nome da simulação

        * **body**: Objeto que contém informações sobre os corpos que serão simulados:
            * **ast: Optional[List[str]]**: lista de strings que contenha o nome dos asteroides que serão simulados.
            * **com: Optional[List[str]]**: lista de strings que contenha o nome os cometas que serão simulados.
            * **pln: Optional[List[str]]**: lista de strings que contenha o nome os planetas que serão simulados.
            * **sat: Optional[List[str]]**: lista de strings que contenha o nome os satélites que serão simulados.
        
        * **calendar**: Objeto que contém informações sobre o calendário utilizado na simulação:
            * **model: str={cd | jd}**: modelo de calendário utilizado, onde *cd* representa *calendário* e *jd* representa *calendário juliano*, 
            * **start_time: str|float**: tempo inicial da simulação.<br>
                ```
                date : str 
                String que receberá uma data/hora do calendário gregroriano
                Onde o formato desta entrada será da forma:

                Calendar format:

                tipo      Formato                                  Significado      
                1     YYYY-MM-DD.DDDDD                   ano, mês, dias com casa decimais  (casas decimais sào opcionais)
                2     YYYY-MM-DD hh:mm.m                 ano, mês, dias, horas e minutos com casa decimais (casas decimais sào opcionais)
                3     YYYY-MM-DD hh:mm:ss.s              ano, mês, dias, horas, minutos e segundos com casa decimais (casas decimais sào opcionais)
                
                O mês pode ser especificado usando as abreviações de mês de 3 caracteres , conforme definido nos EUA:
                (case insensitive) (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec) ou (01, 02, 03, 05, 06, 
                07, 08, 09, 10, 11, 12).

                date : float
                    Float que receberá o número do dia juliano
                    Onde o formato desta entrada séra da forma:

                    Julian Day Number:
                
                    {integer}.{integer}
                ```
            * **stop_time: str|float**: tempo final da simulação
        
        * **center: str = 500@0**: origem do sistema de coordenadas (500@0 representa o centro de massas do sistema solar), para mais informações consulte [https://ssd.jpl.nasa.gov/horizons/manual.html#center](https://ssd.jpl.nasa.gov/horizons/manual.html#center)
        * **out_units: str={KM-S | AU-D | KM-D}**: unidades  de distância e tempo suportadas, sabendo que a massa sempre estará em kg.
        * **step_size: str** : especifica o delta entre dois pontos de tempo consecutivos, para mais informções consulte o link [https://ssd-api.jpl.nasa.gov/doc/horizons.html#stepping](https://ssd-api.jpl.nasa.gov/doc/horizons.html#stepping)
        * **relative_time: bool**: tempo relativo, se *true* t0 = 0.0 e tf = stop_time - start_time  caso contrario *false* t0 = start_time e tf = stop_time.
    
    Exemplo:

    ```json
    {
        "simulation" : [
            {   
                "name" : "real_simulation",
                "body" : {
                    "pln" : ["Sun", "Mercury", "Venus", 
                    "Earth", "Mars", "Jupiter", 
                    "Saturn", "Uranus", "Neptune"],
            
                    "sat" : ["Moon"]
                },
                "calendar" : {
                    "model" : "cd",
                    "start_time" : "2000-01-01 00:00",
                    "stop_time" : "2001-01-01 00:00"
                },
                "center" : "500@0",
                "step_size" : "3d",
                "out_units" : "KM-D",
            
                "relative_time" : true
            }
        ]
    }
    ```

### Arquivos de saída

Os arquivos contidos em **data/output/<simulation_name>/**, possuem os resultados numéricos provenientes da simulação execultada pelo **subsistema fortran** ou da base de dados da **Nasa**.

Os ficheiros estão dispostos da seguinte forma:

* **\<simulation_name-1\>.sob** <br>
    Contém a solução numérica do *corpo 1*, onde os registros estão dispostos da seguinte forma: <br>

    | Linha |\<registro\>|Descrição|
    |:------|:----------:|:--------|
    |1      |$t_0$ $x_0$ $y_0$ $z^*_0$ $vx_0$ $vy_0$ $vz^*_0$ $err\_S_0$ $err\_V_0$|...       |
    |.<br>.<br>.|.<br>.<br>.|         |
    |g      |$t_g$ $x_g$ $y_g$ $z^*_g$ $vx_g$ $vy_g$ $err\_S_g$ $err\_V_g$|:**float** Onde $\vec{S}_g = x_g\hat{e}_1 + y_g\hat{e}_2 + z^*_g\hat{e}_3$ <br> e $\vec{V}_g = vx_g\hat{e}_1 + vy_g\hat{e}_2 + vz^*_g\hat{e}_3$ <br> representa a posição e a velocidade vetorial do corpo    Localizado em **data/output/<simulation_name>/**, este arquivo contém informações gerais sobre a simulação.
    Esse arquivo possui o seguite esquema: no <br> instante $t_g$. Onde $err\_S_g$ $err\_V_g$ <br>representa o maior erro dentre as coordenadas da posição e da velocidade|
    |.<br>.<br>.|.<br>.<br>.|         |
    |n      |$t_n$ $x_n$ $y_n$ $z^*_n$ $vx_n$ $vy_n$ $err\_S_n$ $err\_V_n$|...      |

    Table: \* No espaço bidimensional, estes registros não estarão presentes.


* **\<simulation_name-2\>.sob** <br>
    Contém a solução numérica do *corpo 2*, onde os registros estão dispostos da mesma forma que o aterior.<br>.<br>.<br>.

* **\<simulation_name-2\>.sob** <br>
    Contém a solução numérica do *corpo n*, onde os registros estão dispostos da mesma forma que os demais.

* **report.json** <br>
    Localizado em **data/output/<simulation_name>/**, este arquivo contém informações gerais sobre a simulação.
    Esse arquivo possui o seguite esquema:<br>
    ```json
    {
        "runtime" : float,
        "simulation" : {
            "name" : str,
                "method" : {
                    "name" : rkdp | rkfb | rkfb7 | rkvn,
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
                    "local_storage" : str
                },
                .
                .
                .
                {
                    "body" : str,
                    "mass" : float,
                    "local_storage" : str
                }
            ]
        }
    }
    ```

    Descrição dos atributos: <br>

    * **runtime: float**: tempo de execução da simulação em segundos.
    * **simulation**: Objeto que contém informações sobre a simulação, incluindo:

        * **name: float**: nome da simulação.

        * **method**: Objeto que contém informações sobre o método numérico utilizado na simulação, incluindo:
            * **name: str={rkdp | rkfb | rkfb7 | rkvn}**: nome do método numérico, onde cada abrviação representa *rkdp = Runge-Kutta-Dormand-Prince*, *rkfb = Runge-kutta-Fehlberg*, *rkfb7 = Runge-kutta-Fehlberg-7-ordem*, *rkvn = Runge-kutta-Verner*
            * **eps: float**: tolerância do método numérico.
            * **tol: float**: tolerância do método numérico.
            * **step**: Objeto que contém informações sobre o passo de integração, incluindo:
                * **hmin: float**: passo de integração mínimo.
                * **hmax: float**: passo de integração máximo.
            
        * **domain**: Objeto que contém informações sobre o domínio da simulação, incluindo:
            * **t0: float**: tempo inicial da simulação.
            * **tf: float**: tempo final da simulação.
        
        * **dms: float**: dimensão do espaço da simulação (2D ou 3D).
        * **nbody: int**: número de corpos na simulação.

        * **state**: Lista de objetos que contém informações sobre o estado inicial de cada corpo na simulação, incluindo:
            * **body: str**: nome do corpo.
            * **mass: float**: massa do corpo.
            * **local_storag: str**: um valor float que representa o estado inicial do corpo.


