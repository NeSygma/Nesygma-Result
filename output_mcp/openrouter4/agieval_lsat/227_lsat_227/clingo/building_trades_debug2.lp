% === DATA ===
b(g,1). b(f,1).       % class 1 buildings
b(l,2). b(k,2). b(m,2). b(o,2).  % class 2 buildings
b(y,3). b(z,3).       % class 3 buildings

v(1,4). v(2,2). v(3,1).

% Option definitions
opt_bld(a,f). opt_bld(a,g).

% Test sum
opt_min_sum(O, S) :- 
    O = a,
    S = #sum{W, B : opt_bld(O, B), b(B,Cls), v(Cls,W)}.

#show opt_min_sum/2.