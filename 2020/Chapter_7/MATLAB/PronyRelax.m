function [sse, FittedCurve] = PronyRelax(params,xdata,ydata,N)
    % Prony series (relaxation only) 
    % fun is parametrized with xdata,ydata
    % so fminsearch must capture params with an annonimuous function
    % @(params) fun(params,xdata,ydata)
    
    for j=1:2:2*N
        E(j)   = params(j);
        tau(j) = params(j+1);
    end
    E_inf = params(2*N+1);

    FittedCurve = E_inf.*ones(length(xdata),1);
    for j=1:2:2*N
        FittedCurve = FittedCurve + E(j).*exp(-xdata./tau(j));
    end
    ErrorVector = FittedCurve - ydata;
    sse = sum(ErrorVector .^ 2);
end
