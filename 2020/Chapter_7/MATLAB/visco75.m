% Ex 7.5 

% elastic properties
E_0 = 656 %MPa
% bulk modulus K=E*G/3/(3G-E)%http://en.wikipedia.org/wiki/Bulk_modulus
% incompressibility means E=3G, so
G_0 = E_0/3

% visco properties
tau = 37.8 %seconds, will need ~5*tau to decay
g_1 = 0.169 %MPa

% geometry
tk = 1.25   %mm
b = 10  %mm
L = 40  %mm
Area = 9*tk*b

% relaxation 
t = [0:.1:150];
G_t = G_0 * (1 - g_1*(1 - exp(-t/tau)));
E_t = 3*Gt;
% plot(t/tau,E_t/E_0,'-')
% xlabel('t/\tau'); ylabel('E(t)/E_0')

% creep test
Force = 1000    %MN
S11_0 = Force/Area 

% relaxation test
U1 = 0.4    %mm
E11_0 = U1/L
S11_0 = E_0 * E11_0
S11_t = E_t * E11_0;
% plot(t/tau,S11_t/S11_0,'-')
% xlabel('t/\tau'); ylabel('\sigma_{11}(t)/\sigma_{S11}^0')
plot(t/tau,S11_t,'-')
xlabel('t/\tau'); ylabel('\sigma_{11}(t) [MPa]')


