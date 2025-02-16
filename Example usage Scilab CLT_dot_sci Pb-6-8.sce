// Pb 6-8 in Into Comp mater Design 3rd Ed, ISBN 978-1-138-19680-3
mode(0); // prints each line like MATLAB unless suppressed by ;
funcprot(0); // suppress warning when redefining a function
exec('CLT.sci',0);// functions in CLT.sci
N = 2; // number of laminas
thickness = [2,2]; // mm
orientation = [0,0]; // deg
Q_ = zeros(3,3,N);
// Aluminum
E1 = 71E3;
E2 = 71E3;
v12 = 0.3;
G12 = E2/2/(1+v12);
Q(:,:,1) = buildQ(E1,E2,G12,v12);// use CLT.sci
// Copper
E1 = 119E3;
E2 = 119E3;
v12 = 0.3;
v23 = v12;
G12 = E2/2/(1+v12);
Q(:,:,2) = buildQ(E1,E2,G12,v12);// use CLT.sci
// calculate
[A,B,D] = ABD(Q,thickness,orientation)// use CLT.sci
// generate LaTeX output 
prettyprint(A)
prettyprint(B)
prettyprint(D)
