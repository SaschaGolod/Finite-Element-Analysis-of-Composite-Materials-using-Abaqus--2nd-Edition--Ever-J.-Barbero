function [sse, FittedCurve] = SLSrelax(params,xdata,ydata)
    % 3-parameter exponential decay
    % Standard Linear Solid (SLS) relaxation (7.21)
    % fun is parametrized with xdata,ydata
    % so fminsearch must capture params with an annonimuous function
    % @(params) fun(params,xdata,ydata)
    
    D_0  = params(1);
    D_1  = params(2);
    tau  = params(3);    

    E_0 = D_0^-1;
    E_2 = D_1^-1;
    E_inf = (D_0+D_1)^-1;
    E_1 = E_0 - E_inf;
    
    FittedCurve = E_inf + E_1 .* exp(-xdata./tau*(E_0+E_2)/E_2);
    ErrorVector = FittedCurve - ydata;
    sse = sum(ErrorVector .^ 2);
end
