function [Elas_prop, Visc_prop,model] = ...
    PMMViscoMatrix( time, V_f, imod_m, imod_f,...
                    Elas_prop_m, Elas_prop_f, Visc_prop_m)

% Viscoelastic micromechanics, isotropic and transversely isotropic fibers [Barbero & Luciano 1995].
% Uses invlapFEAcomp routine to do numerical inverse laplace transform.
%  Copyright: Ever J. Barbero
%             Department of Mechanical and Aerospace Engineering
%             West Virginia University, Morgantown, WV 26505-6106
%  23 Feb 2006, MATLAB 7 
%  IF YOU PUBLISH WORK BENEFITING FROM THIS M-FILE, PLEASE CITE IT AS:
%  R. Luciano and E. J. Barbero, "Analytical Expressions for the Relaxation Moduli 
%  of Linear Viscoelastic Composites with Periodic Microstructure," ASME J. Applied 
%  Mechanics, 62(3), 786-793, (1995)
%  http://www.cemr.wvu.edu/~ejb/source/MAE646/Chapter_6/

% To run this M-file need the functions:
%                   fitfunFEAcomp(xdata, ydata,ifun)
%                   invlapFEAcomp(time,func)

%% Elastic Properties identification
%% ---------------------------------
% Matrix
%% Elas_prop_m(1)    E_m
%% Elas_prop_m(2)    nu_m

% Isotropic fibers
%% Elas_prop_f(1)    E_f
%% Elas_prop_f(2)    nu_f

% Transversaly isotropic fibers
%% Elas_prop_f(1)   E_a 
%% Elas_prop_f(2)   E_t 
%% Elas_prop_f(3)   nu_a 
%% Elas_prop_f(4)   nu_t 
%% Elas_prop_f(5)   G_a
%% Elas_prop_f(6)   G_t

%% Viscoelastic Properties identification
%% --------------------------------------

% Maxwell Model
%% Visc_prop_m(1)   eta_m

% Standard Solid Model (SLS)
%% Visc_prop_m(1)   eta_m

% Power law 
%% Visc_prop_m(1)   eta_m

syms s complex;

disp('Perodic Microstructure, elastic fibers and viscoelastic matrix');
disp('==============================================================');
%%%Matrix: isotropic
if imod_m==1 
    % Maxwell viscoelastic solution, 
    % redefines E_m w/the Carson transform of the viscoelastic model
    E_0 = Elas_prop_m(1);
    eta_0 = Visc_prop_m(1); tau_0 = eta_0/E_0;
    E_m = s*E_0/(s+1/tau_0);
    nu_m = Elas_prop_m(2);
    disp('Matrix: Maxwell Model');
elseif imod_m==2 
    % Other model
    disp('Matrix: Other Model');
else                
    % Matrix elastic solution
    disp('Matrix: Elastic solution');
    E_m = Elas_prop_m(1);
    nu_m = Elas_prop_m(2);
end

