% --- Domain ---
pos(1..12).
type(a; b; c; d).
count(a, 3). count(b, 3). count(c, 4). count(d, 2).

% --- Car Type-Option Mapping ---
has_option(a, 1).
has_option(b, 3). has_option(b, 4).
has_option(c, 2).
has_option(d, 5).

% --- Hierarchical Options ---
% Option 5 implies Option 1
effective_option(T, 1) :- has_option(T, 1).
effective_option(T, 1) :- has_option(T, 5).

% --- Assignment ---
{ assign(P, T) : type(T) } = 1 :- pos(P).
:- type(T), count(T, N), not #count { P : assign(P, T) } = N.

% --- Positional Ban ---
% No car with Option 4 (EV) at 1 or 12. Type B has Option 4.
:- assign(1, b).
:- assign(12, b).

% --- Equipment Cooldown ---
% Option 2 (Type C) must have at least a 2-slot gap.
:- assign(P, c), assign(P+1, c).
:- assign(P, c), assign(P+2, c).

% --- Standard Capacity ---
% At most 2 cars with effective Option 1 in any window of 4.
has_eff_opt1(P) :- assign(P, T), effective_option(T, 1).
:- pos(P), P <= 9, #count { P1 : P <= P1, P1 <= P+3, has_eff_opt1(P1) } > 2.

% --- Conditional Capacity ---
% Option 3 (Type B).
has_opt3(P) :- assign(P, T), has_option(T, 3).
has_opt4(P) :- assign(P, T), has_option(T, 4).
preceded_by_ev(P) :- P > 1, has_opt4(P-1).

% If P is preceded by EV, at most 1 car with Option 3 in [P, P+3].
:- pos(P), P <= 9, preceded_by_ev(P), #count { P1 : P <= P1, P1 <= P+3, has_opt3(P1) } > 1.
% Otherwise, at most 2 cars with Option 3 in [P, P+3].
:- pos(P), P <= 9, not preceded_by_ev(P), #count { P1 : P <= P1, P1 <= P+3, has_opt3(P1) } > 2.

% --- Output ---
solution_found :- assign(_, _).
#show assign/2.
#show solution_found.