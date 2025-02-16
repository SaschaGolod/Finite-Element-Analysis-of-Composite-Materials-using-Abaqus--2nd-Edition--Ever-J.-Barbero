%% Example Prony
% given Maxwell relaxation parameters, 
% produce pseudo-data with Maxwell relaxation (7.15),
% then fit a Prony series to the pseudo-data 
clear all;clc;
% Data
E_0 = 4082;     %MPa
tau = 39.15;    %min
nu  = 0.311;    %constant, used in FEA, not here
TimeInitial = 0;
TimeFinal = 5*tau;
%% Pseudo-data Maxwell relaxation (7.15)
estimates(1) = E_0;
estimates(2) = tau;
xdata = [TimeInitial:(TimeFinal-TimeInitial)/10:TimeFinal]'
ydata = xdata;  %just to initialize the variable ydata
% Print
s=(['Maxwell Relaxation E_0=',num2str(E_0),', tau=',num2str(tau),', nu=',num2str(nu)]);
fprintf('%s\n',s)

% Plot
figure(2);
model = @(params) MaxwellRelax(params,xdata,ydata)
% use the handle to reproduce the plot at xdata
[sse,FittedCurve] = model(estimates);
plot(xdata,FittedCurve,'r')
title('Maxwell relaxation')
text(xdata(2),FittedCurve(1),s)
legend('(7.15)','location','best')
xlabel('time (s)'); ylabel('Relaxation moduli [MPa]');
hold off
%% Fit a Prony series to the pseudo-data
% after running all previous cells, put the relaxation values into ydata
ydata = FittedCurve;

% fit with Prony series with N terms
% 2*N+1 params are [E_i, tau_i, E_inf]
% initial estimate
N = 1;
estimates = [ydata(1), tau, ydata(length(ydata))];
% N = 2;
% estimates = [ydata(1), 10., ydata(length(ydata)), .1, .1];

% fun is parametrized with xdata,ydata
% so fminsearch must capture params with an annonimuous function
% @(params) fun(params,xdata,ydata)
model = @(params) PronyRelax(params,xdata,ydata,N);

% estimates: estimated parameters of the model
estimates = fminsearch(model, estimates);

% Print
s=(['E_1=',num2str(estimates(1)),', tau_1=',num2str(estimates(2))...
    ,', E_{inf}=',num2str(estimates(length(estimates)))]);
E_inf = estimates(2*N+1);
E_0   = E_inf;
fprintf('Prony relaxation parameters\n');
for i=1:2:2*N
    E_0 = E_0 + estimates(i);
    fprintf('i = %g, e_i   =   %g, tau_i = %g\n',i,estimates(i)/E_0,estimates(i+1))
end
    fprintf('       E_0   = %g\n',E_0)
    fprintf('       E_inf = %g\n',E_inf)
fprintf('Prony shear relaxation parameters\n');
for i=1:2:2*N
    fprintf('i = %g, g_i   =   %g, tau_i = %g\n',i,estimates(i)/E_0,estimates(i+1))
end
    fprintf('       G_0   = %g\n',E_0/3)
    fprintf('       G_inf = %g\n',E_inf/3)

% Plot
figure(3)
plot(xdata,ydata,'ok'); hold on
title('Prony relaxation derived from Table 7.2')
text(xdata(2),ydata(1),s)

% use the handle to reproduce the fit at xdata
[sse,FittedCurve] = model(estimates);
plot(xdata,FittedCurve,'r')
legend('derived data',['Prony, N=',num2str(N)],'location','best')
xlabel('time (s)'); ylabel('Relaxation moduli [MPa]');
hold off
