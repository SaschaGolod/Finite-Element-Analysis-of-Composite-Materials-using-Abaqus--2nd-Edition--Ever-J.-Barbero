// CLT.sci Scilab functions for Classical Lamination Theory
// (c) 2017, 2018 Ever J. Barbero, all rights reserved. 
// To be used with Examples in 
// "Introduction to Composite Materials Design--Third Edition"
// ISBN: 978-1-138-19680-3 
// Usage: insert the following in your .sce file
//        exec('C:\folder_location\CLT.sci');
//
Reuter = [[1,0,0];[0,1,0];[0,0,2]];// Reuter matrix

function [T,a] = transf(theta)// theta [degrees]
    // build in-plane [T] and intralaminar [a] transformation matrices
    m = cosd(theta);
    n = sind(theta);
    R = [[1 0 0];[0 1 0];[0 0 2]];
    T = [[m^2 n^2 2*m*n];..
         [n^2 m^2 -2*m*n];..
         [-m*n m*n m^2-n^2]] // (5.40) in-plane transformation matrix
    [a] = [[m n];[-n m]]; //(5.27) intralaminar transformation matrix
endfunction

function Macaulay = Macaulay(x)
    // returns positive argument, else zero
    Macaulay = (x+abs(x))/2;
endfunction

function Q = buildQ(E1,E2,G12,v12)
    // build reduced stiffness matrix in lamina cs
    v21 = v12*E2/E1;
    D = 1-v12*v21;
    // (5.24)
    Q = zeros(3,3);
    Q(1,1) = E1/D;
    Q(2,2) = E2/D;
    Q(1,2) = v12*E2/D;
    Q(2,1) = Q(1,2);
    Q(3,3) = G12;
endfunction

function Qast = buildQast(G13,G23)
    // build [Q*] (5.24)
    Qast = zeros(2,2);
    Qast(1,1) = G23;
    Qast(2,2) = G13;
endfunction

function Q_ = rotateQ(Q,theta)
    // rotate from lamina to laminate
    T = transf(theta)//theta in degrees
    Q_ = inv(T) * Q * inv(T)' // (5.54)
endfunction

function Qast_ = rotateQast(Qast,theta)
    // rotate from lamina to laminate
    [dummy,a] = transf(theta)//only need [a]
    Qast_ = a * Qast * a' //(5.54)
endfunction

function sigma = rotateSigma_(sigma_,theta)
    // rotate from laminate to lamina cs
    T = transf(theta)//theta in degrees
    sigma = T * sigma_ //(5.44)
endfunction

function eps = rotateEps_(eps_,theta)
    // rotate from laminate to lamina cs
    R = Reuter;//defined in this file: CLT.sci
    T = transf(theta)//theta in degrees
    eps = R*T*R^-1*eps_; //(5.42)
endfunction

function [A,B,D] = buildABD(Q,thickness,orientation)
    // build A,B,D matrices
    // same material for all laminas
    // see ABD() for laminas of different materials
    A = zeros(3,3); B = A; D = A; // initialize 
    N = length(thickness)
    if length(orientation) ~= N then
        disp('wrong number of orientations')
        break
    end
    LaminateThickness = sum(thickness)
    z_km1 = - LaminateThickness/2 // bottom of laminate
    for k = 1:1:N
        z_k = z_km1 + thickness(k) // top of lamina k
        Q_ = rotateQ(Q,orientation(k))//only difference w.r.t. ABD() function
        A = A + Q_*thickness(k)
        B = B - Q_*(z_k^2-z_km1^2)/2 // new M-k sign convention
        D = D + Q_*(z_k^3-z_km1^3)/3
        z_km1 = z_k // next lamina bottom coordinate
    end
endfunction