% PMM calculation section
if imod_f==1                % isotropic fibers
    disp('Fibers: Isotropic');
    %%%Matrix: isotropic	

    lm_0=E_m*nu_m/((1+nu_m)*(1-2*nu_m));
    mu_0=E_m/(2*(1+nu_m));	
    nu_0=nu_m;		

    %%%Fiber: isotropic																					
    
    E_f  = Elas_prop_f(1);   
    nu_f = Elas_prop_f(2); 
    
    lm_1=nu_f*E_f/((1+nu_f)*(1-2*nu_f));	
    mu_1=E_f/(2*(1+nu_f));	
    nu_1=nu_f;																					

    %% a	b	c	g

    a=mu_1-mu_0-2*mu_1*nu_m+2*mu_0*nu_f;	
    b=-mu_0*nu_m+mu_1*nu_f+2*mu_0*nu_m*nu_f-2*mu_1*nu_m*nu_f;	
    c=(mu_0-mu_1)*(-mu_0+mu_1-mu_0*nu_m-2*mu_1*nu_m+2*mu_0*nu_f+mu_1*nu_f+2*mu_0*nu_m*nu_f-2*mu_1*nu_m*nu_f);	
    g=2-2*nu_m;

    %%S_3	S_6	S_7
    S_3=0.49247-0.47603*V_f-0.02748*V_f^2;	
    S_6=0.36844-0.14944*V_f-0.27152*V_f^2;	
    S_7=0.12346-0.32035*V_f+0.23517*V_f^2;	

    %%D_	C_11*	C_12*	C_23*	C_22*	C_44*	C_66*
    D_=(a*S_3^2)/(2*mu_0^2*c)-(a*S_6*S_3)/(mu_0^2*g*c)+a*(S_6^2-S_7^2)/(2*mu_0^2*g^2*c)+S_3*(b^2-a^2)/(2*mu_0*c^2)+(S_6*(a^2-b^2)+S_7*(a*b+b^2))/(2*mu_0*g*c^2)+(a^3-2*b^3-3*a*b^2)/(8*c^3);	
    C_11=lm_0+2*mu_0-V_f*((S_3^2)/(mu_0^2)-2*S_6*S_3/(mu_0^2*g)-a*S_3/(mu_0*c)+(S_6^2-S_7^2)/(mu_0^2*g^2)+(a*S_6+S_7*b)/(mu_0*g*c)+(a^2-b^2)/(4*c^2))/D_;	
    C_12=lm_0+((S_3/(2*c*mu_0))-((S_6-S_7)/(2*mu_0*c*g))-(a+b)/(4*c^2))*b*V_f/D_;	
    C_23=lm_0+V_f*((a*S_7)/(2*mu_0*g*c)-(b*a+b^2)/(4*c^2))/D_;	
    C_22=lm_0+2*mu_0-V_f*((-a*S_3)/(2*mu_0*c)+(a*S_6)/(2*mu_0*g*c)+(a^2-b^2)/(4*c^2))/D_;	
    C_44=mu_0-V_f/((-2*S_3)/mu_0+1/(mu_0-mu_1)+4*S_7/(mu_0*(2-2*nu_0)));	
    C_66=mu_0-V_f/((-S_3/mu_0)+1/(mu_0-mu_1));	

    %%% Engineering Constants
    %%E_1	E_2	n_12	n_23	G_12	G_23		
    E_1=C_11-(2*C_12^2)/(C_22+C_23);	
    E_2=((2*C_11*C_22+2*C_11*C_23-4*C_12^2)*(C_22-C_23+2*C_44))/(3*C_11*C_22+C_11*C_23+2*C_11*C_44-4*C_12^2);	
    n_12=C_12/(C_22+C_23);	
    n_23=(C_11*C_22+3*C_11*C_23-2*C_11*C_44-4*C_12^2)/(3*C_11*C_22+C_11*C_23+2*C_11*C_44-4*C_12^2);	
    G_12=C_66;	
    G_23=E_2/(2*(1+n_23));

    %%% Restrictions on elastic constants
    %%1-n12n21>0	1-n13n31>0	1-n23n32>0	1-n12n21-n23n32-n13n31-2n21n32n13>0
    % rest1=1-(n_12.*n_12.*E_2./E_1);	
    % rest2=1-(n_12.*n_12.*E_2./E_1);	
    % rest3=1-(n_23.*n_23)	;
    % rest4=1-(n_12.*n_12.*E_2./E_1)-(n_23.*n_23)-(n_12.*n_12.*E_2./E_1)-(2.*(n_12.*E_2./E_1).*(n_23).*(n_12))					
    % if ((rest1<=0) | (rest2<=0) | (rest3<=0) | (rest4<=0))
    %     disp('Error: restriction on FIBER elastic constants')
    % end
