!> @brief Método Runge-kutta-Dormand-Prince

!Tabela de Butcher referente ao respectivo método
 !_________________________________________________________
 !c1=(0.0)   | 
 !c2=(1.0/5) | a21=(1.0/5)
 !c3=(3.0/10)| a31=(3.0/40)       a32=(9.0/40)
 !c4=(4.0/5) | a41=(44.0/45)      a42=(-56.0/15)      a43=(32.0/9)
 !c5=(8.0/9) | a51=(19372.0/6561) a52=(-25360.0/2187) a53=(64448.0/6561) a54=(-212.0/729)
 !c6=(1.0)   | a61=(9017.0/3168)  a62=(-355.0/33)     a63=(46732.0/5247) a64=(49.0/176)   a65=(-5103.0/18656)
 !c7=(1.0)   | a71=(35.0/384)     a72=(0.0)           a73=(500.0/1113)   a74=(125.0/192)  a75=(-2187.0/6784)   a76=(11.0/84)
 !           |---------------------------------------------------------------------------------------------------------------------------- 
 !           | b1=(35.0/384)      b2=(0.0)            b3=(500.0/1113)    b4=(125.0/192)   b5=(-2187.0/6784)    b6=(11.0/84)
 !           | d1=(5179.0/57600)  d2=(0.0)            d3=(7571.0/16695)  d4=(393.0/640)   d5=(-92097.0/339200) d6=(187.0/2100) d7=(1.0/40)
 !           |---------------------------------------------------------------------------------------------------------------------------- 
 !           | e1=(-71.0/57600)   e2=(0.0)            e3=(71.0/16695)    e4=(-71.0/1920)  e5=(17253.0/339200)  e6=(-22.0/525)  e7=(1.0/40)
 !_________________________________________________________
 
!==========================================================
module dormand_prince

    implicit none

    private
    public :: rkdp_fx, rkdp_fcx

    real, parameter :: c1=(0.0), c2=(1.0/5), c3=(3.0/10), c4=(4.0/5), c5=(8.0/9), c6=(1.0), c7=(1.0)

    real, parameter :: a21=(1.0/5), a31=(3.0/40), a32=(9.0/40), a41=(44.0/45), a42=(-56.0/15), &
                       a43=(32.0/9), a51=(19372.0/6561), a52=(-25360.0/2187), a53=(64448.0/6561), &
                       a54=(-212.0/729), a61=(9017.0/3168), a62=(-355.0/33), a63=(46732.0/5247), &
                       a64=(49.0/176), a65=(-5103.0/18656), a71=(35.0/384), a72=(0.0), &
                       a73=(500.0/1113),  a74=(125.0/192), a75=(-2187.0/6784), a76=(11.0/84)
    
    real, parameter :: b1=(35.0/384), b2=(0.0), b3=(500.0/1113), b4=(125.0/192), b5=(-2187.0/6784), &
                       b6=(11.0/84)
    
    real, parameter :: d1=(5179.0/57600), d2=(0.0), d3=(7571.0/16695), d4=(393.0/640), &
                       d5=(-92097.0/339200), d6=(187.0/2100), d7=(1.0/40)

    real, parameter :: e1=(-71.0/57600), e2=(0.0), e3=(71.0/16695), e4=(-71.0/1920), &
                       e5=(17253.0/339200), e6=(-22.0/525), e7=(1.0/40)
     
