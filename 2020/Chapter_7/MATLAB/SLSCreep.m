function [sse, FittedCurve] = SLSCreep(params,xdata,ydata)
    % 3-parameter exponential 
    % Standard Linear Solid (SLS) creep (7.20)
    % fun is parametrized with xdata,ydata
    % so fminsearch must capture params with an annonimuous function
    % @(params) fun(params,xdata,ydata)
    
    D_0  = params(1);
    D_1  = params(2);
    tau  = params(3);    

    FittedCurve = D_0 + D_1 .* (1-exp(-xdata./tau));
    ErrorVector = FittedCurve - ydata;
    sse = sum(ErrorVector .^ 2);
end