elseif imod_f==2            %%%Fiber: transversely isotropic
    disp('Fibers: Transversely Isotropic');
    %%%Matrix: isotropic 
    C16=E_m;
    D16=nu_m;

    %%%Fiber: transversely isotropic
    F15=V_f;
    B12=Elas_prop_f(1);%E_a;
    C12=Elas_prop_f(2);%E_t;
    D12=Elas_prop_f(3);%nu_a;
    E12=Elas_prop_f(4);%nu_t;
    F12=Elas_prop_f(5);%G_a;
    G12=Elas_prop_f(6);%G_t;
    % restrictions
    H12=1-(D12*D12*C12/B12);	
    I12=1-(D12*D12*C12/B12);	
    J12=1-(E12*E12);	
    K12=1-(D12*D12*C12/B12)-(E12*E12)-(D12*D12*C12/B12)-(2*(D12*C12/B12)*(E12)*(D12));
    if ((H12<=0) | (I12<=0) | (J12<=0) | (K12<=0))
        disp('Error: restriction on FIBER elastic constants')
    end
    % matrix
    E35=C16*D16/((1+D16)*(1-2*D16));
    F35=C16/(2*(1+D16));	
    G35=D16;
    % fiber
    E38=J12*B12/K12;	
    F38=(D12+E12*D12)*C12/K12;	
    G38=I12*C12/K12;
    H38=(E12+((C12*D12/B12)*D12))*C12/K12;	
    I38=F12;
    % S terms
    D42=0.49247-0.47603*F15-0.02748*F15^2;	
    E42=0.36844-0.14944*F15-0.27152*F15^2;	
    F42=0.12346-0.32035*F15+0.23517*F15^2;
    % a1 a2 a3 a4 etc
    J34=(4*F35^2)-(2*F35*G38)+(6*E35*F35)-(2*E38*F35)-(2*F35*H38)+(H38*E38)+(4*E35*F38)-(2*F38^2)-(E35*G38)-(2*E38*E35)+(E38*G38)-(E35*H38);	
    K34=(8*F35^3)-(8*F35*F35*G38)+(12*F35*F35*E35)-(4*F35*F35*E38)-(2*F35*H38*H38)+(4*F35*E35*H38)+(4*F35*E38*G38)-(8*F35*E35*G38)-(4*F35*F38*F38)+(2*F35*G38*G38)-(4*F35*E38*E35)+(8*F35*E35*F38)+(2*F35*E38*G38)+(4*F38*H38*E35)-(4*F38*G38*E35)-(2*E35*E38*H38)-(2*H38*F38*F38)+(H38*H38*E38)+(2*G38*F38*F38)-(E38*G38*G38)+(E35*G38*G38)-(E35*H38*H38);	
    L34=(((4*F35^2)+(4*F35*E35)-(2*E38*F35)-(2*F35*G38)-(E38*E35)-(E35*G38)-(F38^2)+(E38*G38)+(2*E35*F38))/(K34))-(((D42)-(E42/(2-2*G35)))/(F35));	
    M34=(-((-2*F35*H38)+(2*E35*F35)-(E35*H38)-(E38*E35)-(F38^2)+(2*E35*F38)+(E38*H38))/(K34))+((F42)/(F35*(2-2*G35)));	
    N34=((((2*F35+2*E35-G38-H38)*(-M34^2+L34^2))/(J34))+((2*(M34-L34)*(E35-F38)*(E35-F38))/(J34^2)))^(-1);	
    O34=(((2*F35)+(2*E35)-G38-H38)*L34/(J34))-(((E35-F38)*(E35-F38))/(J34^2));	
    P34=(((2*F35)+(2*E35)-G38-H38)*M34/(J34))-(((E35-F38)*(E35-F38))/(J34^2));	
    %
    H42= (E35+2*F35)-(F15*(-M34^2+L34^2)*N34);	
    I42=(E35)+(F15*(((E35-F38)*(M34-L34))/(J34))*N34);	
    J42=(E35+2*F35)-(F15*O34*N34);	
    K42=(E35)+(F15*P34*N34);	
    L42=(F35)-F15*(((2)/((2*F35)-G38+H38))-(((2*D42)-((4*F42)/(2-2*G35)))/(F35)))^(-1);	
    M42=(F35)-F15*((1/(F35-I38))-(D42/F35))^(-1);
    % C*
    H47=H42;	
    I47=I42;	
    J47=(0.75*J42+0.25*K42+0.5*M42);	
    K47=(0.25*J42+0.75*K42-0.5*M42);	
    L47=0.5*(J42-K42);	
    M47=M42;
    % Engineering properties in time or Carson depending on the matrix model
    B24=(H47)-((2*I47*I47)/(J47+K47));	
    C24=(2*H47*J47+2*H47*K47-4*I47*I47)*(J47-K47+2*L47)/(3*H47*J47+H47*K47+2*H47*L47-4*I47*I47);	
    D24=I47/(J47+K47);	
    F24=M47;	
    G24=0.25*J47-0.25*K47+0.5*L47;	
    E24=C24/(2*G24)-1;	
    H24=1-(D24*D24*C24/B24);	
    I24=1-(D24*D24*C24/B24);	
    J24=1-(E24*E24);	
    K24=1-(D24*D24*C24/B24)-(E24*E24)-(D24*D24*C24/B24)-(2*(D24*C24/B24)*(E24)*(D24));
    % Engineering constants are either elastic or Carson relaxations depending
    % on the matrix model input above
    E_1=B24;
    E_2=C24;
    n_12=D24;
    n_23=E24;
    G_12=F24;
    G_23=G24;
    if ((H12<=0) | (I12<=0) | (J12<=0) | (K12<=0))
        disp('Error: restriction on OUTPUT elastic constants')
    end
