% Compositions
comp(f; h; l; o; p; r; s; t).
pos(1..8).

% Each composition exactly once
{ assigned(C, P) : pos(P) } = 1 :- comp(C).
{ assigned(C, P) : comp(C) } = 1 :- pos(P).

% Helper for position
pos_of(C, P) :- assigned(C, P).

% Conditions
% 1. T is performed either immediately before F or immediately after R.
cond1 :- pos_of(t, P1), pos_of(f, P2), P2 = P1 + 1.
cond1 :- pos_of(t, P1), pos_of(r, P2), P1 = P2 + 1.
:- not cond1.

% 2. At least two compositions are performed either after F and before R, or after R and before F.
% |pos(F) - pos(R)| - 1 >= 2  => |pos(F) - pos(R)| >= 3
cond2 :- pos_of(f, P1), pos_of(r, P2), P1 - P2 >= 3.
cond2 :- pos_of(f, P1), pos_of(r, P2), P2 - P1 >= 3.
:- not cond2.

% 3. O is performed either first or fifth.
cond3 :- pos_of(o, 1).
cond3 :- pos_of(o, 5).
:- not cond3.

% 4. The eighth composition performed is either L or H.
cond4 :- pos_of(l, 8).
cond4 :- pos_of(h, 8).
:- not cond4.

% 5. P is performed at some time before S.
cond5 :- pos_of(p, P1), pos_of(s, P2), P1 < P2.
:- not cond5.

% 6. At least one composition is performed either after O and before S, or after S and before O.
% |pos(O) - pos(S)| - 1 >= 1 => |pos(O) - pos(S)| >= 2
cond6 :- pos_of(o, P1), pos_of(s, P2), P1 - P2 >= 2.
cond6 :- pos_of(o, P1), pos_of(s, P2), P2 - P1 >= 2.
:- not cond6.

% Question constraints
:- not pos_of(p, 3).
:- not pos_of(s, 6).

% Identify the composition at position 5
comp_at_5(C) :- pos_of(C, 5).

% Option A: F or H
option_a :- comp_at_5(f).
option_a :- comp_at_5(h).
% Option B: F or O
option_b :- comp_at_5(f).
option_b :- comp_at_5(o).
% Option C: F or T
option_c :- comp_at_5(f).
option_c :- comp_at_5(t).
% Option D: H or L
option_d :- comp_at_5(h).
option_d :- comp_at_5(l).
% Option E: O or R
option_e :- comp_at_5(o).
option_e :- comp_at_5(r).

% We want the option that is true in ALL models.
#show comp_at_5/1.
#show option_a/0.
#show option_b/0.
#show option_c/0.
#show option_d/0.
#show option_e/0.