!> @brief Método Runge-kutta-Verner

!Tabela de Butcher referente ao respectivo método
 !________________________________________________
 !c1=(0.0)    |
 !c2=(1.0/18) | a21=(1.0/18)
 !c3=(1.0/6)  | a31=(-1.0/12)     a32=(1.0/4)
 !c4=(2.0/9)  | a41=(-2.0/81)     a42=(4.0/27)    a43=(8.0/81)
 !c5=(2.0/3)  | a51=(40.0/33)     a52=(-4.0/11)   a53=(-56.0/11)    a54=(54.0/11)
 !c6=(1.0)    | a61=(-329.0/73)   a62=(72.0/73)   a63=(5380.0/219)  a64=(-12285.0/584) a65=(2695.0/1752)
 !c7=(8.0/9)  | a71=(-8716.0/891) a72=(656.0/297) a73=(39520.0/891) a74=(-416.0/11)    a75=(52.0/27)     a76=(0.0)
 !c8=(1.0)    | a81=(3015.0/256)  a82=(-9.0/4)    a83=(-4219.0/78)  a84=(5985.0/128)   a85=(-539.0/384)  a86=(0.0)       a87=(693.0/3328)
 !            |----------------------------------------------------------------------------------------------------------------------------
 !            |  b1=(3.0/80)       b2=(0.0)        b3=(4.0/25)       b4=(243.0/1120)    b5=(77.0/160)     b6=(73.0/700)   b7=(0.0)
 !            |  d1=(57.0/640)     d2=(0.0)        d3=(-16.0/65)     d4=(1377.0/2240)   d5=(121.0/320)    d6=(0.0)        d7=(891.0/8320)  d8=(2.0/25)
 !            |----------------------------------------------------------------------------------------------------------------------------
 !            |  e1=(33.0/640)     e2=(0.0)        e3=(-132.0/325)   e4=(891.0/2240)    e5=(-33.0/320)    e6=(-73.0/700)  e7=(891.0/8320)  e8=(2.0/35)
 !________________________________________________

!==========================================================
module verner

    implicit none

    private
    public :: rkvn_fx, rkvn_fcx

    real, parameter :: c1=(0.0), c2=(1.0/18), c3=(1.0/6), c4=(2.0/9), c5=(2.0/3), c6=(1.0), c7=(8.0/9), &
                       c8=(1.0)

    real, parameter :: a21=(1.0/18), a31=(-1.0/12), a32=(1.0/4), a41=(-2.0/81), a42=(4.0/27), &
                       a43=(8.0/81), a51=(40.0/33), a52=(-4.0/11), a53=(-56.0/11), a54=(54.0/11), &
                       a61=(-329.0/73), a62=(72.0/73), a63=(5380.0/219), a64=(-12285.0/584), &
                       a65=(2695.0/1752), a71=(-8716.0/891), a72=(656.0/297), a73=(39520.0/891), &
                       a74=(-416.0/11), a75=(52.0/27), a76=(0.0), a81=(3015.0/256), a82=(-9.0/4), &
                       a83=(-4219.0/78), a84=(5985.0/128), a85=(-539.0/384), a86=(0.0), a87=(693.0/3328)

    real, parameter :: b1=(3.0/80), b2=(0.0), b3=(4.0/25), b4=(243.0/1120), b5=(77.0/160), b6=(73.0/700), &
                       b7=(0.0)

    real, parameter :: d1=(57.0/640), d2=(0.0), d3=(-16.0/65), d4=(1377.0/2240), d5=(121.0/320), d6=(0.0), &
                       d7=(891.0/8320), d8=(2.0/25)

    real, parameter :: e1=(33.0/640), e2=(0.0), e3=(-132.0/325), e4=(891.0/2240), e5=(-33.0/320), &
                       e6=(-73.0/700), e7=(891.0/8320), e8=(2.0/35)
    