function [A,B,D] = ABD(Q,thickness,orientation)
    // build A,B,D matrices
    // different material for each lamina
    // see buildABD() for simpler version with single material system
    A = zeros(3,3); B = A; D = A; // initialize 
    N = length(thickness)
    if length(orientation) ~= N then
        disp('wrong number of orientations')
        break
    end
    LaminateThickness = sum(thickness)
    z_km1 = - LaminateThickness/2 // bottom of laminate
    for k = 1:1:N
        z_k = z_km1 + thickness(k) // top of lamina k
        Q_ = rotateQ(Q(:,:,k),orientation(k))//only difference w.r.t. buildABD()
        A = A + Q_*thickness(k)
        B = B - Q_*(z_k^2-z_km1^2)/2 // new M-k sign convention
        D = D + Q_*(z_k^3-z_km1^3)/3
        z_km1 = z_k // next lamina bottom coordinate
    end
endfunction

function H = buildH(Qast,thickness,orientation)
    // build H matrix, all laminas same material
    H = zeros(2,2)
    N = length(thickness)
    if length(orientation) ~= N then
        disp('wrong number of orientations')
        break
    end
    LaminateThickness = sum(thickness)
    z_km1 = - LaminateThickness/2 // bottom of laminate
    for k = 1:1:N
        t_k = thickness(k)
        z_k = z_km1 + t_k // top of lamina k
        zbar_k = z_km1 + t_k/2 // center of lamina k
        Qast_ = rotateQast(Qast,orientation(k))
        // H = H - Qast_*thickness(k) // classical theory, not good enough
        H = H-5/4*Qast_*(t_k-4/(LaminateThickness^2)*(t_k*zbar_k^2+(t_k^3)/12))
        z_km1 = z_k // next lamina bottom coordinate
    end
endfunction

function [R,imode] = maxStress(FT,FC,sigma)
    // calculates max. stress R and mode of failure
    // imode =1: fiber, 2: matrix transverse, 3: matrix shear
    // input strength values like this:  FT = [F1t,F2t,F6]; FC = [F1c,F2c,F6]
    I1 = Macaulay(sigma(1)/FT(1)) + Macaulay(-sigma(1)/FC(1)) + 1.0E-12
    I2 = Macaulay(sigma(2)/FT(2)) + Macaulay(-sigma(2)/FC(2)) + 1.0E-12
    I3 = Macaulay(sigma(3)/FT(3)) + Macaulay(-sigma(3)/FC(3)) + 1.0E-12//inplane shear sigma_6
    [I,imode] = max(I1,I2,I3) //max I and mode
    R = 1/I //strength ratio (triggers and error if I==0)
    imode = sign(sigma(imode))*imode //mode with sign (tension, compression)
endfunction

function [R,imode] = interactingFC(FT,FC,sigma)
    // calculates Interacting R and mode of failure
    // imode =1: fiber. imode =2: matrix
    // input strength values like this:  FT = [F1t,F2t,F6]; FC = [F1c,F2c,F6]
    // Interacting coefficients
    F2t = FT(2); F2c = FC(2); F6 = FT(3);
    f2  = F2t^-1 - F2c^-1
    f22 = (F2t*F2c)^-1
    f66 = F6^-2
    // calculations
    I1 = Macaulay(sigma(1)/FT(1)) + Macaulay(-sigma(1)/FC(1)) + 1.0E-12
    R1 = 1/I1 //strength ratio (triggers and error if I==0)
    a = f22*sigma(2)^2 + f66*sigma(3)^2;
    b = f2*sigma(2);
    R2 = -b+sqrt(b^2+4*a)/(2*a);
    [R,imode] = min(R1,R2) //max I and mode
    imode = sign(sigma(imode))*imode //mode with sign (tension, compression)
endfunction

