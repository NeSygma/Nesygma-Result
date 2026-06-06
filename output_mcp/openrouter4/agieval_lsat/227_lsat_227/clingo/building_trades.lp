% === BUILDING TRADES PROBLEM ===
% Three companies trade buildings with value classes

% === DATA ===
% Buildings with their classes
% g=garza, f=flores, l=lynch, k=king, m=meyer, o=ortiz, y=yates, z=zimmer
b(g,1). b(f,1).       % class 1 buildings
b(l,2). b(k,2). b(m,2). b(o,2).  % class 2 buildings
b(y,3). b(z,3).       % class 3 buildings

% Value per class (class 1=4, class 2=2, class 3=1)
v(1,4). v(2,2). v(3,1).

% Companies: realprop(r), southco(s), trustcorp(t)
c(r;s;t).

% === OWNERSHIP (final state, after trades) ===
% Each building owned by exactly one company
{ own(B,Co) : c(Co) } = 1 :- b(B,_).

% === VALUE INVARIANT ===
% Each company's total value must be 6 (preserved through trades)
:- c(Co), #sum{W,B : b(B,Cls), v(Cls,W), own(B,Co)} != 6.

% === OPTION DEFINITIONS ===
% Each option specifies a company and the buildings it MUST own.
opt_co(a,r). opt_co(b,s). opt_co(c,s). opt_co(d,t). opt_co(e,t).

opt_bld(a,f). opt_bld(a,g).       % A: RealProp owns Flores, Garza
opt_bld(b,f). opt_bld(b,m).       % B: Southco owns Flores, Meyer
opt_bld(c,g). opt_bld(c,l).       % C: Southco owns Garza, Lynch
opt_bld(d,f). opt_bld(d,o).       % D: Trustcorp owns Flores, Ortiz
opt_bld(e,g). opt_bld(e,m).       % E: Trustcorp owns Garza, Meyer

% === CHECK WHICH OPTIONS ARE IMPOSSIBLE ===
% For each option, compute the minimum total value for the specified company
% based solely on the buildings the option requires them to own.
% If this minimum exceeds 6, the option is impossible (can't satisfy value=6 invariant).

opt_min_sum(O, S) :- 
    opt_co(O, _),
    S = #sum{W : opt_bld(O, B), b(B,Cls), v(Cls,W)}.

% An option is impossible if the minimum required value exceeds 6
opt_impossible(O) :- opt_min_sum(O, S), S > 6.

% === DERIVE THE ANSWER ===
% Only one option should be impossible. That option is the answer.
option(a) :- opt_impossible(a), not opt_impossible(b), not opt_impossible(c), not opt_impossible(d), not opt_impossible(e).
option(b) :- opt_impossible(b), not opt_impossible(a), not opt_impossible(c), not opt_impossible(d), not opt_impossible(e).
option(c) :- opt_impossible(c), not opt_impossible(a), not opt_impossible(b), not opt_impossible(d), not opt_impossible(e).
option(d) :- opt_impossible(d), not opt_impossible(a), not opt_impossible(b), not opt_impossible(c), not opt_impossible(e).
option(e) :- opt_impossible(e), not opt_impossible(a), not opt_impossible(b), not opt_impossible(c), not opt_impossible(d).

#show option/1.