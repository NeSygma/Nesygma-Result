% === DATA ===
b(g,1). b(f,1).       % class 1 buildings
b(l,2). b(k,2). b(m,2). b(o,2).  % class 2 buildings
b(y,3). b(z,3).       % class 3 buildings

v(1,4). v(2,2). v(3,1).

c(r;s;t).             % realprop, southco, trustcorp

% Ownership
{ own(B,Co) : c(Co) } = 1 :- b(B,_).

% Value invariant
:- c(Co), #sum{W,B : b(B,Cls), v(Cls,W), own(B,Co)} != 6.

% Option definitions
opt_co(a,r). opt_co(b,s). opt_co(c,s). opt_co(d,t). opt_co(e,t).

opt_bld(a,f). opt_bld(a,g).
opt_bld(b,f). opt_bld(b,m).
opt_bld(c,g). opt_bld(c,l).
opt_bld(d,f). opt_bld(d,o).
opt_bld(e,g). opt_bld(e,m).

% Compute min sum for each option
opt_min_sum(O, S) :- 
    opt_co(O, _),
    S = #sum{W : opt_bld(O, B), b(B,Cls), v(Cls,W)}.

% Debug: show min sums
% Check which are impossible
opt_impossible(O) :- opt_min_sum(O, S), S > 6.

% Derive answer
option(a) :- opt_impossible(a), not opt_impossible(b), not opt_impossible(c), not opt_impossible(d), not opt_impossible(e).
option(b) :- opt_impossible(b), not opt_impossible(a), not opt_impossible(c), not opt_impossible(d), not opt_impossible(e).
option(c) :- opt_impossible(c), not opt_impossible(a), not opt_impossible(b), not opt_impossible(d), not opt_impossible(e).
option(d) :- opt_impossible(d), not opt_impossible(a), not opt_impossible(b), not opt_impossible(c), not opt_impossible(e).
option(e) :- opt_impossible(e), not opt_impossible(a), not opt_impossible(b), not opt_impossible(c), not opt_impossible(d).

#show option/1.
#show opt_impossible/1.
#show opt_min_sum/2.