function [LPF,R1,R2,R6] = TMS(eps0,e1t,e1c,e2t,v12,orientation,thickness)
    // Truncated Max. Strain (TMS)
    // to avoid matrix cutoff, set et2 = %inf
    // TMS is a laminate f.c. It cannot be called individually per lamina
    // eps0 == [A]^-1 * {N}, symmetric laminate
    LT = sum(thickness);// laminate thickness
    NL = length(orientation); // number of laminas
    if length(thickness)~=length(orientation) then, abort, end
    R1 = %inf;
    R2 = %inf;
    R6 = %inf;
    for k = 1:NL/2//symmetric part only
        eps = rotateEps_(eps0,orientation(k)); //to lamina c.s.
        if eps(1)~=0 then //prevent division by zero
            r1 = Macaulay(e1t/eps(1)) + Macaulay(-e1c/eps(1));//(7.56)
            R1 = min(R1,r1);// tracks min(R1) for all laminas
        else 
            r1 = %inf;
        end
        if abs(eps(1)-eps(2))~=0 then //prevent division by zero
            r6 = (1 + v12) * max(e1t,e1c) / abs( eps(1) - eps(2) );//(7.56)
            R6 = min(R6,r6);// tracks min(R6) for all laminas
        else 
            r6 = %inf;
        end
        if eps(2)>0 then // matrix cutoff
            r2 = Macaulay(e2t/eps(2)); //(7.57)
            R2 = min(R2,r2);// tracks min(R2) for all laminas
        else 
            r2 = %inf;
        end
        LPF = min(R1,R2,R6);//tracks overall minimum for all laminas
        table(k,:)=([ k, orientation(k), round(1E6*eps'), round([r1, r2, r6]*100)/100 ])
    end
endfunction

function [E1,E2,G12,v12,alpha1,alpha2] = ROM(Ef,vf,alphaf,Em,vm,alpham,Vf)
    // Simple Micromechanics for Isotropic fiber and matrix
    // Better use PMM for increased accuracy
    Vm = 1-Vf // Vf: fiber volume fraction. Vm: matrix v.f.
    Gf = Ef/2/(1+vf)//isotropic fiber//corrected sign (4.14)
    Gm = Em/2/(1+vm)//isotropic matrix//corrected sign (4.14) 
    GA = Gf// Shear modulus isotropic fiber
    vA = vf // Poisson's ratio isotropic fiber 
    // ROM (rule of mixtures)
    E1 = Ef*Vf + Em*Vm//accurate, best
    v12 = vf*Vf + vm*Vm//accurate, best
    // E2 = 1/(Vf/Ef + Vm/Em)//not accurate, not used
    // G12 = 1/(Vf/Gf + Vm/Gm)//not accurate, not used
    // CAM/CCA (cylindrical assemblage micromechanics) (4.35)
    G12 = Gm * ( (1+Vf) + (1-Vf)*Gm/Gf )/( (1-Vf) + (1+Vf)*Gm/Gf ) //good
    // PMM (periodic microstructure micromechanics) best
    // S3 = 0.49247 - 0.47603*Vf - 0.02748*Vf^2
    // G12 = Gm * ( 1 + (Vf*(1-Gm/GA)) / (Gm/GA + S3*(1-Gm/GA)) )//best
    // Halpin-Tsai (4.25)
    zeta = 2
    eta = (Ef/Em - 1)/(Ef/Em + 2)
    E2 = Em * (1+zeta*eta*Vf) / (1-eta*Vf)//Halpin-Tsai, best (4.25)
    // Strife-Prewo formula. Better use PMM for accuracy.
    alpha1 = (alphaf*Vf*Ef + alpham*Vm*Em)/E1
    alphaT = alphaf // isotropic fiber
    alpha2 = (1 + vm)*alpham*(1-Vf) + (1+vA)*alphaT*Vf - alpha1*v12 
endfunction

function [E1,E2,G12,v12,v23] = PMM(EA,ET,GA,vA,vT,EM,vM,Vf)
// Periodic Microstructure Micromechanics transversely isotropic fiber. 
// (c) Ever J. Barbero (1994-2017)
// Equations taken from (please cite in your work): 
// Barbero, E.J. and Luciano, R., "Micromechanical formulas for the
// relaxation tensor of linear viscoelastic composites with transversely
// isotropic fibers", International Journal of Solids and Structures,
// 32(13):1859--1872, 1995. http://barbero.cadec-online.com/papers/1995/ 
// 95BarberoLucianoMicromechanicalFormulas.pdf
    //
    // fiber coefficients
    f =ET/EA
    Delta = (1-2*vA^2*f-vT^2-2*vA^2*vT*f)/(EA*ET^2)
    C_11 = (1-vT^2)/(ET^2*Delta)
    C_22 = (1-vA^2*f)/(EA*ET*Delta)
    C_33 = C_22
    C_12 = (vA*f+vA*vT*f)/(ET^2*Delta)
    C_13 = C_12
    C_23 = (vT + vA^2*f)/(EA*ET*Delta)
    C_44 = ET/(2*(1+vT))
    C_55 = GA
    C_66 = C_55
    // matrix coefficients
    lam_m = (EM*vM)/((1+vM)*(1-2*vM))
    mu_m = EM/2/(1+vM)//isotropic matrix
    // geometry
    S3 = 0.49247 - 0.47603*Vf - 0.02748*Vf^2
    S6 = 0.36844 - 0.14944*Vf - 0.27152*Vf^2
    S7 = 0.12346 - 0.32035*Vf + 0.23517*Vf^2
    // a_values
    a1 = 4*mu_m^2 - 2*mu_m*C_33 + 6*lam_m*mu_m - 2*C_11*mu_m - ...
    2*mu_m*C_23 + C_23*C_11 + 4*lam_m*C_12 - 2*C_12^2 - lam_m*C_33 ...
    -2*C_11*lam_m + C_11*C_33 - lam_m*C_23
    a2 = 8*mu_m^3- 8*mu_m^2*C_33 + 12*mu_m^2*lam_m -4*mu_m^2*C_11 ...
    - 2*mu_m*C_23^2 + 4*mu_m*lam_m*C_23 + 4*mu_m*C_11*C_33 - ...
    8*mu_m*lam_m*C_33 - 4*mu_m*C_12^2 + 2*mu_m*C_33^2 - ...
    4*mu_m*C_11*lam_m + 8*mu_m*lam_m*C_12 + 2*lam_m*C_11*C_33 + ...
    4*C_12*C_23*lam_m - 4*C_12*C_33*lam_m - 2*lam_m*C_11*C_23 - ...
    2*C_23*C_12^2 + C_23^2*C_11 + 2*C_33*C_12^2 - C_11*C_33^2 + ...
    lam_m*C_33^2 - lam_m*C_23^2 
    a3 = ((4*mu_m^2 + 4*lam_m*mu_m - 2*C_11*mu_m - 2*mu_m*C_33 - ...
    C_11*lam_m - lam_m*C_33 - C_12^2)/a2)  + ...
    ((C_11*C_33 + 2*lam_m*C_12)/a2) - ((S3-((S6)/(2-2*vM)))/mu_m) 
    a4 = -1*((-2*mu_m*C_23 + 2*lam_m*mu_m - lam_m*C_23 - ...
    C_11*lam_m - C_12^2 + 2*lam_m*C_12 + C_11*C_23)/a2) + ...
    (S7)/(mu_m*(2-2*vM))
    // C_values
    C11t = lam_m + 2*mu_m - Vf*(-a4^2 + a3^2)*inv(-1*(((2*mu_m + ...
    2*lam_m - C_33 - C_23)*(a4^2-a3^2))/a1) + ...
    ((2*(a4-a3)*(lam_m-C_12)^2)/a1^2)) 
    C12t = lam_m + Vf*(((lam_m-C_12)*(a4-a3))/a1)*inv(1*(((2*mu_m + ...
    2*lam_m - C_33 - C_23)*(a3^2-a4^2))/a1) + ...
    ((2*(a4-a3)*(lam_m-C_12)^2)/a1^2))
    C22t = lam_m + 2*mu_m - Vf*(((2*mu_m + 2*lam_m - C_33 - ...
    C_23)*a3/a1) -((lam_m-C_12)^2/a1^2))*inv(1*(((2*mu_m + 2*lam_m ...
    - C_33 - C_23)*(a3^2-a4^2))/a1) + ((2*(a4-a3)*(lam_m-C_12)^2)/a1^2))
    C23t = lam_m + Vf*(((2*mu_m + 2*lam_m - C_33 - C_23)*a4/a1) - ...
    ((lam_m-C_12)^2/a1^2))*inv(1*(((2*mu_m + 2*lam_m - C_33 - ...
    C_23)*(a3^2-a4^2))/a1) + ((2*(a4-a3)*(lam_m-C_12)^2)/a1^2))
    C44t = mu_m - Vf*inv((2/(2*mu_m - C_22 + C_23)) - ...
    inv(mu_m)*(2*S3 - (4*S7/(2-2*vM))))
    C66t = mu_m -Vf*inv(inv(mu_m-C_66) - S3/mu_m)
    // C_total
    C11 = C11t
    C12 = C12t
    C13 = C12t
    C22 = (3/4)*C22t + (1/4)*C23t +(1/4)*C44t //corrected
    C33 = C22
    C23 = (1/4)*C22t + (3/4)*C23t -(1/4)*C44t //corrected
    C55 = C66t
    C66 = C66t
    C44 = (C22-C23)/2 // TI enforced, do not use C44t here
    // stiffness
    C = [C11 C12 C13 0 0 0; C12 C22 C23 0 0 0; C13 C23 C33 0 0 0; ...
    0 0 0 C44 0 0; 0 0 0 0 C55 0; 0 0 0 0 0 C66]
    // compliance
    S = inv(C);
    // Elastic properties
    E1 = 1/S(1,1) 
    E2 = 1/S(2,2)
    v12 = -S(2,1)/S(1,1)
    v23 = -S(3,2)/S(2,2) 
    G12 = 1/S(6,6)
    G23 = 1/S(4,4)  //redundant 
endfunction

function [a1,a2] = Levin(EA,ET,GA,vA,vT,EM,vM,aA,aT,aM,Vf,E1,E2,v12,v23)
    // (c) Ever J. Barbero (2017) ISBN 978-1-138-19680-3 Sect. 4.4
    // computes lamina tangent CTE's (a1,a2) using Levin CTE equations
    // EA, ET, GA, vA, vT, aA, aT: T.I. elastic properties and CTEs of fiber
    // EM, vM, aM: isotropic matrix values at temp. T 
    // E1, E2, v12, v23, must be previously calculated using PMM formulas

    // effective compliance 3x3 tensor
    S11_ = 1/E1 // E1, E2, v12, v23, previously calculated by PMM
    S22_ = 1/E2 
    S12_ = -v12/E1 
    S23_ = -v23/E2 

    // volume average
    Vm = 1-Vf// matrix volume fraction
    a1h = aA*Vf + aM*Vm// axial. alpha tensors are diagonal
    a2h = aT*Vf + aM*Vm// transverse. alpha tensors are diagonal

    S11h = Vf/EA + Vm/EM
    S22h = Vf/ET + Vm/EM
    S12h = - vA/EA*Vf - vM/EM*Vm
    S23h = - vT/ET*Vf - vM/EM*Vm

    // A = Sf - Sm
    A11 = 1/EA - 1/EM
    A22 = 1/ET - 1/EM
    A12 = -vA/EA + vM/EM
    A23 = -vT/ET + vM/EM

    detA = A11*(A22^2-A23^2)+2*A12*(A12*A23-A22*A12)

    P11 = (A22^2-A23^2)/detA
    P22 = (A11*A22-A12^2)/detA
    P12 = (A12*A23-A22*A12)/detA
    P23 = (A12^2-A11*A23)/detA

    // effective tangent CTEs
    a1 = a1h + (S11_-S11h)*( (aA-aM)*P11 + (aT-aM)*2*P12 ) +..
         2*(S12_-S12h)*( (aA-aM)*P12 + (aT-aM)*(P22+P23) )
    a2 = a2h + (S12_-S12h)*( (aA-aM)*P11 + (aT-aM)*2*P12 ) +..
         (S22_-S22h + S23_-S23h)*( (aA-aM)*P12 + (aT-aM)*(P22+P23) ) 
endfunction

function [Ex,Ey,Gxy,PRxy] = LaminateModuli(A,h)
    // A: A matrix
    // h: laminate thickness
    Ex = (A(1,1)*A(2,2)-A(1,2)^2)/(h*A(2,2))
    Ey = (A(1,1)*A(2,2)-A(1,2)^2)/(h*A(1,1))
    PRxy = A(1,2)/A(2,2)
    Gxy = A(3,3)/h; 
endfunction

function [hr,A,B,D,h,NL] = HR(Q,thick_,theta_,r)
    exec('C:\Users\EJB\OneDrive\Scilab\CLT.sci');
    // calculate homogenization ratio hr (6.54)
    // Q: lamina stiffness matrix 3x3
    // thick_: sublaminate thicknesses (r=1)
    // theta_: sublaminate orientations (r=1)
    function BIIhat = BIIhat(B,h)
        // calculate BIIhat. h:laminate thickness. B: B matrix
        Bhat = B/h^2;                                   // (6.55)
        trBhat = Bhat(1,1)+Bhat(2,2)+2*Bhat(3,3);       // trace Bhat
        Bhat2 = Bhat*Bhat;              // (Bhat)^2
        trBhat2 = Bhat2(1,1)+Bhat2(2,2)+2*Bhat2(3,3);   // trace Bhat2
        BIIhat = (trBhat^2-trBhat2)/2;                  //(6.56)
    endfunction
    // do r=1 to get BIIhat_r_1
    thick = thick_; theta = theta_; h = sum(thick); NL = length(thick_);
    if NL~=length(theta_) then disp('* ERROR *'); abort; end
    [A,B,D] = buildABD(Q,thick,theta);
    // calculate BIIhat_r_1
    BIIhat_r_1 = BIIhat(B,h);
    // r > 1
    if r > 1 then
        for i=2:r // build the arrays for r > 1 concatenating r sublaminates
            thick = cat(2,thick,thick_); theta = cat(2,theta,theta_);
        end
        h = sum(thick); NL = sum(thick);
        [A,B,D] = buildABD(Q,thick,theta);
        hr = 1 - sqrt(BIIhat(B,h)/BIIhat_r_1)
    else
        hr = 0;
    end
endfunction

function [NT,MT] = thermalForces(Q,alpha,thickness,orientation,deltaT)
    // calculate thermal forces
    // Q(:,:,k) lamian c.s. stiffness Q for lamina k
    // alpha(:,k) lamina c.s. CTE for lamina k 
    NL = length(thickness)
    if length(orientation) ~= NL then
        disp('wrong number of orientations')
        break
    end
    NT = zeros(3,1); MT = zeros(3,1); // initialize column arrays
    LaminateThickness = sum(thickness)
    z_km1 = - LaminateThickness/2 // bottom of laminate
    for k = 1:1:NL
        z_k = z_km1 + thickness(k) // top of lamina k
        Q_ = rotateQ(Q(:,:,k),orientation(k))//laminate c.s.
        alpha_ = rotateEps_(alpha(:,k),-orientation(k))//lamina to laminate c.s.
        NT = NT + deltaT * Q_ * alpha_ * thickness(k)//(6.74) original
        MT = MT - deltaT * Q_ * alpha_ * (z_k^2-z_km1^2)/2//(6.74) original
        z_km1 = z_k // bottom next lamina 
    end
endfunction
