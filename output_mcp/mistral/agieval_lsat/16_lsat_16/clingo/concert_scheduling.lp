% Define the compositions
composition(f; h; l; o; p; r; s; t).

% Define positions 1 through 8
position(1..8).

% Each position has exactly one composition
1 { performed(P, C) : composition(C) } 1 :- position(P).

% Each composition is performed exactly once
1 { performed(P, C) : position(P) } 1 :- composition(C).

% Given: S is performed fourth
:- not performed(4, s).

% T is performed either immediately before F or immediately after R
% Case 1: T immediately before F
:- performed(P, t), performed(P+1, f), P+1 =< 8.
% Case 2: T immediately after R
:- performed(P, r), performed(P+1, t), P+1 =< 8.

% At least two compositions are performed either after F and before R, or after R and before F
% This means |position(F) - position(R)| >= 3
:- performed(Pf, f), performed(Pr, r), abs(Pf - Pr) < 3.

% O is performed either first or fifth
:- not performed(1, o), not performed(5, o).

% The eighth composition performed is either L or H
:- not performed(8, l), not performed(8, h).

% P is performed at some time before S
:- performed(Ps, s), performed(Pp, p), Pp >= Ps.

% At least one composition is performed either after O and before S, or after S and before O
% This means |position(O) - position(S)| >= 2
:- performed(Po, o), performed(Ps, s), abs(Po - Ps) < 2.

% Map answer choices to conditions
% Choice A: F, H, P as positions 1,2,3
answer(a) :- performed(1, f), performed(2, h), performed(3, p).

% Choice B: H, P, L as positions 1,2,3
answer(b) :- performed(1, h), performed(2, p), performed(3, l).

% Choice C: O, P, R as positions 1,2,3
answer(c) :- performed(1, o), performed(2, p), performed(3, r).

% Choice D: O, P, T as positions 1,2,3
answer(d) :- performed(1, o), performed(2, p), performed(3, t).

% Choice E: P, R, T as positions 1,2,3
answer(e) :- performed(1, p), performed(2, r), performed(3, t).

% Map the correct answer to option/1
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.