contains

    subroutine rkdp_fx(f, x, y0, h, tol, y, err, hopt)

        interface
            pure function f(x) result(y)
                real, dimension(:,:), intent(in) :: x
                real, dimension(size(x,dim=1), size(x,dim=2)) :: y
            end function f
        end interface

        real, dimension(:,:), intent(in) :: x
        real, dimension(:,:), intent(in) :: y0
        real, intent(in) :: h
        real, intent(in) :: tol
        real, dimension(:,:), intent(out) :: y
        real, intent(out) :: err
        real, intent(out) :: hopt
        real, dimension(size(y,dim=1), size(y,dim=2), 7) :: k               
        real, dimension(size(y,dim=1), size(y,dim=2)) :: esti_err_y 
        real:: s

            k(:,:,1) = h*f(x)
            k(:,:,2) = h*f(x + a21*k(:,:,1)) 
            k(:,:,3) = h*f(x + a31*k(:,:,1) + a32*k(:,:,2)) 
            k(:,:,4) = h*f(x + a41*k(:,:,1) + a42*k(:,:,2) + a43*k(:,:,3))
            k(:,:,5) = h*f(x + a51*k(:,:,1) + a52*k(:,:,2) + a53*k(:,:,3) + a54*k(:,:,4))
            k(:,:,6) = h*f(x + a61*k(:,:,1) + a62*k(:,:,2) + a63*k(:,:,3) + a64*k(:,:,4) + a65*k(:,:,5))
            k(:,:,7) = h*f(x + a71*k(:,:,1) + a73*k(:,:,3) + a74*k(:,:,4) + a75*k(:,:,5) + a76*k(:,:,6))          !a72=0.0

            y = y0 + b1*k(:,:,1) + b3*k(:,:,3) + b4*k(:,:,4) + b5*k(:,:,5) + b6*k(:,:,6)                        !b2=0.0

            esti_err_y = e1*k(:,:,1) + e3*k(:,:,3) + e4*k(:,:,4) + e5*k(:,:,5) + e6*k(:,:,6) + e7*k(:,:,7)      !e2=0.0

            err = maxval(abs(esti_err_y))
            s = ((tol*h)/(2.0*err))**(1.0/5)
            hopt = s*h

    end subroutine rkdp_fx
    
    subroutine rkdp_fcx(f, c, x, y0, h, tol, y, err, hopt)
    
        interface 
            pure function f(c, x) result(y)
                real, dimension(:), intent(in) :: c
                real, dimension(:,:), intent(in) :: x
                real, dimension(size(x,dim=1), size(x,dim=2)) :: y
            end function f
        end interface
        
        real, dimension(:), intent(in) :: c
        real, dimension(:,:), intent(in) :: x
        real, dimension(:,:), intent(in) :: y0
        real, intent(in) :: h
        real, intent(in) :: tol
        real, dimension(:,:), intent(out) :: y
        real, intent(out) :: err
        real, intent(out) :: hopt
        real, dimension(size(y,dim=1), size(y,dim=2), 7) :: k               
        real, dimension(size(y,dim=1), size(y,dim=2)) :: esti_err_y 
        real :: s
    
            k(:,:,1) = h*f(c, x)
            k(:,:,2) = h*f(c, x + a21*k(:,:,1)) 
            k(:,:,3) = h*f(c, x + a31*k(:,:,1) + a32*k(:,:,2)) 
            k(:,:,4) = h*f(c, x + a41*k(:,:,1) + a42*k(:,:,2) + a43*k(:,:,3))
            k(:,:,5) = h*f(c, x + a51*k(:,:,1) + a52*k(:,:,2) + a53*k(:,:,3) + a54*k(:,:,4))
            k(:,:,6) = h*f(c, x + a61*k(:,:,1) + a62*k(:,:,2) + a63*k(:,:,3) + a64*k(:,:,4) + a65*k(:,:,5))
            k(:,:,7) = h*f(c, x + a71*k(:,:,1) + a73*k(:,:,3) + a74*k(:,:,4) + a75*k(:,:,5) + a76*k(:,:,6))       !a72=0.0
    
            y = y0 + b1*k(:,:,1) + b3*k(:,:,3) + b4*k(:,:,4) + b5*k(:,:,5) + b6*k(:,:,6)                          !b2=0.0
    
            esti_err_y = e1*k(:,:,1) + e3*k(:,:,3) + e4*k(:,:,4) + e5*k(:,:,5) + e6*k(:,:,6) + e7*k(:,:,7)        !e2=0.0
    
            err = maxval(abs(esti_err_y))
            s = ((tol*h)/(2.0*err))**(1.0/5)
            hopt = s*h

    end subroutine rkdp_fcx
       
end module dormand_prince
!===========================================================