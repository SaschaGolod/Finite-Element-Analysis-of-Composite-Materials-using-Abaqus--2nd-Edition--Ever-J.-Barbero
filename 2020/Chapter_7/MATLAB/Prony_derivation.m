%% Prony series
syms s t G_inf G_1 tau_1 G_0 tau_2 G_2
G = G_inf + G_1*exp(-t/tau_1)
Gs = s*laplace(G)   %Carson
Js = 1/Gs;
pretty(simplify(Js))
Jt = ilaplace(Js/s)
pretty((Jt))
Jt_0 = 1/G_inf
Jt_1 = simplify(Jt - Jt_0);
pretty(Jt_1)

Jt_11 = subs(Jt_1,G_1+G_inf,G_0);
pretty(Jt_11)
