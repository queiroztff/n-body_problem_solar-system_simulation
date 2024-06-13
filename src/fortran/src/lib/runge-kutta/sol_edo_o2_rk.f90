!> @brief Dada a seguinte equação diferencial de segunda ordem edo(2)
!! fazendo y'=x, a mesma pode ser reescrita de forma aclopada, como uma equação diferencial de primeira ordem edo(1)
!!                    y'=x =f(t,y,x)
!!                    x'=g(t,y,x)
!! 
!! Este módulo tem por objetivo solucionar PVI(problema de valor inicial) de uma edo(2) em um domínio t=[t0,tf],
!! através de um método númerico que será informado pelo o usuário, como argumento da subroutina.
!! Para isso, será realiza sucessivas chamadas da subroutina do respectivo método numérico, 
!! onde o codigo fonte de todos módulos os quais contém o método a ser escolhido se encontra 
!! no dirtório /n_body_problem/Software/fortran/src/lib/runge-kutta, 
!! ou no mesmo caminho relativo aparti da localização dete módulo.

!===========================================================
module sol_edo_o2_rk

    implicit none

    private
    public :: sol_edo2_rk

contains

    subroutine sol_edo2_rk(g, &
                           f, &
                           meth_g, &
                           meth_f, &
                           cc, &
                           cx0, &
                           cy0, &
                           t0, &
                           tf, &
                           tol, &
                           eps, &
                           hmax, &
                           hmin, &
                           distance_inverter, &
                           time_inverter, &
                           body_name, &
                           output_dir_simulation_result)

        !definindo as interfaces que irão receber às equações diferenciais (ed) como argumento    
        interface differential_eq_f
            pure function f(x) result(y)
                real, dimension(:,:), intent(in) :: x
                real, dimension(size(x,dim=1), size(x,dim=2)) :: y
            end function f
        end interface differential_eq_f

        interface differential_eq_g
            pure function g(c, y) result(z)
                real, dimension(:), intent(in) :: c
                real, dimension(:,:), intent(in) :: y
                real, dimension(size(y,dim=1), size(y,dim=2)) :: z
            end function g
        end interface differential_eq_g

        !definindo às interfaces que irá receber o método númerico como argumento
        interface meth_for_ed_f
            subroutine meth_f(f, x, y0, h, tol, y, err, hopt)
                interface differential_eq
                    pure function f(x) result(y)
                        real, dimension(:,:), intent(in) :: x
                        real, dimension(size(x,dim=1), size(x,dim=2)) :: y
                    end function f
                end interface differential_eq

                real, dimension(:,:), intent(in) :: x
                real, dimension(:,:), intent(in) :: y0
                real, intent(in) :: h
                real, intent(in) :: tol
                real, dimension(:,:), intent(out) :: y
                real, intent(out) :: hopt
                real, intent(out) :: err
            end subroutine meth_f
        end interface meth_for_ed_f

        interface meth_for_ed_g
            subroutine meth_g(g, c, x, y0, h, tol, y, err, hopt)
                interface differential_eq
                    pure function g(c, x) result(y)
                        real, dimension(:), intent(in) :: c
                        real, dimension(:,:), intent(in) :: x
                        real, dimension(size(x,dim=1), size(x,dim=2)) :: y
                    end function g
                end interface differential_eq

                real, dimension(:), intent(in) :: c
                real, dimension(:,:), intent(in) :: x
                real, dimension(:,:), intent(in) :: y0
                real, intent(in) :: h
                real, intent(in) :: tol
                real, dimension(:,:), intent(out) :: y
                real, intent(out) :: hopt
                real, intent(out) :: err
            end subroutine meth_g
        end interface meth_for_ed_g

        real, dimension(:,:), intent(in) ::  cx0, cy0                     !Vetores referente a condição inicial do problema
        real, dimension(:), intent(in) :: cc                              !Constantes que serão passadas como argumento para segunda ed g
        real, intent(in) :: t0, tf                                        ![t0,tf] represeta o intervalo (domínio) em que a ed será solucionada
        real, intent(in) :: tol                                           !Tolerância do respectivo método a ser definida pelo usuário, caso contrário eps = e-11                           
        real, intent(in) :: eps                                           !Delta entre dois valores, que irá auxiliar no ato de escrever no arquivo de saída, caso naõ seja imformado eps = 0.01
        real, intent(in):: hmax, hmin                                     !Tamanho do passo máximo 'hmax' e minímo 'hmin' envolvidos no método de solução a ser informado, caso contrario hmax=e-6 e hmin=e-10
        real, intent(in) :: distance_inverter                             !Fator de inversão de unidade de distância
        real, intent(in) :: time_inverter                                 !Fator de inversão de unidade de tempo
        character(len=*), dimension(:), intent(in) :: body_name           !Nome dos corpos envolvidos no problema
        character(len=*) :: output_dir_simulation_result                  !Diretório que irá conter o resultado da simulação
        real, dimension(size(cx0,dim=1), size(cx0,dim=2)) :: x0, x        !Variáveis axiliares na solução differential_eq_f
        real, dimension(size(cy0,dim=1), size(cy0,dim=2)) :: y0, y        !Variáveis axiliares na solução differential_eq_g
        real :: err_x, err_y                                              !Variavel auxiliares para a obteção do maior erro dentre às coordenadas
        real :: t                                                         !Variável que irá percorrer o domínio do problema [t0,tf] 
        real :: h, hopt, hopt_x, hopt_y                                   !Variáveis que irão indicar o tamanho do passo envolvido no método de solução
        integer :: i, j                                                   !Variáveis que serão utilizada como contadores
        integer :: dms                                                    !Variável que irá indicar a dimensão do espaço vetorial 'dms', conforme os dados de entrada
        integer :: nbody                                                  !Variável auxiliar que irá indicar a quantidade de corpos envolvido no problema 'ncorpos'
        real, dimension(size(cx0,dim=1), size(cx0,dim=2)) :: x_aux, y_aux !Vetores auxiliares para escrita no arquivo de saída 
        real :: t_c                                                       !Variável auxiliará na escrita do tempo, aqual receberá o valor convertido para as unidades original
        real, dimension(size(cx0,dim=1), size(cx0,dim=2)) :: x_c, y_c     !Variável auxiliará na escrita da posição e da velocidade, aqual receberá o valor convertido para as unidades original
        real :: err_x_c, err_y_c                                          !Variável auxiliará na escrita dos erros de simulação da posição e da velocidade, aqual receberá o valor convertido para as unidades original
        character(len=384), dimension(size(cx0,dim=2)) :: output_file     !Arquivos de saída referente a solução númerica pelo método 

            dms = size(cx0,dim=1)           !Atribuindo a dimensão do espaço vetorial, conforme os dados de entrada
            nbody = size(cx0,dim=2)         !Atribuindo o número de corpos envoldos no problema conforme os dados de entrada 

            !Atribuindo as condições iniciais para a inícialização da subroutina
            h = hmin
            t = t0
            x0 = cx0
            y0 = cy0

            !Atribuindo valores iniciais, aos vetores que irão auxiliar na escrita do arquivo de saída
            x_aux = real(0)
            y_aux = real(0)

            !Gerando os arquivos (de saída) que irão receber os dados gerados pelo o método numérico
            !Estes arquivos se encontrar no díretório ../../output/$(name_simulation)
            generating_files: do j=1, nbody
                output_file(j)= trim(output_dir_simulation_result)//'/'//trim(body_name(j))//'.sob'  !(.sob state of the body)
                open(unit=j, action='WRITE', form='FORMATTED', status='REPLACE', file=output_file(j), err=10)
            end do generating_files

            !Recorrencia do método númerico
            solution_edo: do

                call meth_g(g, cc, x0, y0, h, tol, y, err_y, hopt_y)

                call meth_f(f, y0, x0, h, tol, x, err_x, hopt_x)

                !Condição para que o loop continue
                loop: if(t<tf) then

                    !Escrevendo os pontos 't', 'x', 'y', 'err_x' e 'err_y' gerados pelo o método
                    !se e somente se a diferença entre os mesmos (pontos) for maior que 'eps'  
                    write_cond: if((abs(maxval(x-x_aux))) > eps .or. (abs(maxval(y-y_aux))) > eps) then

                        t_c = t*time_inverter
                        x_c = x*distance_inverter
                        y_c = y*(distance_inverter/time_inverter)
                        err_x_c = err_x*distance_inverter
                        err_y_c = err_y*(distance_inverter/time_inverter)

                        writing_files: do j=1, nbody
                            write(unit=j, fmt=*, err=11) t_c, (x_c(i,j), i=1, dms), (y_c(i,j), i=1, dms), err_x_c, err_y_c
                        end do writing_files

                        x_aux = x
                        y_aux = y

                    end if write_cond

                    !Escolhendo o passo ideal 'hopt' dentre 'hopt_x' e hopt_y, para a proxima interação
                    h_optimal: if(hopt_x < hopt_y) then
                        hopt = hopt_x
                    else
                        hopt = hopt_y
                    end if h_optimal

                    !Averiguando se o valor do passo ideal 'hopt', se encontra entre os valores
                    !do passo maximo 'hmax' e do passo minimo  'hmin'
                    h_check: if(hopt < hmin) then
                        hopt = hmin
                    else if (hopt > hmax) then h_check
                        hopt = hmax
                    end if h_check

                    !Atrindo novos valores às variáveis de recorrencia 'h', 't', 'x0', 'y0'
                    !para a procima interação
                    h = hopt
                    t = t + h
                    x0 = x
                    y0 = y

                    cycle

                else 

                    !Escrevendo nos arquivos de saída os dados gerados pela última interação
                    last_data: do j=1, nbody

                        t_c = t*time_inverter
                        x_c = x*distance_inverter
                        y_c = y*(distance_inverter/time_inverter)
                        err_x_c = err_x*distance_inverter
                        err_y_c = err_y*(distance_inverter/time_inverter)

                        write(unit=j, fmt=*, err=12) t_c, (x_c(i,j), i=1, dms), (y_c(i,j), i=1, dms), err_x_c, err_y_c

                    end do last_data

                    !Fechando os arquivos de saída
                    close_files: do j=1, nbody
                        close(unit=j, status='keep', err=13)
                    end do close_files

                    exit

                end if loop

            end do solution_edo

        !Se não hover erro no desenpacotamento (abrimento), escrita dos dados ou no empacotamento (fechamento) do arquivo de saída
        go to 999

        !em caso de erro
        10 print *, "houve um erro no desempacotamento (abrimento) do arquivo de saída 'output_file'"
        stop

        11 print *, "houve um erro na escrita dos dados da simulação no arquivo de saída 'output_file'"
        stop

        12 print *, "houve um erro na escrita dos ultimos dados da simulação no arquivo de saída 'output_file'"
        stop

        13 print *,  "houve um erro no empacotamento (fechamento) do arquivo de saída 'output_file'"
        stop

        999 continue   
    end subroutine sol_edo2_rk

end module sol_edo_o2_rk
!===========================================================