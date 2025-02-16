% minimizeGnc.m: find Gnc with a0 Kn tno rangeCOD constant 
%! Remember to close Abaqus CAE, it locks the .odb!!!!!!!!!!!!!!!!!!!!
%! Remember to select the correct SOFTENING MODEL inside *.py!!!!!!!!!
%! Remember to select the correct experimental data inside *.py!!!!!!!
%! Remember to select the correct *.py inside "cost1D.m"!!!!!!!!!!!!!!
%! Remember to set the initialState.txt!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
%! If "cost" does not change, check Abaqus breaking with an error!!!!!
% To adjust a0 use rangeCOD of the initial linear region of data 
% To adjust Gnc use rangeCOD of all experimental data 
clc; dos('copy .\initialState.txt .\state.txt');% read by *.py script
[~, ~] = dos('clean.bat');% remove *.lck and other unnecessary files
is = fopen('initialState.txt','r');
A = fscanf(is, '%g %g %g %g %g' );
a0 = A(1);% adjust 1st if simulation doesn't match linear data
Kn = A(2);% use ~Ea/ta, do not adjust too much
tno = A(3);% use adhesive bulk strength, do not adjust too much
Gnc = A(4);% fracture energy, main property to adjust
rangeCOD = A(5); %COD = 2*simulationRange 
disp([num2str([a0, Kn, tno, Gnc, rangeCOD])])
fclose(is);
% 'Display','iter' to see what's going on!
% 'Tolfun' = 1.0*%cost, 'TolX' = 0.01*Gnc
options = optimset('Display','iter','TolFun',1.0,'TolX',0.01,'MaxIter',100);
fun = @(x)cost1D(a0, Kn, tno, x, rangeCOD);% a0 Kn tno rangeCOD constant
x = fminsearch(fun, Gnc, options);% x is Gnc
disp('optimum = '+string(x))
