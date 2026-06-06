% Domains
pos(1..8).

% Compositions
comp(f). comp(h). comp(l). comp(o). comp(p). comp(r). comp(s). comp(t).

% Fixed facts
at(p,3).
at(s,6).
at(o,1).

% Assignment: each composition to exactly one position
1 { at(C,P) : pos(P) } 1 :- comp(C).
1 { at(C,P) : comp(C) } 1 :- pos(P).

% T adjacency condition
adj1 :- at(t,Tp), at(f,Fp), Fp = Tp+1.
adj2 :- at(r,Rp), at(t,Tp), Tp = Rp+1.
:- not adj1, not adj2.

% Distance between F and R at least 3 (no 1 or 2 apart)
:- at(f,Fp), at(r,Rp), Fp = Rp+1.
:- at(f,Fp), at(r,Rp), Rp = Fp+1.
:- at(f,Fp), at(r,Rp), Fp = Rp+2.
:- at(f,Fp), at(r,Rp), Rp = Fp+2.

% Eighth composition is L or H
:- not at(l,8), not at(h,8).

% P before S
:- at(p,Pp), at(s,Ps), Pp >= Ps.

% O first or fifth (already at(o,1) fact, but keep constraint)
:- not at(o,1), not at(o,5).

% At least one composition between O and S
:- at(o,Po), at(s,Ps), Po = Ps+1.
:- at(o,Po), at(s,Ps), Ps = Po+1.

% Fifth must be F or T
:- not at(f,5), not at(t,5).

% Option mapping (only C should be derivable)
option(a) :- at(f,5), never_true.
option(b) :- at(f,5), never_true.
option(c) :- at(f,5).
option(c) :- at(t,5).
option(d) :- at(h,5), never_true.
option(e) :- at(o,5), never_true.

#show option/1.