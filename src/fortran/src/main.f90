!Programa principal

!===========================================================
program n_body_problem

    use dormand_prince
    use verner
    use fehlberg
    use fehlberg7
    use edo_nbody
    use sol_edo_o2_rk
    use, intrinsic :: iso_fortran_env, only : stdin=>input_unit, &
                                              ioend=>iostat_end, &
                                              ioeor=>iostat_eor

    implicit none

        call exe_all_simutions()
        
    stop

contains

    subroutine number_of_lines_in_a_file(file, &
                                         nlines)
        !! Esta subroutina averigua a existencia de um arquivo 'file'
        !! e conta o número de linhas 'nlines' que este arquivo possui

        character(len=*), intent(in) :: file
        integer, intent(out) :: nlines
        integer :: nline
        integer :: iostat
        logical :: exist_file

            nline = 0

            inquire(file=file, exist=exist_file)
            if(exist_file) then
                open(unit=stdin, file=file, action='READ', form='FORMATTED', status='OLD', err=10)
            else 
                print *, "ERRO FATAL no Módulo = main"
                print *, "Arquivo de configuração ", file, " inexistente"
                print *, "Impossível continuar com a execução do programa"
                stop
            end if

            do
                read(unit=stdin, fmt=*, iostat=iostat)

                if(iostat == ioend) then
                    rewind(unit=stdin, err=11)
                    exit
                else if(iostat /= 0) then
                    print *, "Um erro ocorreu na leitura do arquivo ", file
                    stop
                else 
                    nline = nline + 1
                end if
            end do

            close(unit=stdin, status='KEEP', err=12)

            nlines = nline
    
        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", file
        stop
        
        11 print *, "Houve um erro no rebobinamento do arquivo ", file
        stop

        12 print *, "Houve um erro ao fechar o arquivo ", file
        stop

        999 continue

    end subroutine number_of_lines_in_a_file

    subroutine maximum_number_of_columns_in_a_file(file, &
                                                   ncolumns)
        !! Esta subroutina averigua a existencia de um arquivo 'file'
        !! e conta o número máximo de colunas 'ncolumns' que este arquivo possui

        character(len=*), intent(in) :: file
        integer, intent(out) :: ncolumns
        character(len=1028) :: line 
        integer :: ncolumn, maxncolumn
        integer :: iostat
        integer :: i
        logical :: exist_file
        
            ncolumn = 1 !O primeiro dado lido já é uma coluna
            maxncolumn = 1

            inquire(file=file, exist=exist_file)
            if(exist_file) then
                open(unit=stdin, file=file, action='READ', form='FORMATTED', status='OLD', err=10)
            else 
                print *, "ERRO FATAL no Módulo = main"
                print *, "Arquivo de configuração ", file, " inexistente"
                print *, "Impossível continuar com a execução do programa"
                stop
            end if

            do
                read(unit=stdin, fmt='(a1024)', iostat=iostat) line

                if(iostat == ioend) then
                    rewind(unit=stdin, err=11)
                    exit
                else if(iostat /= 0) then
                    print *, "Um erro ocorreu na leitura do arquivo ", file
                    stop
                else 
                    ncolumn = 1
                    line = adjustl(line)
                    do i = 1, len_trim(line)
                        if(line(i:i) == ' ') ncolumn = ncolumn + 1  
                    end do

                    if(maxncolumn < ncolumn) maxncolumn = ncolumn

                end if
            end do

            close(unit=stdin, status='KEEP', err=12)

            ncolumns = maxncolumn
    
        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", file
        stop
        
        11 print *, "Houve um erro no rebobinamento do arquivo ", file
        stop

        12 print *, "Houve um erro ao fechar o arquivo ", file
        stop
    
        999 continue

    end subroutine maximum_number_of_columns_in_a_file

    subroutine convert_external_file_to_internal(file, &
                                                 recl, &
                                                 nlines, &
                                                 internal_file)
        !!Dando um arquivo 'file' com tamanho de regitro maximo 'recl' em bytes
        !!e número de linhas nlines, esta subroutina transforma 
        !!este arquivo (externo) em interno através da saída 'internal_file'

        character(len=*), intent(in) :: file
        integer, intent(in) :: recl
        integer, intent(in) :: nlines
        character(len=:), dimension(:) , allocatable, intent(out) :: internal_file
        integer :: i
        logical :: exist_file
        integer :: erro

            allocate(character(len=recl) :: internal_file(nlines) , stat=erro)

            select case(erro)
                case(1)
                    print *, "Erro na rotina do sistema ao tentar fazer a alocação"
                    stop
                case(2)
                    print *, "Um objeto de dados inválido foi especificado para alocação"
                    stop
                case(3)
                    print *, "Erro na rotina do sistema ao tentar fazer a alocação"
                    print *, "Um objeto de dados inválido foi especificado para alocação"
                    stop
                case default
                    continue
            end select

            inquire(file=file, exist=exist_file)
            if(exist_file) then
                open(unit=stdin, file=file, action='READ', form='FORMATTED', status='OLD', err=10)
            else 
                print *, "ERRO FATAL no Módulo = main"
                print *, "Arquivo de configuração ", file, " inexistente"
                print *, "Impossível continuar com a execução do programa"
                stop
            end if

            do i=1, nlines
                read(unit=stdin, fmt='(a32)', err=11) internal_file(i)
            end do
            
            close(unit=stdin, status='KEEP', err=12)
        
        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", file
        stop
        
        11 print *, "Houve um erro no rebobinamento do arquivo ", file
        stop

        12 print *, "Houve um erro ao fechar o arquivo ", file
        stop

        999 continue
        
    end subroutine convert_external_file_to_internal

    subroutine error_exe_cmd_message(cmdstat, cmdmsg)
        !! Informado o número cmdstat referente a subroutina execute_command_line
        !! em caso de erro uma mensage é exibida referente ao erro e o programa é parado
        !! caso nenhum erro seja encontrado a execução do programa continua normalmente

        integer, intent(in) :: cmdstat
        character(len=*), intent(in) :: cmdmsg

            error_exe_cmd: select case(cmdstat)
                case(-2)
                    print *, "Execução assicrona não suportada"
                    stop
                case(-1)
                    print *, "Execução do comando em linha não suportada"
                    stop
                case(1)
                    print *, "Ocorreu um erro durante a execução"
                    print *, trim(cmdmsg)
                case(0)
                    continue
            end select error_exe_cmd
    
    end subroutine error_exe_cmd_message

    subroutine create_directory_if_it_doesnt_exist(path)
        !! Dado um caminho de um diretório 'path' esta subroutina averigua se o mesmo existe
        !! Se não existir o mesmo é criado

        character(len=*), intent(in) :: path
        logical :: exist_dir
        integer :: cmd_error
        character(len=128) :: cmd_msg

            inquire(file=trim(path)//'/.', exist=exist_dir)
            if(exist_dir) then
                continue
            else
                call execute_command_line('mkdir '//trim(path)//'', &
                                            wait=.TRUE., &
                                            cmdstat=cmd_error, & 
                                            cmdmsg=cmd_msg)
                
                call error_exe_cmd_message(cmdstat=cmd_error, cmdmsg=cmd_msg)

            end if

    end subroutine create_directory_if_it_doesnt_exist 

    subroutine abspath(relative_path, absolute_path)
        !! Dado um caminho relativo 'relative_path' está subroutina retorna
        !! a versão normalizada e absoluta deste caminho na variável absolute_path

        character(len=*), intent(in) :: relative_path
        character(len=*), intent(out) :: absolute_path
        integer :: cmd_error
        character(len=1028) :: cmd_msg
        character(len=128) :: tmp_dir, tmp_file

            tmp_dir = '/tmp/fortran'
            tmp_file = '/tmp/fortran/auxiliary_file.dat'

            !Criando diretório e arquivo tempórarios
            call execute_command_line(command='mkdir '//trim(tmp_dir)//' && touch '//trim(tmp_file)//'', &
                                      wait=.TRUE., &
                                      cmdstat=cmd_error, &
                                      cmdmsg=cmd_msg)
            
            call error_exe_cmd_message(cmdstat=cmd_error, cmdmsg=cmd_msg)

            !Escrevendo em arquivo tempórario saída do comando realpath
            call execute_command_line(command='realpath '//trim(relative_path)//' > '//trim(tmp_file)//'', &
                                      wait=.TRUE., &
                                      cmdstat=cmd_error, &
                                      cmdmsg=cmd_msg)

            call error_exe_cmd_message(cmdstat=cmd_error, cmdmsg=cmd_msg)

            !Lendo arquivo tempórario e atribuindo valor a variável absolute_path
            open(unit=stdin, file=tmp_file, action='READ', form='FORMATTED', status='OLD', err=10)

            read(unit=stdin, fmt='(A)', err=11) absolute_path

            close(unit=stdin, status='KEEP', err=12)

            !Apagando diretório tempórario
            call execute_command_line(command='rm -r '//trim(tmp_dir)//'', &
                                      wait=.TRUE., &
                                      cmdstat=cmd_error, &
                                      cmdmsg=cmd_msg)

            call error_exe_cmd_message(cmdstat=cmd_error, cmdmsg=cmd_msg)
        
        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", tmp_file
        stop
        
        11 print *, "Houve um erro na leitura do arquivo ", tmp_file
        stop

        12 print *, "Houve um erro ao fechar o arquivo ", tmp_file
        stop

        999 continue
        
    end subroutine abspath

    subroutine read_file_init_sim(simulation_name)
        !! Esta subroutina averigua a existencia e lê o arquivo localizado 
        !! no caminho relativo '../../../data/input/fortran/__init__.sim', guardando os registro
        !! de cada linha i no array(i), após concluir o procedimento o arquivo é fechado
        
        character(len=128), dimension(:), allocatable, intent(out) :: simulation_name
        character(len=128) :: path, file_name, input_file
        integer :: i
        integer :: nsimulations
        integer :: iostat, erro
        logical :: exist_file

            path = '../../../data/input/fortran/'
            file_name = '__init__.sim'
            call abspath(relative_path = (trim(path)//trim(file_name)), &
                         absolute_path = input_file)
            
            call number_of_lines_in_a_file(file=input_file, nlines=nsimulations)

            allocate(simulation_name(nsimulations), stat=erro)

            select case(erro)
                case(1)
                    print *, "Erro na rotina do sistema ao tentar fazer a alocação"
                    stop
                case(2)
                    print *, "Um objeto de dados inválido foi especificado para alocação"
                    stop
                case(3)
                    print *, "Erro na rotina do sistema ao tentar fazer a alocação"
                    print *, "Um objeto de dados inválido foi especificado para alocação"
                    stop
                case default
                    continue
            end select

            inquire(file=input_file, exist=exist_file)
            if(exist_file) then
                open(unit=stdin, file=input_file, action='READ', form='FORMATTED', status='OLD', err=10)
            else 
                print *, "ERRO FATAL no Módulo = main"
                print *, "Arquivo de configuração ", file_name, " inexistente"
                print *, "Impossível continuar com a execução do programa"
                stop
            end if

            do i=1, nsimulations
                read(unit=stdin, fmt=*, err=11) simulation_name(i)
            end do

            close(unit=stdin, status='KEEP', err=12)

        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", file_name
        stop
        
        11 print *, "Houve um erro na leitura do nome da simulação 'simulation_name' do arquivo ", file_name
        stop

        12 print *, "Houve um erro ao fechar o arquivo ", file_name
        stop

        999 continue

    end subroutine read_file_init_sim

    subroutine read_file_simulation_name_config(simulation_name, &
                                                method_name, &
                                                eps, &
                                                tol, &
                                                hmax, &
                                                hmin, &
                                                G_s, &
                                                distance_conversion_factor, &
                                                mass_conversion_factor, &
                                                time_conversion_factor)
        !! Esta subroutina averigua a existencia e lê os registros do arquivo localizado
        !! no caminho relativo '../../../data/input/fortran/{simulation_name}.config'

        character(len=*), intent(in) :: simulation_name
        character(len=128), intent(out), optional :: method_name
        real, intent(out), optional :: eps
        real, intent(out), optional :: tol
        real, intent(out), optional :: hmax, hmin
        real, intent(out), optional :: G_s           ! constante gravitacional do sistema
        real, intent(out), optional :: distance_conversion_factor
        real, intent(out), optional :: mass_conversion_factor
        real, intent(out), optional :: time_conversion_factor
        character(len=128) :: path, file_name, input_file
        character(len=:), dimension(:), allocatable :: line

        path = '../../../data/input/fortran/'
        file_name = trim(simulation_name)//'.config'
        call abspath(relative_path = (trim(path)//trim(file_name)), &
                         absolute_path = input_file)

        call convert_external_file_to_internal(file=input_file, &
                                               recl=32, &
                                               nlines=8, &
                                               internal_file=line)
        
        if(present(method_name)) then
            read(line(1), fmt=*, err=11) method_name
        end if

        if(present(eps)) then
            read(line(2), fmt=*, err=12) eps
        end if

        if(present(tol)) then
            read(line(3), fmt=*, err=13) tol
        end if

        if(present(hmax) .or. present(hmin)) then
            read(line(4), fmt=*, err=14) hmax, hmin
        end if

        if(present(G_s)) then
            read(line(5), fmt=*, err=15) G_s
        end if

        if(present(distance_conversion_factor)) then
            read(line(6), fmt=*, err=16) distance_conversion_factor
        end if

        if(present(mass_conversion_factor)) then
            read(line(7), fmt=*, err=17) mass_conversion_factor
        end if

        if(present(time_conversion_factor)) then
            read(line(8), fmt=*, err=18) time_conversion_factor
        end if
        
        !Caso não haja erro
        go to 999

        !Em caso de erro
        
        11 print *, "Houve um erro na leitura no  nome do método numerico 'method_name' no aquivo ", file_name
        stop

        12 print *, "Houve um erro na leitura do valor que irá auxiliar"
        print *, "na escrita nos arquivos resultantes da solução do problema 'eps'  no arquivo ", file_name
        stop
    
        13 print *, "Houve um erro na leitura no valor da tolerância do método numerico 'tol' no arquivo ", file_name
        stop

        14 print *, "Houve um erro na leitura do tamanho do passo 'hmax' e 'hmin' no arquivo ", file_name 
        stop

        15 print *, "Houve um erro na leitura no valor da constante gravitacional 'G' no arquivo ", file_name
        stop

        16 print *, "Houve um erro na leitura do fator de converção de distância"
        print *, "'distance_conversion_factor' no aarquivo ", file_name
        stop
        
        17 print *, "Houve um erro na leitura do fator de converção de massa 'mass_conversion_factor' no aarquivo ", file_name
        stop

        18 print *, "Houve um erro na leitura do fator de converção de tempo 'time_conversion_factor' no aarquivo ", file_name
        stop

        999 continue

    end subroutine read_file_simulation_name_config

    subroutine read_file_simulation_name_initial_coditions(simulation_name, &
                                                           nbody, &
                                                           dms, &
                                                           t0, &
                                                           tf, &
                                                           body_name, &
                                                           mass, &
                                                           s0, &
                                                           v0)
        !! Esta subroutina averigua a existencia e lê os registros do arquivo localizado
        !! no caminho relativo '../../../data/input/fortran/{simulation_name}.ic' que contem o domínio do problema 
        !! o nome do corpo, a mass e as condições iniciais dos corpos

        character(len=*), intent(in) :: simulation_name
        integer, intent(out) :: nbody
        integer, intent(out) :: dms
        real, intent(out) ::  t0, tf
        character(len=128), dimension(:), allocatable, intent(out) :: body_name
        real, dimension(:), allocatable, intent(out) :: mass
        real, dimension(:,:), allocatable, intent(out) :: s0
        real, dimension(:,:), allocatable, intent(out) :: v0
        integer :: nlines_of_file, ncolumns_of_file 
        character(len=128) :: path, file_name, input_file
        logical :: exist_file
        integer :: i, j
        integer :: error_number

            path = '../../../data/input/fortran/'
            file_name = trim(simulation_name)//'.ic'
            call abspath(relative_path = (trim(path)//trim(file_name)), &
                         absolute_path = input_file)

            call number_of_lines_in_a_file(file=input_file, nlines=nlines_of_file)
            call maximum_number_of_columns_in_a_file(file=input_file, ncolumns=ncolumns_of_file)

            nbody = nlines_of_file - 1 !devido a formatação do documento, para saber mais leia README.md
            dms = (ncolumns_of_file - 2)/2 !devido a formatação do documento, para saber mais leia README.md

            !! Averiguando se a dimenção do espaço vetorial, a qual deve ser 'dms=2', ou 'dms=3', 
            !! e o número de corpos 'ncorpos'>=2 envolvidos no problema
            erro_vetorial: if(nbody<2) then
                print *, "Quantidade de corpos deve ser 'ncorpos'>=2"
                stop
            else if(dms/=2 .AND. dms/=3) then erro_vetorial
                print *, "A dimensão do espaço vetorial deve ser bidimensional dms=2 ou tridimensional dms=3"
                stop
            else erro_vetorial
                continue
            end if erro_vetorial

            allocate(body_name(nbody), mass(nbody), s0(dms, nbody), v0(dms, nbody), stat=error_number)
            error_allocation: select case(error_number)
                case(1)
                    print *, "Erro na rotina do sistema ao tentar fazer a alocação"
                    stop
                case(2)
                    print *, "Um objeto de dados inválido foi especificado para alocação"
                    stop
                case(3)
                    print *, "Erro na rotina do sistema ao tentar fazer a alocação"
                    print *, "Um objeto de dados inválido foi especificado para alocação"
                    stop
                case default
                    continue
            end select error_allocation

            inquire(file=input_file, exist=exist_file)
            if(exist_file) then
                open(unit=stdin, file=input_file, action='READ', form='FORMATTED', status='OLD', err=10)
            else 
                print *, "ERRO FATAL no Módulo = main"
                print *, "Arquivo de configuração ", file_name, " inexistente"
                print *, "Impossível continuar com a execução do programa"
                stop
            end if

            read(unit=stdin, fmt=*, err=11) t0, tf
            do i=1, nbody
                read(unit=stdin, fmt=*, err=12) body_name(i), mass(i), (s0(j,i), j=1,dms), (v0(j,i), j=1, dms) 
            end do
            
            close(unit=stdin, status='KEEP', err=13)

        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", file_name
        stop
        
        11 print *, "Houve um erro na leitura no domínio em que o problema será solucionado t0, tf, no arquivo ", file_name
        stop
    
        12 print *, "Houve um erro na leitura do nome do corpo 'body_name'," 
        print *, "massa 'm',  posição inicial 's0', ou velocidade inicial 'v0' dos corpos  no arquivo ", file_name
        stop

        13 print *, "Houve um erro ao fechar o arquivo ", file_name
        stop
    
        999 continue
        
    end subroutine read_file_simulation_name_initial_coditions

    subroutine measurement_unit_converter(simulation_name, &
                                          distance_converter, &
                                          mass_converter, &
                                          time_converter, &
                                          distance_inverter, &
                                          mass_inverter, &
                                          time_inverter, &
                                          G_effective)
        !! Dada o nome de uma simulação, esta subroutina lê os fatores de conversão, do 
        !! arquivo {simulation_name}.config os faoteres de conversão, inversão de cada unidade 
        !! e a constante gravitacional efetiva do problema

        character(len=*), intent(in) :: simulation_name
        real, intent(out), optional :: distance_converter
        real, intent(out), optional :: mass_converter
        real, intent(out), optional :: time_converter
        real, intent(out), optional :: distance_inverter
        real, intent(out), optional :: mass_inverter
        real, intent(out), optional :: time_inverter
        real, intent(out), optional :: G_effective            ! Constate gravitacional efetiva
        real :: distance_conversion_factor
        real :: mass_conversion_factor
        real :: time_conversion_factor
        real :: G_s                                            ! Constate gravitacional do sistema

            call read_file_simulation_name_config(simulation_name = simulation_name, &
                                                  G_s = G_s, &
                                                  distance_conversion_factor = distance_conversion_factor, &
                                                  mass_conversion_factor = mass_conversion_factor, &
                                                  time_conversion_factor = time_conversion_factor)

            if(present(distance_converter)) then
                distance_converter = distance_conversion_factor
            end if

            if(present(mass_converter)) then
                mass_converter = mass_conversion_factor
            end if

            if(present(time_converter)) then
                time_converter = time_conversion_factor
            end if

            if(present(distance_inverter)) then
                distance_inverter = 1/distance_conversion_factor
            end if

            if(present(mass_inverter)) then
                mass_inverter = 1/mass_conversion_factor
            end if

            if(present(time_inverter)) then
                time_inverter = 1/time_conversion_factor
            end if

            if(present(G_effective)) then
                G_effective = G_s*(distance_conversion_factor**(3))*(mass_conversion_factor**(-1))*(time_conversion_factor**(-2))
            end if

    end subroutine measurement_unit_converter

    subroutine exe_simulation(simulation_name, &
                              runtime)
        !! Dada uma simulação 'simulation_name', esta subroutina executa as subroutinas númericas,
        !! com a finalidade de solucionar o problema, além de devolve o tempo de execução 'runtime'
        !! deste processo.

        character(len=*), intent(in) :: simulation_name
        real, intent(out) :: runtime
        character(len=128) :: method_name
        real :: eps
        real :: tol
        real :: hmax, hmin
        integer :: nbody
        integer :: dms
        real ::  t0, tf
        character(len=128), dimension(:), allocatable :: body_name
        real, dimension(:), allocatable :: mass
        real, dimension(:,:), allocatable :: s0
        real, dimension(:,:), allocatable :: v0
        real :: distance_converter
        real :: mass_converter
        real :: time_converter
        real :: distance_inverter
        real :: mass_inverter
        real :: time_inverter
        real :: G_effective
        character(len=128) :: output_dir
        character(len=128) :: output_dir_simulation_result
        integer :: start_time
        integer :: rate
        integer :: end_time

            output_dir = '../../../data/output/'
            call abspath(relative_path = (trim(output_dir)//trim(simulation_name)), &
                         absolute_path = output_dir_simulation_result)

            call create_directory_if_it_doesnt_exist(path = output_dir_simulation_result)

            call read_file_simulation_name_config(simulation_name = simulation_name, &
                                                  method_name = method_name, &
                                                  eps = eps, &
                                                  tol = tol, &
                                                  hmax = hmax, &
                                                  hmin = hmin)
            
            call read_file_simulation_name_initial_coditions(simulation_name = simulation_name, &
                                                             nbody = nbody, &
                                                             dms = dms, &
                                                             t0 = t0, &
                                                             tf = tf, &
                                                             body_name = body_name, &
                                                             mass = mass, &
                                                             s0 = s0, &
                                                             v0 = v0)
            
            call measurement_unit_converter(simulation_name = simulation_name, &
                                            distance_converter = distance_converter, &
                                            mass_converter = mass_converter, &
                                            time_converter = time_converter, &
                                            distance_inverter = distance_inverter, &
                                            time_inverter = time_inverter, &
                                            G_effective = G_effective)

            G_eft = G_effective
            
            call system_clock(count=start_time, count_rate=rate)

            choice_method: select case(method_name)
                case ('rkdp')

                    call sol_edo2_rk(g = g, &
                                     f = f, &
                                     meth_g = rkdp_fcx, &
                                     meth_f = rkdp_fx, &
                                     cc = (mass*mass_converter), &
                                     cx0 = (s0*distance_converter), &
                                     cy0 = (v0*distance_converter/time_converter), &
                                     t0 = (t0*time_converter), &
                                     tf = (tf*time_converter), &
                                     tol = tol, &
                                     eps = eps, &
                                     hmax = hmax, &
                                     hmin = hmin, &
                                     distance_inverter = distance_inverter, &
                                     time_inverter = time_inverter, &
                                     body_name=body_name, &
                                     output_dir_simulation_result = output_dir_simulation_result)

                case ('rkvn')

                    call sol_edo2_rk(g = g, &
                                     f = f, &
                                     meth_g = rkvn_fcx, &
                                     meth_f = rkvn_fx, &
                                     cc = (mass*mass_converter), &
                                     cx0 = (s0*distance_converter), &
                                     cy0 = (v0*distance_converter/time_converter), &
                                     t0 = (t0*time_converter), &
                                     tf = (tf*time_converter), &
                                     tol = tol, &
                                     eps = eps, &
                                     hmax = hmax, &
                                     hmin = hmin, &
                                     distance_inverter = distance_inverter, &
                                     time_inverter = time_inverter, &
                                     body_name=body_name, &
                                     output_dir_simulation_result = output_dir_simulation_result)


                case ('rkfb')

                    call sol_edo2_rk(g = g, &
                                     f = f, &
                                     meth_g = rkfb_fcx, &
                                     meth_f = rkfb_fx, &
                                     cc = (mass*mass_converter), &
                                     cx0 = (s0*distance_converter), &
                                     cy0 = (v0*distance_converter/time_converter), &
                                     t0 = (t0*time_converter), &
                                     tf = (tf*time_converter), &
                                     tol = tol, &
                                     eps = eps, &
                                     hmax = hmax, &
                                     hmin = hmin, &
                                     distance_inverter = distance_inverter, &
                                     time_inverter = time_inverter, &
                                     body_name=body_name, &
                                     output_dir_simulation_result = output_dir_simulation_result)

                case ('rkfb7')

                    call sol_edo2_rk(g = g, &
                                     f = f, &
                                     meth_g = rkfb7_fcx, &
                                     meth_f = rkfb7_fx, &
                                     cc = (mass*mass_converter), &
                                     cx0 = (s0*distance_converter), &
                                     cy0 = (v0*distance_converter/time_converter), &
                                     t0 = (t0*time_converter), &
                                     tf = (tf*time_converter), &
                                     tol = tol, &
                                     eps = eps, &
                                     hmax = hmax, &
                                     hmin = hmin, &
                                     distance_inverter = distance_inverter, &
                                     time_inverter = time_inverter, &
                                     body_name=body_name, &
                                     output_dir_simulation_result = output_dir_simulation_result)

                case default
                    print *, "Erro fatal, método numerico não encontrado"
                    stop

            end select choice_method   

            call system_clock(count=end_time)

            runtime = real(end_time - start_time)/real(rate)

    end subroutine exe_simulation

    subroutine report_body_features(simulation_name, & 
                                    runtime)
        !! Dada uma simulação 'simulation_name' e um tempo de execução, esta subroutina 
        !! escreve um relatório na formatação json, que irá conter infoções como o tempo 
        !! de processamento da simulação, configuração, caminho dos arquivos da simulação ...
        !! dentre outras informações. Para mais informações sobre a formatação deste arquivo leia
        !! README.md 

        character(len=*), intent(in) :: simulation_name
        real, intent(in) :: runtime
        character(len=128) :: method_name
        real :: eps
        real :: tol
        real :: hmax, hmin
        integer :: nbody
        integer :: dms
        real ::  t0, tf
        character(len=128), dimension(:), allocatable :: body_name
        real, dimension(:), allocatable :: mass
        real, dimension(:,:), allocatable :: s0
        real, dimension(:,:), allocatable :: v0
        character(len=128) :: output_dir,  path, file_name, output_file
        character(len=1024) :: fmt
        integer :: i, j

            call read_file_simulation_name_config(simulation_name = simulation_name, &
                                                  method_name = method_name, &
                                                  eps = eps, &
                                                  tol = tol, &
                                                  hmax = hmax, &
                                                  hmin = hmin)

            call read_file_simulation_name_initial_coditions(simulation_name = simulation_name, &
                                                             nbody = nbody, &
                                                             dms = dms, &
                                                             t0 = t0, &
                                                             tf = tf, &
                                                             body_name = body_name, &
                                                             mass = mass, &
                                                             s0 = s0, &
                                                             v0 = v0)
            
            output_dir = '../../../data/output/'
            file_name = 'report.json'
            call abspath(relative_path = (trim(output_dir)//trim(simulation_name)//'/'//trim(file_name)), &
                         absolute_path = output_file)

            open(unit=stdin, file=output_file, action='WRITE', form='FORMATTED', status='REPLACE', err=10)

            fmt = '(a1, /, &
                   &a, f12.3, a, / &
                   &a, /, &
                   &a, a, a, /,&
                   &a, /, &
                   &a, a, a2, /, &
                   &a, es0.3, a, /, &
                   &a, es0.3, a, /, &
                   &a, /, &
                   &a, es0.3, a, /, &
                   &a, es0.3, /, &
                   &a, /, &
                   &a, /, &
                   &a, /, &
                   &a, f12.8, a, /, &
                   &a, f12.8, /, &
                   &a, /, &
                   &a, i0, a, /,&
                   &a, i0, a, /,&
                   &a)'

            write(unit=stdin, fmt=fmt, err=11) '{', &
                                               '    "runtime" : ', runtime, ',', &
                                               '    "simulation" : {', &
                                               '        "name" : "',trim(simulation_name), '",', &
                                               '            "method" : {', &
                                               '                "name" : "', trim(method_name), '",', &
                                               '                "eps" : ', eps, ',', &
                                               '                "tol" : ', tol, ',', &
                                               '                "step" : {', &
                                               '                    "hmin" : ', hmin, ',', &
                                               '                    "hmax" : ', hmax, &
                                               '                }', &
                                               '            },', &
                                               '        "domain" : {', &
                                               '            "t0" : ', t0, ',', &
                                               '            "tf" : ', tf, &
                                               '            },', &
                                               '        "dms" : ', dms, ',',  &
                                               '        "nbody" : ', nbody, ',', &
                                               '        "state" : ['

            do i = 1, (nbody - 1)

                fmt = '(a, /, &
                       &a, a, a/, &
                       &a, es0.3, a, /, &
                       &a, a, a, /, &
                       &a)'

                write(unit=stdin, fmt=fmt, err=11) '            {', &
                                                   '                "body" : "', trim(body_name(i)), '",', &
                                                   '                "mass" : ', mass(i), ',', &
                                                   '                "local_storage" : "', trim(body_name(i)), '.sob"', & 
                                                   '            },'

            end do

            fmt = '(a, /, &
                   &a, a, a, /, &
                   &a, es0.3, a, / &
                   &a, a, a, /, &
                   &a, /, &
                   &a, /, &
                   &a, /, &
                   &a, /, &
                   &a)'

            write(unit=stdin, fmt=fmt, err=11) '            {', &
                                               '                "body" : "', trim(body_name(nbody)), '",', &
                                               '                "mass" : ', mass(nbody), ',', &
                                               '                "local_storage" : "', trim(body_name(nbody)), '.sob"', & 
                                               '            }', &
                                               '        ]', &
                                               '    }', &
                                               '}'

            

            close(unit=stdin, status='KEEP', err=12)

        !Caso não haja erro
        go to 999

        !Em caso de erro
        10 print *, "Houve um erro no desempacotamento (abrimento) do arquivo ", file_name
        stop

        11 print *, "Houve um erro na escrita do arquivo", file_name
        stop

        12 print *, "Houve um erro ao fechar o arquivo ", file_name
        stop

        999 continue

    end subroutine report_body_features

    subroutine exe_all_simutions()
        !! End_Point, esta subroutina será utilizada pelo o main com a 
        !! finalidade de executar todas as simulações  

        character(len=128), dimension(:), allocatable :: simulation_name
        real :: runtime
        integer :: nsimulations
        integer :: simulation_number

            call read_file_init_sim(simulation_name=simulation_name)

            nsimulations = size(simulation_name, dim=1)

            do simulation_number = 1, nsimulations
                call exe_simulation(simulation_name = simulation_name(simulation_number), &
                                    runtime = runtime)

                call report_body_features(simulation_name = simulation_name(simulation_number), &
                                          runtime = runtime)
            end do

    end subroutine exe_all_simutions

end program n_body_problem
!===========================================================