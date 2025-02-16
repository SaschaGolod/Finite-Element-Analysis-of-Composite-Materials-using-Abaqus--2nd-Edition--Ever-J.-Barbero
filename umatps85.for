      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,                 &
     & RPL,DDSDDT,DRPLDE,DRPLDT,STRAN,DSTRAN,                           &
     & TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,MATERL,NDI,NSHR,NTENS,        &
     & NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,CELENT,                   &
     & DFGRD0,DFGRD1,NOEL,NPT,KSLAY,KSPT,KSTEP,KINC)

!     Copyright (c) 2007, 2012, Ever J. Barbero, http://www.mae.wvu.edu/barbero/
!     Abaqus Ex. 8.5
!     ERRATA 2007 has been incorporated into umatps85.for

      INCLUDE 'ABA_PARAM.INC'

      PARAMETER (EPS8=2.22D-16) !SMALLEST NUMBER REAL*8
      
      CHARACTER*80 MATERL
      DIMENSION STRESS(NTENS),STATEV(NSTATV),                           &
     & DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),                 &
     & STRAN(NTENS),DSTRAN(NTENS),TIME(2),PREDEF(1),DPRED(1),           &
     & PROPS(NPROPS),COORDS(3),DROT(3,3),                               &
     & DFGRD0(3,3),DFGRD1(3,3)

!      A = 1.
!      EPS   = EPSILON(A)        !NEGLIGIBLE COMPARED TO 1.0, SAME TYPE AS A
!      TINY2 = TINY(A)           !SMALLEST NUMBER OF SAME TYPE AS A
!      HUGE2 = HUGE(A)           !LARGEST NUMBER OF SAME TYPE AS A
! -----------------------------------------------------------
!      UMAT FOR 3D SOLID ELEMENTS
!      IMPLICIT NAME CONVENTION
! -----------------------------------------------------------
!      NDI: # of direct components (11,...) of DDSDDE, DDSDDT, and DRPLDE
!      NSHR: # of engineering shear components (12,...) of DDSDDE, DDSDDT, and DRPLDE
!      NTENS = NDI + NSHR: Size of the stress or strain component array
!      TIME(1):    Value of step time at the beginning of the current increment.
!      TIME(2):    Value of total time at the beginning of the current increment.
!      DTIME:      Time increment.
!      STRESS(NTENS):  passed in as the stress tensor at the beginning of the increment
!                      must be updated to be the stress tensor at the end of the increment
! -----------------------------------------------------------

!      user defined variables
!      conv: convergence flag
!      k: iteration #
!      kmax: max. # of iterations allowed
!      ncomp: # of inplane components of stress = 3           
!      tol: tolerance for the damage criterion

       INTEGER          i, j, conv, k, kmax, ncomp/3/
       DOUBLE PRECISION tol/1.0D-3/
       DOUBLE PRECISION E1, E2, nu12, nu21, G12 , nu23, G23 
       DOUBLE PRECISION D2, D6, sigma1, sigma2, sigma6 , Y2s, Y6s
       DOUBLE PRECISION eps1, eps2, eps6
       DOUBLE PRECISION C(3,3), Y(3), df_dY(3), eps(3)
       DOUBLE PRECISION F2t, F6, GIc, GIIc, gamma0, c1, c2 
       DOUBLE PRECISION gamma1, delta, dgamma_ddelta
       DOUBLE PRECISION g, g_hat, lambda, prod

!     INITIALIZE THE TANGENT STIFFNESS
      DDSDDE = 0.0D0
      
!     CALCULATE THE TANGENT STIFFNESS
      IF (NDI.EQ.1) THEN
        write(*,*) "NDI=1 not implemented"
        call xit
      ELSEIF (NDI.EQ.2) THEN
!       STEPS are numbered after Section 8.4.1 in the textbook
!       Eqs. for Ex. 8.5 are taken from Ex. 8.4 in the textbook      
!       STEP 1. set up strains in tensor notation
        eps = STRAN(1:3) + DSTRAN(1:3)
        eps(3)  = eps(3)/2.;   ! use tensorial notation for shear
        eps1 = eps(1)
        eps2 = eps(2)
        eps6 = eps(3)
!       STEP 2. recover state variables and properties 
!       Recover state variables
        delta = statev(1)
        D2    = statev(2)
        D6    = statev(3)  
!       get the elastic properties and damage model parameters
        E1      = props(1)
        E2      = props(2)
        nu12    = props(3)
        nu23    = props(4)   ! Not used for plane stress
        G12     = props(5)
        G13     = G12
        G23     = props(6)   ! Not used for plane stress
        nu21    = nu12*E2/E1
        F2t     = props(7)   ! Strength 2 tension
        F6      = props(8)   ! Strength 12 shear
        GIc     = props(9)  
        GIIc    = props(10) 
        c1      = props(11) 
        c2      = props(12) 
        gamma0  = props(13) 
!       START the RETURN MAPPING ALGORITHM
        conv = 0
        k = 0
        kmax = 1000
        do while (conv.eq.0)
!           STEP 3. compute thermodynamic forces and damage hardening
!           calculate secant stiffness 2D (plane stress) as a f. of current damage
            C      = 0
            C(1,1) = -E1 / (nu21 * nu12 - 1)
            C(1,2) = (-1 + D2) * E2 * nu12 / (nu21 * nu12 - 1)
            C(2,1) = E1 * (-1 + D2) * nu21 / (nu21 * nu12 - 1)
            C(2,2) = -(-1 + D2) ** 2 * E2 / (nu21 * nu12 - 1)
            C(3,3) = 2 * G12* (-1 + D6) ** 2 !incorporates ERRATA 2007
!!           calculate the Cauchy stress using the current secant stiffness 
            STRESS = matmul(c,eps)
            sigma1 = STRESS(1)
            sigma2 = STRESS(2)
            sigma6 = STRESS(3)