contains

    subroutine rkvn_fx(f, x, y0, h, tol, y, err, hopt)

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
        real, intent(out) :: hopt
        real, intent(out) :: err
        real, dimension(size(y,dim=1), size(y,dim=2), 8) :: k               
        real, dimension(size(y,dim=1), size(y,dim=2)) :: esti_err_y 
        real:: s

            k(:,:,1) = h*f(x)
            k(:,:,2) = h*f(x + a21*k(:,:,1)) 
            k(:,:,3) = h*f(x + a31*k(:,:,1) + a32*k(:,:,2)) 
            k(:,:,4) = h*f(x + a41*k(:,:,1) + a42*k(:,:,2) + a43*k(:,:,3))
            k(:,:,5) = h*f(x + a51*k(:,:,1) + a52*k(:,:,2) + a53*k(:,:,3) + a54*k(:,:,4))
            k(:,:,6) = h*f(x + a61*k(:,:,1) + a62*k(:,:,2) + a63*k(:,:,3) + a64*k(:,:,4) + a65*k(:,:,5))
            k(:,:,7) = h*f(x + a71*k(:,:,1) + a72*k(:,:,2) + a73*k(:,:,3) + a74*k(:,:,4) + a75*k(:,:,5))                      !a76=0.0
            k(:,:,8) = h*f(x + a81*k(:,:,1) + a82*k(:,:,2) + a83*k(:,:,3) + a84*k(:,:,4) + a85*k(:,:,5) + a87*k(:,:,7))       !a86=0.0

            y = y0 + b1*k(:,:,1) + b3*k(:,:,3) + b4*k(:,:,4) + b5*k(:,:,5) + b6*k(:,:,6)                                      !b2=0.0, b7=0.0

            esti_err_y = e1*k(:,:,1) + e3*k(:,:,3) + e4*k(:,:,4) + e5*k(:,:,5) + e6*k(:,:,6) + e7*k(:,:,7) + e8*k(:,:,8)      !e2=0.0

            err = maxval(abs(esti_err_y))
            s = ((tol*h)/(2.0*err))**(1.0/5)
            hopt = s*h

    end subroutine rkvn_fx


    subroutine rkvn_fcx(f, c, x, y0, h, tol, y, err, hopt)

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
        real, intent(out) :: hopt
        real, intent(out) :: err
        real, dimension(size(y,dim=1), size(y,dim=2), 8) :: k               
        real, dimension(size(y,dim=1), size(y,dim=2)) :: esti_err_y 
        real :: s

            k(:,:,1) = h*f(c, x)
            k(:,:,2) = h*f(c, x + a21*k(:,:,1)) 
            k(:,:,3) = h*f(c, x + a31*k(:,:,1) + a32*k(:,:,2)) 
            k(:,:,4) = h*f(c, x + a41*k(:,:,1) + a42*k(:,:,2) + a43*k(:,:,3))
            k(:,:,5) = h*f(c, x + a51*k(:,:,1) + a52*k(:,:,2) + a53*k(:,:,3) + a54*k(:,:,4))
            k(:,:,6) = h*f(c, x + a61*k(:,:,1) + a62*k(:,:,2) + a63*k(:,:,3) + a64*k(:,:,4) + a65*k(:,:,5))
            k(:,:,7) = h*f(c, x + a71*k(:,:,1) + a72*k(:,:,2) + a73*k(:,:,3) + a74*k(:,:,4) + a75*k(:,:,5))                      !a76=0.0
            k(:,:,8) = h*f(c, x + a81*k(:,:,1) + a82*k(:,:,2) + a83*k(:,:,3) + a84*k(:,:,4) + a85*k(:,:,5) + a87*k(:,:,7))       !a86=0.0

            y = y0 + b1*k(:,:,1) + b3*k(:,:,3) + b4*k(:,:,4) + b5*k(:,:,5) + b6*k(:,:,6)                                         !b2=0.0, b7=0.0

            esti_err_y = e1*k(:,:,1) + e3*k(:,:,3) + e4*k(:,:,4) + e5*k(:,:,5) + e6*k(:,:,6) + e7*k(:,:,7) + e8*k(:,:,8)         !e2=0.0

            err = maxval(abs(esti_err_y))
            s = ((tol*h)/(2.0*err))**(1.0/5)
            hopt = s*h

    end subroutine rkvn_fcx

end module verner
!==========================================================