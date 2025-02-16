function [estimates, model] = fitfunFEAcomp(xdata, ydata,ifun)

if ifun==0
    start_point = rand(1, 2);
    model = @polyfun;
    estimates = fminsearch(model, start_point);
elseif ifun==1
    % Call fminsearch with a random starting point.
    start_point = [1 0] ; %rand(1, 2);
    model = @expfun;
    estimates = fminsearch(model, start_point);    
elseif ifun==12
    start_point =[1 1 0];% rand(1, 3);
    model = @fitpower;
    estimates = fminsearch(model, start_point);
elseif ifun==13
    start_point =[1 1 1 0];% rand(1, 4);
    model = @fitkevin;
    estimates = fminsearch(model, start_point);
end

% Call fminsearch with a random starting point.
% expfun accepts curve parameters as inputs, and outputs sse,
% the sum of squares error for A * exp(-lambda * xdata) - ydata, 
% and the FittedCurve. FMINSEARCH only needs sse, but we want to 
% plot the FittedCurve at the end.
    function [sse, FittedCurve] = polyfun(params)
        p1 = params(1);
        p2 = params(2);
        FittedCurve = p2 + p1 .* xdata;
        ErrorVector = FittedCurve - ydata;
        sse = sum(ErrorVector .^ 2);
    end
% expfun accepts curve parameters as inputs, and outputs sse,
% the sum of squares error for A * exp(-lambda * xdata) - ydata, 
% and the FittedCurve. FMINSEARCH only needs sse, but we want to 
% plot the FittedCurve at the end.
    function [sse, FittedCurve] = expfun(params)
        A = params(1);
        lambda = params(2);
        FittedCurve = A .* exp(-lambda * xdata);
        ErrorVector = FittedCurve - ydata;
        sse = sum(ErrorVector .^ 2);
    end

% fitXXX accepts curve parameters as inputs, and outputs sse,
% the sum of squares error for the function, and the FittedCurve. 
% FMINSEARCH only needs sse, but we want to 
% plot the FittedCurve at the end.
    function [sse, FittedCurve] = fitpower(params)
        D_0  = params(1);
        D_1  = params(2);
        m    = params(3);
        FittedCurve = D_0 + D_1.*(xdata).^m;
        ErrorVector = FittedCurve - ydata;
        sse = sum(ErrorVector .^ 2);
    end
    function [sse, FittedCurve] = fitkevin(params)
        D_0  = params(1);
        D_1p = params(2);
        tau  = params(3);
        m    = params(4);
        FittedCurve = D_0 + D_1p .* (1-exp(-xdata./tau).^m);
        ErrorVector = FittedCurve - ydata;
        sse = sum(ErrorVector .^ 2);
    end
end
