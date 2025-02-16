function [sse, FittedCurve] = MaxwellRelax(params,xdata,ydata)
    % 2 parameter
    % Maxwell relaxation (7.15)
    % fun is parametrized with xdata,ydata
    % so fminsearch must capture params with an annonimuous function
    % @(params) fun(params,xdata,ydata)
    
    E_0  = params(1);
    tau  = params(2);    

    FittedCurve = E_0 .* exp(-xdata./tau);
    ErrorVector = FittedCurve - ydata;
    sse = sum(ErrorVector .^ 2);
end