!           calculate the thermodinamic loads Y1, Y2 and Y6 as function of Cauchy stresses
            Y(1) = 0
            Y(2) = sigma2 ** 2 / (1 - D2) ** 3 / E2 - nu12 / E1 /       &
     &              (1 - D2)** 2 * sigma1 * sigma2
            Y(3) = sigma6 ** 2 / (1 - D6) ** 3 / 2 / G12 !incorporates ERRATA 2007
            Y2s = Y(2)
            Y6s = Y(3)
!           evalutate gamma
            gamma1 = c1 * (dexp(delta / c2) - 1.0D0)
!           STEP 4. compute damage surface
!           evaluate damage surface g
            if (Y2s+Y6s.ge.0.0) then
                g_hat = dsqrt(((1 - GIc / GIIc) * Y2s * E2 / F2t ** 2 + &
     &              GIc / GIIc * Y2s ** 2 * E2 ** 2 / F2t ** 4 + Y6s ** &
     &              2 * G12 ** 2 / F6**4))
            else
                g_hat = 0
            endif
            g =  g_hat - gamma1 - gamma0
!           elastic (load or unload) or inelastic load (new damage) 
            if (g.le.tol) then
                conv = 1
            else
                k = k  + 1 
!               STEP 5. compute lambda multiplier
!               compute dg_dY*dY_dD*df_dY
                prod = dble(1 / ((1 - GIc / GIIc) * Y2s * E2 / F2t ** 2 + GIc     &
                / GIIc * Y2s ** 2 * E2 ** 2 / F2t ** 4 + Y6s ** 2 * G12 ** 2 / F6 &
                ** 4) * ((1 - GIc / GIIc) * E2 / F2t ** 2 + 2 * GIc / GIIc * Y2s *&
                E2 ** 2 / F2t ** 4) ** 2 * (-nu12 ** 2 * sigma2 / E1 / (-1 + D2)  &
                ** 2 * E2 / (nu21 * nu12 - 1) * eps2 + (2 * sigma2 / (1 - D2) ** 3&
                / E2 - nu12 / E1 / (1 - D2) ** 2 * sigma1) * (E1 * nu21 / (nu21 * &
                nu12 - 1) * eps1 - 2 * (-1 + D2) * E2 / (nu21 * nu12 - 1) * eps2) &
                )) / 0.4D1 + dble(32 / ((1 - GIc / GIIc) * Y2s * E2 / F2t ** 2 + GIc&
                / GIIc * Y2s ** 2 * E2 ** 2 / F2t ** 4 + Y6s ** 2 * G12 ** 2 /    &
                F6 ** 4) * Y6s ** 2 * G12 ** 4 / F6 ** 8 * sigma6 / (1 - D6) ** 3 &
                * (-1 + D6) * eps6)
!               compute dgamma_ddelta
                dgamma_ddelta=c1/c2*dexp(delta/c2)
                lambda = - g / (prod + dgamma_ddelta)
!               STEP 6. update internal variables
!               compute df_dY
                df_dY(2) = (((1 - GIc / GIIc) * Y2s * E2 / F2t ** 2 + GIc / GIIc  &
                * Y2s ** 2 * E2 ** 2 / F2t ** 4 + Y6s ** 2 * G12 ** 2 / F6 ** 4   &
                ) ** (-0.1D1 / 0.2D1) * ((1 - GIc / GIIc) * E2 / F2t ** 2 + 2 * GIc&
                / GIIc * Y2s * E2 ** 2 / F2t ** 4)) / 0.2D1

                df_dY(3) = ((1 - GIc / GIIc) * Y2s * E2 / F2t ** 2 + GIc / GIIc * &
                Y2s ** 2 * E2 ** 2 / F2t ** 4 + Y6s ** 2 * G12 ** 2 / F6 ** 4) ** &
                (-0.1D1 / 0.2D1) * Y6s * G12 ** 2 / F6 ** 4
              
!               update the damage state variables
                delta = delta - lambda
                D2 = D2 + lambda * df_dY(2) 
                D6 = D6 + lambda * df_dY(3)  ! df_dY(3)=df/dY6
            endif
            if (k.ge.kmax) then !RMA did not converge
                write(*,*) "*** ERROR: RMA in UMATPS85 did not converge ***"
                call XIT
            endif
!           STEP 7 . end linearized process
        enddo

!       STEP 8. compute tangent stiffness matrix. 
!       For now, use the secant as tangent, although this is a problem for Abaqus
!       Instead, we should use eq. (8.111) and step 8 in Sect. 8.4.1 
        DDSDDE(1:3,1:3) = C
        DDSDDE(3,3) = C(3,3)/2  ! come back to engineering notation
        IF (NSHR.GT.1) THEN !shells
          DDSDDE(4,4) = G13 !out-of plane do not damage, Abaqus notation
          DDSDDE(5,5) = G23 !out-of plane do not damage, see Table 1.1 (2007)
          STRESS(4) = G13 * ( STRAN(4) + DSTRAN(4) )
          STRESS(5) = G23 * ( STRAN(5) + DSTRAN(5) )
        ENDIF

!       STEP 9. Update the stress and state variables
!       inplane stresses computed inside the RMA are current and out-of-plane values are updated above
!!!       STRESS = STRESS + MATMUL(DDSDDE,DSTRAN)         
!       Update state variables
        statev(1) = delta
        statev(2) = D2
        statev(3) = D6

      ELSEIF (NDI.EQ.3) THEN
        write(*,*) "NDI=3 not implemented"
        call xit
      ELSE
        WRITE (6,"(1x,'NDI VALUE NOT IMPLEMENTED')")
      ENDIF

      RETURN
      END