end

if imod_m==0        % elastic analisis
    Eo_1=E_1;
    Eo_2=E_2;
    nuo_12=n_12;
    nuo_23=n_23;
    Eo_12=G_12;
    Eo_23=G_23;
else                % back to the time domain
    E_1t = invlapFEAcomp(E_1/s,time);
    E_2t = invlapFEAcomp(E_2/s,time);
    n_12t = invlapFEAcomp(n_12/s,time);
    n_23t = invlapFEAcomp(n_23/s,time);
    G_12t = invlapFEAcomp(G_12/s,time);
    G_23t = invlapFEAcomp(G_23/s,time);
    % %
    % % display results in time domain
    % disp('[time,E_1t,E_2t,n_12t,n_23t,G_12t,G_23t]'); 
    % disp([time,E_1t,E_2t,n_12t,n_23t,G_12t,G_23t]);
    % %
    % % plot response without fit
    % f1 = figure;
    % plot(time,E_1t/E_1t(1)); hold on
    % plot(time,E_2t/E_2t(1),'r');
    % plot(time,G_12t/E_2t(1),'g');
    % plot(time,G_23t/E_2t(1),'m'); hold off

    % fit the moduli
    % [estimates,model] = fit_exp1(time,E_2t);
    % return estimates() for the parameters in the fit 
    % and a function handle to 'model' that contains the FittedCurve
    [estimates,model] = fitfunFEAcomp(time,E_2t,1); % #1 to activate fit exponential
    Eo_2 = estimates(1); tau_2 = 1/estimates(2);
    %disp(['Eo_2, tau_2']); disp([Eo_2, tau_2]);
    [estimates,model] = fitfunFEAcomp(time,E_1t,1); % #1 to activate fit exponential
    Eo_1 = estimates(1); tau_1 = 1/estimates(2);
    [estimates,model] = fitfunFEAcomp(time,G_12t,1); % #1 to activate fit exponential
    Eo_12 = estimates(1); tau_12 = 1/estimates(2);
    [estimates,model] = fitfunFEAcomp(time,G_23t,1); % #1 to activate fit exponential
    Eo_23 = estimates(1); tau_23 = 1/estimates(2);
    model
    %
    % % display results
    % disp('Composite relaxations as follows (Poison''s remain constant)');
    nuo_12 = n_12t(1);
    nuo_23 = n_23t(2);
    % disp('Eo_1, Eo_2, Go_12, Go_23, tau_1, tau_2, tau_12, tau_23');
    % disp([Eo_1 Eo_2 Eo_12 Eo_23 tau_1 tau_2 tau_12 tau_23]);
    % disp('nuo_12, nuo_23');
    % disp([n_12t(1) n_23t(2)]);
    % %
    % % Create exponential fit and plot E_2t in a separate figure
    % f2 = figure;
    % plot(time, E_2t, '*'); hold on;
    % [sse, FittedCurve] = model([Eo_2 1/tau_2]);
    % plot(time, FittedCurve, 'r');
end

Elas_prop   = [Eo_1 Eo_2 Eo_12 Eo_23 nuo_12 nuo_23];

if imod_m == 1
    %% Maxwell model
    Visc_prop   = [tau_1 tau_2 tau_12 tau_23];
elseif imod_m ==2
    %% Other model
     Visc_prop   = [0];
else
     Visc_prop   = [0];
     model = 1;
end

end