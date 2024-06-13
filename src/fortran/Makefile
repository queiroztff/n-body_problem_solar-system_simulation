#                                            Opções de compilação gfortran
##=================================================================================================================================================
#
# Sinalizadores de advertencia
#   -Wall               Habilita as opções de avisos mais utilizadas. 
#                       A qual inclui as seguintes flags: -Waliasing, -Wampersand, -Wconversion, -Wsurprising, -Wc-binding-type, 
#                                                         -Wintrinsics-std, -Wtabs, -Wintrinsic-shadow, -Wline-truncation, -Wtarget-lifetime, 
#                                                         -Winteger-division, -Wreal-q-constant, -Wunused and -Wundefined-do-loop
#
#   -Wextra             Habilita algumas opções de aviso para o uso de recursos de linguagem que podem ser problemáticos
#                       A qual incluit as sequintes flags: -Wcompare-reals, -Wunused-parameter and -Wdo-subscript
#
#   -pedantic           Gera avisos sobre recursos de linguagem que são suportados pelo o gfortran, mas não nfazem parte do padrão ISO
#                       do Fortran 95
#
#   -Wsurprising        Gera um aviso quando construções de código "suspeitas"  forem encontradas
#    
#   -Wunderflow         Groduz um aviso quando expressões constantes numéricas são encontradas, o que produz um underflow durante a compilação.
#                       Está opção é habilitada por padrão         
#
# Sinalizadores de entrada e saída
#   -c <arquivo>          Compila para um arquivo de objeto <arquivo>
#   -o <arquivo>          Direciona a saída para <arquivo>
#   -J <diretório>        Direciona <arquivo>.mod para <diretório>
#   -I <diretorio>        Busca <arquivo>.mod em <diretório>
#
# Sinalizadores que controlam o dialeto Fortran
#   -fdefault-integer-8     Define todas variáveis do tipo inteiro pra o tamanho de 8 bytes
#
#   -fdefault-real-8 		Define todas variáveis do tipo real para o tamanho de 8 bytes 
#   -fdefault-real-10       Define todas variáveis do tipo real para o tamanho de 10 bytes 
#   -fdefault-real-16       Define todas variáveis do tipo real para o tamanho de 16 bytes
#  
#   -std={f95|f2003|f2008|f2018|gnu}     	Especifica o padrão ao qual se espera que o programa esteja em conformidade, 
#											o valor 'gnu' especifica um superconjunto do padrão Fortran mais 
#											recente que inclui todas as extensões suportadas pelo GNU Fortran
# 	
#  -fopenmp  				Abilita as extesões OpenMP, como !$OMP e sentinelas !$
#
# Sinalizadores de Alvo
# 
#=================================================================================================================================================

runge_kutta = meth_Dormand-Prince.f90 meth_Verner.f90 meth_Fehlberg.f90 meth_Fehlberg-7th.f90 sol_edo_o2_rk.f90
main = edo_nbody.f90 main.f90
executable_file = n-body.exe

Runge_Kutta = $(addprefix runge-kutta/, $(runge_kutta))

lib = $(Runge_Kutta)

LIB = $(addprefix lib/, $(lib))
SRC = $(addprefix ./src/, $(LIB) $(main))
DEP = $(SRC:.f90=.o)

#Build path
OBJ = $(addprefix $(realpath ../../build/fortran/obj/)/, $(notdir $(SRC:.f90=.o)))
MOD = $(realpath ../../build/fortran/mod)
BIN = $(addprefix $(realpath ../../build/fortran/bin/)/, $(executable_file))

CC = gfortran
C_warning_flags = -Wall -Wextra -pedantic  -Wsurprising -Werror -fbacktrace
C_compile_object = -std=f2018 -fdefault-integer-8 -fdefault-real-8 -O2 -march=native
C_output_flag = -o


#--------------------------------------------------------
all:	$(DEP) $(BIN)

%.o:	%.f90
	$(CC) $(C_compile_object) -c $< -J $(MOD) -o ../../build/fortran/obj/$(@F) 

%.exe:	$(OBJ)
	$(CC) $^ -I $(MOD) -o $@
#--------------------------------------------------------

#--------------------------------------------------------
clean:
	rm $(MOD)/*.mod
	rm $(OBJ)
	rm $(BIN)
#--------------------------------------------------------

meth_Dormand-Prince.f90:	
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/lib/runge-kutta/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)

meth_Verner.f90:
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/lib/runge-kutta/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)

meth_Fehlberg.f90:
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/lib/runge-kutta/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)

meth_Fehlberg-7th.f90:
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/lib/runge-kutta/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)

sol_edo_o2_rk.f90:
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/lib/runge-kutta/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)


edo_nbody.f90:
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)


main.f90:
	$(CC) $(C_warning_flags) $(C_compile_object) -c ./src/$@ -J $(MOD) -o ./obj/$(@:.f90=.o)

rebuild:
	$(CC) $(OBJ) -I $(MOD) -o $(BIN)

run: 
	cd $(dir $(BIN)) && ./$(notdir $(BIN))

rebuild_and_run: rebuild run