      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,                 &
     & RPL,DDSDDT,DRPLDE,DRPLDT,STRAN,DSTRAN,                           &
     & TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,MATERL,NDI,NSHR,NTENS,        &
     & NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,CELENT,                   &
     & DFGRD0,DFGRD1,NOEL,NPT,KSLAY,KSPT,KSTEP,KINC)

!     COPYRIGHT (2012) EVER J. BARBERO, ALL RIGHTS RESERVED
!     EX. 7.5 Finite Element Analysis of Composite Materials with Abaqus

      INCLUDE 'ABA_PARAM.INC'

      PARAMETER (EPS=2.22D-16) !SMALLEST NUMBER REAL*8 CAN STORE
      
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
!     UMAT FOR 3D SOLID ELEMENTS
!     F77 IMPLICIT NAME CONVENTION
! -----------------------------------------------------------
!       NDI: # of direct components (11,...) of DDSDDE, DDSDDT, and DRPLDE
!       NSHR: # of engineering shear components (12,...) of DDSDDE, DDSDDT, and DRPLDE
!       NTENS = NDI + NSHR: Size of the stress or strain component array
!       TIME(1):    Value of step time at the beginning of the current increment.
!       TIME(2):    Value of total time at the beginning of the current increment.
!       DTIME:      Time increment.
!       STRESS(NTENS):  passed in as the stress tensor at the beginning of the increment
!                       must be updated to be the stress tensor at the end of the increment
! -----------------------------------------------------------

      E1o      	= PROPS(1)
      E2o		= PROPS(2)
      E3o       = E2o
      PR12o	    = PROPS(3)
      PR13o     = PR12o
      PR23o     = PROPS(4)	
      G12o      = PROPS(5)
      G13o      = G12o
      G23o      = E2o/2/(1.+PR23o)
	
      tau1	= props(7)
      tau2	= props(8)
      tau12	= props(9)
      tau23	= props(10)

!     Maxwell model
      E1 = E1o*dexp(-(Time(2)+DTime)/tau1)
      E2 = E2o*dexp(-(Time(2)+DTime)/tau2)
      G12 = G12o*dexp(-(Time(2)+DTime)/tau12)
      G23 = G23o*dexp(-(Time(2)+DTime)/tau23)
      PR12 = PR12o
      PR23 = PR23o

!     ELASTIC STIFFNESS

      DO K1=1,NTENS
        DO K2=1,NTENS
           DDSDDE(K1,K2)=0.0D0
        ENDDO
      ENDDO
      
      IF (NDI.EQ.2) THEN
!       PR21	= PR12*E2/E1
        DDSDDE(1,1)	= -1/(-E1+PR12**2.*E2)*E1**2.
	    DDSDDE(1,2)	= -PR12*E1/(-E1+PR12**2.*E2)*E2
        DDSDDE(2,1)	= DDSDDE(1,2)
        DDSDDE(2,2)	= -E1/(-E1+PR12**2.*E2)*E2
        DDSDDE(3,3)	= G12
        IF (NSHR.GT.1) THEN
          DDSDDE(4,4) = G13
          DDSDDE(5,5) = G23
        ENDIF
      ELSEIF (NDI.EQ.3) THEN
!       calculate stiffness 3D stiffness
!	    PR21	= PR12*E2/E1
!	    PR13	= PR12
!	    PR31	= PR21
!	    PR32	= PR23
	    DDSDDE(1,1) = E1**2*(PR23-1)/(E1*PR23-E1+2*PR12**2*E2)
	    DDSDDE(1,2) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)
	    DDSDDE(1,3) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)
	    DDSDDE(2,1) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)      
	    DDSDDE(2,2) = E2*(-E1+PR12**2*E2)/(-E1+E1*PR23**2+2*PR12**2*E2     &
     & +2*PR12**2*E2*PR23)      
	    DDSDDE(2,3) = -E2*(E1*PR23+PR12**2*E2)/(-E1+E1*PR23**2             &
     &  +2*PR12**2*E2+2*PR12**2*E2*PR23)      
	    DDSDDE(3,1) = -E2*E1*PR12/(E1*PR23-E1+2*PR12**2*E2)      
	    DDSDDE(3,2) = -E2*(E1*PR23+PR12**2*E2)/(-E1+E1*PR23**2             &
     &  +2*PR12**2*E2+2*PR12**2*E2*PR23)      
	    DDSDDE(3,3) = E2*(-E1+PR12**2*E2)/(-E1+E1*PR23**2+2*PR12**2*E2     &
     &  +2*PR12**2*E2*PR23)      
	    DDSDDE(4,4)	= G12   !Abaqus notation
	    DDSDDE(5,5)	= G12   !G13
	    DDSDDE(6,6)	= G23   !Abaqus notation
      ELSE
        WRITE (6,3)
      ENDIF
 3    FORMAT(1x,'NDI VALUE NOT IMPLEMENTED')

!     CALCULATE STRESS 

      DO K1=1,NTENS
        STRESS(K1)=0.0D0
        DO K2=1,NTENS
           STRESS(K1)=STRESS(K1)+DDSDDE(K2,K1)*(STRAN(K2)+DSTRAN(K2))
        ENDDO
      ENDDO
        
!     HOURGLASS CONTROL

      rFG = 0.005*(2*G12+G23)/3

!     STATE VARIABLES USED ONLY TO PLOT : moduli(t)

      STATEV(1) = E1
      STATEV(2) = E2
      STATEV(3) = G12
      STATEV(4) = G23
      STATEV(5) = PR12
      STATEV(6) = PR23

      RETURN
      END