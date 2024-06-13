!> @brief Módulo que define às equçãoes diferencias envolvidas mo problema

!===========================================================
module edo_nbody
    
    implicit none

    private
    public :: G_eft, f, g

    real :: G_eft
    
contains

    pure function f(v) result(r)
        real, dimension(:,:), intent(in) :: v
        real, dimension(size(v,dim=1), size(v,dim=2)) :: r

            r = v

    end function f

    pure function g(m,r) result(a)
        real, dimension(:), intent(in) :: m
        real, dimension(:,:), intent(in) :: r
        real, dimension(size(r,dim=1),size(r,dim=2)) :: a
        integer :: nbody
        integer :: i, j

        nbody = size(r, dim=2)
        a = real(0)

        do concurrent(i=1:nbody, j=1:nbody, i/=j)
            a(:,i) = a(:,i) + G_eft*m(j)*(r(:,j) - r(:,i))/(SQRT(DOT_PRODUCT(r(:,j) - r(:,i), r(:,j) - r(:,i))))**3
        end do

    end function g
    
end module edo_nbody
!===========================================================
