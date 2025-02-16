%% Example Prony
% given creep data in tabular form, fit with SLS creep (7.20), 
% produce pseudo-data with SLS relaxation (7.21),
% then fit a Prony series to the pseudo-data 
clear all;clc;
% Read data file 
%(Check for 'File Formats' if another format appears)
M=importdata('Table72.txt',',',2);
datatitle=M.textdata{1,1};
dataheadings=M.colheaders;
xdata = M.data(:,1);    %must use xdata, ydata names, global in @model, because
ydata = M.data(:,2);    %fminsearch expects model w/only 1 argument, params
ydata = ydata./1000;    %convert to MPa
clear M
%% SLS creep (7.20)
% fun is parametrized with xdata,ydata
% so fminsearch must capture params with an annonimuous function
% @(params) fun(params,xdata,ydata)
model = @(params) SLSCreep(params,xdata,ydata)

% params = [D_0, D_1, tau]
% initial estimate
estimates = [ydata(1), ydata(1)/100, 1.];

% estimates: estimated parameters of the model
estimates = fminsearch(model, estimates);

% Print
s=(['SLS Compliance Do=',num2str(estimates(1)),', D1=',num2str(estimates(2))...
    ,', tau=',num2str(estimates(3))]);
fprintf('%s\n',s)

% Plot
figure(1)
plot(xdata,ydata,'ok'); hold on
title('SLS creep Table 7.2')
text(xdata(2),ydata(1),s)

% use the handle to reproduce the plot at xdata
[sse,FittedCurve] = model(estimates);
plot(xdata,FittedCurve,'r')
legend('data','(7.20)','location','best')
xlabel('time (s)'); ylabel('Creep compliance [MPa^-1]');
hold off
%% Pseudo-data SLS relaxation (7.21) of same material
E_0 = estimates(1)^-1;
E_2 = estimates(2)^-1;
E_inf = (E_0^-1+E_2^-1)^-1;

% Print
s=(['SLS Relaxation E_0=',num2str(E_0),', E_2=',num2str(E_2),', E_{inf}=',num2str(E_inf)...
    ,', tau=',num2str(estimates(3))]);
fprintf('%s\n',s)

% Plot
figure(2);
model = @(params) SLSrelax(params,xdata,ydata)
% use the handle to reproduce the plot at xdata
[sse,FittedCurve] = model(estimates);
plot(xdata,FittedCurve,'r')
title('SLS relaxation derived from data Table 7.2')
text(xdata(2),FittedCurve(1),s)
legend('(7.21)','location','best')
xlabel('time (s)'); ylabel('Relaxation moduli [MPa]');
hold off
%% Fit a Prony series to the pseudo-data
% after running all previous cells, put the relaxation values into ydata
ydata = FittedCurve;

% fit with Prony series with N terms
% 2*N+1 params are [E_i, tau_i, E_inf]
% initial estimate
N = 1;
estimates = [ydata(1), 10., ydata(length(ydata))];
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
