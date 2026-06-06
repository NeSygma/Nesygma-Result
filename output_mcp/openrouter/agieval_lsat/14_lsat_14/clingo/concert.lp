% Define compositions and positions
composition(f). composition(h). composition(l). composition(o). composition(p). composition(r). composition(s). composition(t).
position(1..8).

% Exactly one position per composition
1 { pos(C,P) : position(P) } 1 :- composition(C).
% Exactly one composition per position
1 { pos(C,P) : composition(C) } 1 :- position(P).

% Base constraints
% T is either immediately before F or immediately after R.
:- pos(t,Pt), pos(f,Pf), pos(r,Pr), Pt+1 != Pf, Pt != Pr+1.
% At least two compositions between F and R (distance >=3)
:- pos(f,Pf), pos(r,Pr), D = Pf - Pr, D*D < 9.
% O is first or fifth
:- pos(o,Po), Po != 1, Po != 5.
% 8th composition is L or H
:- pos(C,8), C != l, C != h.
% P before S
:- pos(p,Pp), pos(s,Ps), Pp >= Ps.
% At least one composition between O and S (distance >=2)
:- pos(o,Po), pos(s,Ps), D = Po - Ps, D*D < 4.

% Fixed conditions for the question
pos(t,5).
pos(f,6).

% Map options for S position
option(a) :- pos(s,4).
option(a) :- pos(s,7).
option(b) :- pos(s,3).
option(b) :- pos(s,6).
option(c) :- pos(s,3).
option(c) :- pos(s,4).
option(d) :- pos(s,2).
option(d) :- pos(s,7).
option(e) :- pos(s,1).
option(e) :- pos(s,4).

#show option/1.