!> @brief Método Runge-kutta-Fehlberg

!Tabela de Butcher referente ao respectivo método
 !________________________________________________
 !c1=(0.0)   |
 !c2=(1.0/6) | a21=(1.0/6)
 !c3=(4.0/15)| a31=(4.0/75)    a32=(16.0/75)
 !c4=(2.0/3) | a41=(5.0/6)     a42=(-8.0/3)   a43=(5.0/2)
 !c5=(4.0/5) | a51=(-8.0/5)    a52=(144.0/25) a53=(-4.0)        a54=(16.0/25)
 !c6=(1.0)   | a61=(361.0/320) a62=(-18.0/5)  a63=(407.0/128)   a64=(-11.0/80)  a65=(55.0/128)
 !c7=(0.0)   | a71=(-11.0/640) a72=(0.0)      a73=(11.0/256)    a74=(-11.0/160) a75=(11.0/256)   a76=(0.0)
 !c8=(1.0)   | a81=(93.0/640)  a82=(-18.0/5)  a83=(803.0/256)   a84=(-11.0/160) a85=(99.0/256)   a86=(0.0)    a87=(1.0)
 !           |----------------------------------------------------------------------------------------------------------------------------
 !           |  b1=(31.0/384)   b2=(0.0)       b3=(1125.0/2816)  b4=(9.0/32)     b5=(125.0/768)   b6=(5.0/66)  b7=(0.0)
 !           |  d1=(7.0/1408)   d2=(0.0)       d3=(1125.0/2816)  d4=(9.0/32)     d5=(125.0/768)   d6=(0.0)     d7=(5.0/66)  d8=(5.0/66)
 !           |----------------------------------------------------------------------------------------------------------------------------
 !           |  e1=(-5.0/66)    e2=(0.0)       e3=(0.0)          e4=(0.0)        e5=(0.0)         e6=(-5.0/66) e7=(5.0/66)  e8=(5.0/66)
 !________________________________________________

!==========================================================
module fehlberg

    implicit none

    private
    public :: rkfb_fx, rkfb_fcx

    real, parameter :: c1=(0.0), c2=(1.0/6), c3=(4.0/15), c4=(2.0/3), c5=(4.0/5), c6=(1.0), c7=(0.0), &
                       c8=(1.0)

    real, parameter :: a21=(1.0/6), a31=(4.0/75), a32=(16.0/75), a41=(5.0/6), a42=(-8.0/3), &
                       a43=(5.0/2), a51=(-8.0/5), a52=(144.0/25), a53=(-4.0), a54=(16.0/25), &
                       a61=(361.0/320), a62=(-18.0/5), a63=(407.0/128), a64=(-11.0/80), &
                       a65=(55.0/128), a71=(-11.0/640), a72=(0.0), a73=(11.0/256), a74=(-11.0/160), &
                       a75=(11.0/256), a76=(0.0), a81=(93.0/640), a82=(-18.0/5), a83=(803.0/256), &
                       a84=(-11.0/160), a85=(99.0/256), a86=(0.0), a87=(1.0)

    real, parameter :: b1=(31.0/384), b2=(0.0), b3=(1125.0/2816), b4=(9.0/32), b5=(125.0/768), &
                       b6=(5.0/66), b7=(0.0)

    real, parameter :: d1=(7.0/1408), d2=(0.0), d3=(1125.0/2816), d4=(9.0/32), d5=(125.0/768), &
                       d6=(0.0), d7=(5.0/66), d8=(5.0/66)

    real, parameter :: e1=(-5.0/66), e2=(0.0), e3=(0.0), e4=(0.0), e5=(0.0), e6=(-5.0/66), &
                       e7=(5.0/66), e8=(5.0/66)  
    
contains

    subroutine rkfb_fx(f, x, y0, h, tol, y, err, hopt)

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
            k(:,:,7) = h*f(x + a71*k(:,:,1) + a73*k(:,:,3) + a74*k(:,:,4) + a75*k(:,:,5))                                     !a72=0.0, a76=0.0
            k(:,:,8) = h*f(x + a81*k(:,:,1) + a82*k(:,:,2) + a83*k(:,:,3) + a84*k(:,:,4) + a85*k(:,:,5) + a87*k(:,:,7))       !a86=0.0


            y = y0 + b1*k(:,:,1) + b3*k(:,:,3) + b4*k(:,:,4) + b5*k(:,:,5) + b6*k(:,:,6)                                    !b2=0.0, b7=0.0

            esti_err_y = e1*k(:,:,1) + e6*k(:,:,6) + e7*k(:,:,7) + e8*k(:,:,8)                                              !e2=0.0, e3=0.0, e4=0.0, e5=0.0

            err = maxval(abs(esti_err_y))
            s = ((tol*h)/(2.0*err))**(1.0/5)
            hopt = s*h

    end subroutine rkfb_fx

    subroutine rkfb_fcx(f, c, x, y0, h, tol, y, err, hopt)

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
        real:: s

            k(:,:,1) = h*f(c, x)
            k(:,:,2) = h*f(c, x + a21*k(:,:,1)) 
            k(:,:,3) = h*f(c, x + a31*k(:,:,1) + a32*k(:,:,2)) 
            k(:,:,4) = h*f(c, x + a41*k(:,:,1) + a42*k(:,:,2) + a43*k(:,:,3))
            k(:,:,5) = h*f(c, x + a51*k(:,:,1) + a52*k(:,:,2) + a53*k(:,:,3) + a54*k(:,:,4))
            k(:,:,6) = h*f(c, x + a61*k(:,:,1) + a62*k(:,:,2) + a63*k(:,:,3) + a64*k(:,:,4) + a65*k(:,:,5))
            k(:,:,7) = h*f(c, x + a71*k(:,:,1) + a73*k(:,:,3) + a74*k(:,:,4) + a75*k(:,:,5))                                      !a72=0.0, a76=0.0
            k(:,:,8) = h*f(c, x + a81*k(:,:,1) + a82*k(:,:,2) + a83*k(:,:,3) + a84*k(:,:,4) + a85*k(:,:,5) + a87*k(:,:,7))        !a86=0.0


            y = y0 + b1*k(:,:,1) + b3*k(:,:,3) + b4*k(:,:,4) + b5*k(:,:,5) + b6*k(:,:,6)                                        !b2=0.0, b7=0.0

            esti_err_y = e1*k(:,:,1) + e6*k(:,:,6) + e7*k(:,:,7) + e8*k(:,:,8)                                                  !e2=0.0, e3=0.0, e4=0.0, e5=0.0

            err = maxval(abs(esti_err_y))
            s = ((tol*h)/(2.0*err))**(1.0/5)
            hopt = s*h

    end subroutine rkfb_fcx

end module fehlberg
!==========================================================