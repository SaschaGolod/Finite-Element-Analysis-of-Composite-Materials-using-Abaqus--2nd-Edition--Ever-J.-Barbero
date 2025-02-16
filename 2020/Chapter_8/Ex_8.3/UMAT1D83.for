      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,                 &
     & RPL,DDSDDT,DRPLDE,DRPLDT,STRAN,DSTRAN,                           &
     & TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,MATERL,NDI,NSHR,NTENS,        &
     & NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,CELENT,                   &
     & DFGRD0,DFGRD1,NOEL,NPT,KSLAY,KSPT,KSTEP,KINC)

!     Copyright (2007,2012,2021) Ever J. Barbero, Abaqus Ex. 8.3

      INCLUDE 'ABA_PARAM.INC'

      PARAMETER (EPS=2.22D-16) !SMALLEST NUMBER REAL*8 CAN STORE
      
      CHARACTER*80 MATERL
      DIMENSION STRESS(NTENS),STATEV(NSTATV),                           &
     & DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),                 &
     & STRAN(NTENS),DSTRAN(NTENS),TIME(2),PREDEF(1),DPRED(1),           &
     & PROPS(NPROPS),COORDS(3),DROT(3,3),                               &
     & DFGRD0(3,3),DFGRD1(3,3)

! -----------------------------------------------------------
!     UMAT FOR 1D, 2D, 3D SOLID ELEMENTS
!     F77 IMPLICIT NAME CONVENTION, F95 FREE FORMATTING
! -----------------------------------------------------------
!     NDI: # of direct components (11,...) of DDSDDE, DDSDDT, and DRPLDE
!     NSHR: # of engineering shear components (12,...) 
!                                          of DDSDDE, DDSDDT, and DRPLDE
!     NTENS = NDI + NSHR: Size of the stress or strain component array
!     TIME(1): Value of step time at the beginning of current increment.
!     TIME(2): Value of total time at the beginning of current increment.
!     DTIME  : Time increment.
!     STRESS(NTENS):  passed in as the stress tensor at the beginning of 
!                     the increment, must be updated.
! -----------------------------------------------------------
!23456
!     ************ User defined part *************************************
      DOUBLE PRECISION E, m, delta_alpha 
      DOUBLE PRECISION gamma_hat, D 
      DOUBLE PRECISION sigma_b, C 
      keycut   = 0

!     Recover state variables
      gamma_hat = statev(1)
      D = statev(2)

!     get Properties, and Damage model parameters
      E           = props(1)  ! Elastic modulus
      m           = props(2)  ! Weibul shape parameter 
      delta_alpha = props(3)  !parameter 

!     compute effective stress  
      sigma_b = E * (STRAN(1) + DSTRAN(1))

!     update gamma_hat 
      gamma_hat = max (gamma_hat, sigma_b)    

!     calculate D and secant stiffness 1D 
      D       = 1 - dexp(-delta_alpha*gamma_hat**m)
      C       = dexp(-delta_alpha*gamma_hat**m)*E

!     calculate the apparent stress *** output: S11
      STRESS(1)= (1-D) * E * (STRAN(1) + DSTRAN(1))  ! see alternative below

!     INITIALIZE THE TANGENT STIFFNESS
      DO K1=1,NTENS
        DO K2=1,NTENS
           DDSDDE(K1,K2)=0.0D0
        ENDDO
      ENDDO
      
!     CALCULATE THE TANGENT STIFFNESS
      IF (NDI.EQ.1) THEN
        if (gamma_hat.eq.statev(1)) then  ! gamma_hat did not change
          DDSDDE(1,1)=C
        else  ! gamma_hat did change
          DDSDDE(1,1)=(1 - delta_alpha*m*gamma_hat**m)  &
     &                *dexp(-delta_alpha*gamma_hat**m)*E 
        endif 
      ELSEIF (NDI.EQ.2) THEN
        write(*,*) "NDI=2 not implemented"
        call xit
!       DO NOT DELETE
!       left over from Ex. 3.14 for later generalizing to 2D        
!       PR21    = PR12*E2/E1
!        DDSDDE(1,1)    = -1/(-E1+PR12**2.*E2)*E1**2.
!       DDSDDE(1,2) = -PR12*E1/(-E1+PR12**2.*E2)*E2
!        DDSDDE(2,1)    = DDSDDE(1,2)
!        DDSDDE(2,2)    = -E1/(-E1+PR12**2.*E2)*E2
!        DDSDDE(3,3)    = G12
!        IF (NSHR.GT.1) THEN
!          DDSDDE(4,4) = G13
!          DDSDDE(5,5) = G23
      ELSEIF (NDI.EQ.3) THEN
        write(*,*) "NDI=3 not implemented"
        call xit
!       DO NOT DELETE
!       left over from Ex. 7.7 for later generalizing to 3D
!       calculate stiffness 3D stiffness
!       PR21    = PR12*E2/E1
!       PR13    = PR12
!       PR31    = PR21
!       PR32    = PR23
!       DDSDDE(1,1) = E1**2*(PR23-1)/(E1*PR23-E1+2*PR12**2*E2)
!       DDSDDE(1,2) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)
!       DDSDDE(1,3) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)
!       DDSDDE(2,1) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)      
!       DDSDDE(2,2) = E2*(-E1+PR12**2*E2)/(-E1+E1*PR23**2+2*PR12**2*E2     &
!     & +2*PR12**2*E2*PR23)      
!       DDSDDE(2,3) = -E2*(E1*PR23+PR12**2*E2)/(-E1+E1*PR23**2             &
!     &  +2*PR12**2*E2+2*PR12**2*E2*PR23)      
!       DDSDDE(3,1) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)      
!       DDSDDE(3,2) = -E2*(E1*PR23+PR12**2*E2)/(-E1+E1*PR23**2             &
!     &  +2*PR12**2*E2+2*PR12**2*E2*PR23)      
!       DDSDDE(3,3) = E2*(-E1+PR12**2*E2)/(-E1+E1*PR23**2+2*PR12**2*E2     &
!     &  +2*PR12**2*E2*PR23)      
!       DDSDDE(4,4) = G12   !Abaqus notation
!       DDSDDE(5,5) = G12   !G13
!       DDSDDE(6,6) = G23   !Abaqus notation
      ELSE
        WRITE (6,3)
      ENDIF
 3    FORMAT(1x,'NDI VALUE NOT IMPLEMENTED')

!     DO NOT DELETE
!     UPDATE THE STRESS FOR ANY VALUE OF NTENS for later generalizing to 3D
!      DO K1=1,NTENS
!        STRESS(K1)=0.0D0
!        DO K2=1,NTENS
!           STRESS(K1)=STRESS(K1)+DDSDDE(K2,K1)*(STRAN(K2)+DSTRAN(K2))
!        ENDDO
!      ENDDO
!     STRESS(1)= STRESS(1) + DDSDDE(1,1)*DSTRAN(1)  ! alternative
        
!     Update state variables
      statev(1) = gamma_hat !effective stress, output: SDV1
      statev(2) = D         !damage          , output: SDV2

      RETURN
      END