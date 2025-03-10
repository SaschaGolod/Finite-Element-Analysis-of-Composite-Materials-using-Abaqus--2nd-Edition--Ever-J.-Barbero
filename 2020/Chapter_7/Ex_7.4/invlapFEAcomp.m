% invlapWVU  numerical inverse Laplace transform
%    This is a modification of 
%    Hollenbeck, K. J. (1998) INVLAP.M: A matlab function for numerical 
%    inversion of Laplace transforms by the de Hoog algorithm,
%    http://www.mathworks.com/
%    While the original routine requires the function F to be saved a priori 
%    in a .m file with the ./, .*, and .^ operators explicity writen, 
%    invlapWVU accepts a regular function F and does the transformation
%    from / to ./ and so on automatically. For usage see
%    PMMisotropicfiberviscomatrix.m, at http://www.cemr.wvu.edu/~ejb/source
%
% f = invlapWVU(F, t, alpha, tol);
%         
% F       laplace-space function  
%           must have form F(s,t,..), where s is the Laplace parameter,
%           and return column vector as result
% t       column vector of times for which real-space function values are
%           sought
% alpha   largest pole of F (default zero)
% tol     numerical tolerance of approaching pole (default 1e-9)
% f       vector of real-space values f(t)
%
% example: identity function in Laplace space:
%           F = 1/(s^2);
%           invlap(F, [1;2;3])
%
% algorithm: de Hoog et al's quotient difference method with accelerated 
%   convergence for the continued fraction expansion
%   [de Hoog, F. R., Knight, J. H., and Stokes, A. N. (1982). An improved 
%    method for numerical inversion of Laplace transforms. S.I.A.M. J. Sci. 
%    and Stat. Comput., 3, 357-366.]
% Modification: The time vector is split in segments of equal magnitude
%   which are inverted individually. This gives a better overall accuracy.   

%  details: de Hoog et al's algorithm f4 with modifications (T->2*T and 
%    introduction of tol). Corrected error in formulation of z.
%
%  Copyright: Karl Hollenbeck
%             Department of Hydrodynamics and Water Resources
%             Technical University of Denmark, DK-2800 Lyngby
%             email: karl@isv16.isva.dtu.dk
%  22 Nov 1996, MATLAB 5 version 27 Jun 1997 updated 1 Oct 1998
%  IF YOU PUBLISH WORK BENEFITING FROM THIS M-FILE, PLEASE CITE IT AS:
%    Hollenbeck, K. J. (1998) INVLAP.M: A matlab function for numerical 
%    inversion of Laplace transforms by the de Hoog algorithm,
%    http://www.isva.dtu.dk/staff/karl/invlap.htm 

function f = invlapWVU(F, t, alpha, tol, P1,P2,P3,P4,P5,P6,P7,P8,P9);
%
%   WVU 2-18-2006
%   conversion to ./ type operators
    F = char(F); 
    F = strrep(F,'/','./');
    F = strrep(F,'*','.*');
    F = strrep(F,'^','.^');
%   end 2-18-06, but more below
%
if nargin <= 2,
  alpha = 0;
elseif isempty(alpha),
  alpha = 0;
end
if nargin <= 3,
  tol = 1e-9;
elseif isempty(tol),
  tol = 1e-9;
end
f = [];

% split up t vector in pieces of same order of magnitude, invert one piece
%   at a time. simultaneous inversion for times covering several orders of 
%   magnitudes gives inaccurate results for the small times.

allt = t;				% save full times vector
logallt = log10(allt);
iminlogallt = floor(min(logallt));
imaxlogallt = ceil(max(logallt));
for ilogt = iminlogallt:imaxlogallt,	% loop through all pieces
  
  t = allt(find((logallt>=ilogt) & (logallt<(ilogt+1))));
  if ~isempty(t),			% maybe no elements in that magnitude

    T = max(t)*2;
    gamma = alpha-log(tol)/(2*T);
    % NOTE: The correction alpha -> alpha-log(tol)/(2*T) is not in de Hoog's
    %   paper, but in Mathematica's Mathsource (NLapInv.m) implementation of 
    %   inverse transforms
    nt = length(t);
    M = 20;
    run = [0:1:2*M]';    % so there are 2M+1 terms in Fourier series expansion

    % find F argument, call F with it, get 'a' coefficients in power series
    s = gamma + i*pi*run/T;
%
%
%   WVU 2-18-06
%     command = ['a = ' F '(s'];
%     if nargin > 4,  			% pass on parameters
%       for iarg = 1:nargin-4,
% 	    command = [command ',P' int2str(iarg)];
%       end
%     end
%     command = [command ');'];
%
    command = ['a = ' F ';' ];
%   end 2-18-06

    eval(command);
    a(1) = a(1)/2;     			% zero term is halved

    % build up e and q tables. superscript is now row index, subscript column
    %   CAREFUL: paper uses null index, so all indeces are shifted by 1 here
    e = zeros(2*M+1, M+1);
    q = zeros(2*M  , M+1);  		% column 0 (here: 1) does not exist
    e(:,1) = zeros(2*M+1,1);
    q(:,2) = a(2:2*M+1,1)./a(1:2*M,1);
    for r = 2:M+1,           		% step through columns (called r...)
      e(1:2*(M-r+1)+1,r) = ...
	  q(2:2*(M-r+1)+2,r) - q(1:2*(M-r+1)+1,r) + e(2:2*(M-r+1)+2,r-1);
      if r<M+1,               		% one column fewer for q
	rq = r+1;
	q(1:2*(M-rq+1)+2,rq) = ...
	 q(2:2*(M-rq+1)+3,rq-1).*e(2:2*(M-rq+1)+3,rq-1)./e(1:2*(M-rq+1)+2,rq-1);
      end
    end

    % build up d vector (index shift: 1)
    d = zeros(2*M+1,1);
    d(1,1) = a(1,1);
    d(2:2:2*M,1) = -q(1,2:M+1).'; % these 2 lines changed after niclas
    d(3:2:2*M+1,1) = -e(1,2:M+1).'; % ...

    % build up A and B vectors (index shift: 2) 
    %   - now make into matrices, one row for each time
    A = zeros(2*M+2,nt);
    B = zeros(2*M+2,nt);
    A(2,:) = d(1,1)*ones(1,nt);
    B(1:2,:) = ones(2,nt);
    z = exp(i*pi*t'/T);		% row vector 
    % after niclas back to the paper (not: z = exp(-i*pi*t/T)) !!!
    for n = 3:2*M+2,
      A(n,:) = A(n-1,:) + d(n-1,1)*ones(1,nt).*z.*A(n-2,:);  % different index 
      B(n,:) = B(n-1,:) + d(n-1,1)*ones(1,nt).*z.*B(n-2,:);  %  shift for d!
    end

    % double acceleration
    h2M = .5 * ( ones(1,nt) + ( d(2*M,1)-d(2*M+1,1) )*ones(1,nt).*z );
    R2Mz = -h2M.*(ones(1,nt) - ...
	(ones(1,nt)+d(2*M+1,1)*ones(1,nt).*z/(h2M).^2).^.5);
    A(2*M+2,:) = A(2*M+1,:) + R2Mz .* A(2*M,:);
    B(2*M+2,:) = B(2*M+1,:) + R2Mz .* B(2*M,:);

    % inversion, vectorized for times, make result a column vector
    fpiece = ( 1/T * exp(gamma*t') .* real(A(2*M+2,:)./B(2*M+2,:)) )';
    f = [f; fpiece];			% put pieces together

  end % if not empty time piece
  
end % loop through time vector pieces
