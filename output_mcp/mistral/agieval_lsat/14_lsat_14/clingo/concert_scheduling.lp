% Base facts: compositions and positions
composition(f; h; l; o; p; r; s; t).
position(1..8).

% Assign each position to a composition
1 { assigned(P, C) : composition(C) } 1 :- position(P).

% Each composition is assigned to exactly one position
1 { assigned(P, C) : position(P) } 1 :- composition(C).

% Constraint 1: T is performed either immediately before F or immediately after R
% T immediately before F: position(T) = position(F) - 1
% T immediately after R: position(T) = position(R) + 1
:- assigned(P, t), assigned(P+1, f).
:- assigned(P, t), assigned(P-1, r).

% Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
% This means: |position(F) - position(R)| >= 3
:- assigned(Pf, f), assigned(Pr, r), abs(Pf - Pr) < 3.

% Constraint 3: O is performed either first or fifth
:- assigned(1, C), C != o.
:- assigned(5, C), C != o.

% Constraint 4: The eighth composition is either L or H
:- assigned(8, C), C != l, C != h.

% Constraint 5: P is performed at some time before S
:- assigned(Pp, p), assigned(Ps, s), Pp >= Ps.

% Constraint 6: At least one composition is performed either after O and before S, or after S and before O
% Helper: There is at least one position between P1 and P2
position(P) :- position(1..8).
has_between(P1, P2) :- position(P1), position(P2), P1 < P2, P2 - P1 > 1, position(P), P1 < P, P < P2.

% If O is before S, there must be at least one position between them
:- assigned(Po, o), assigned(Ps, s), Po < Ps, not has_between(Po, Ps).

% If S is before O, there must be at least one position between them
:- assigned(Po, o), assigned(Ps, s), Ps < Po, not has_between(Ps, Po).

% Question-specific condition: T is performed fifth and F is performed sixth
:- not assigned(5, t).
:- not assigned(6, f).

% Determine possible positions for S
possible_s_position(P) :- position(P), assigned(P, s).

% Map possible positions of S to answer choices
% (A) fourth or seventh
option(a) :- possible_s_position(4).
option(a) :- possible_s_position(7).

% (B) third or sixth
option(b) :- possible_s_position(3).
option(b) :- possible_s_position(6).

% (C) third or fourth
option(c) :- possible_s_position(3).
option(c) :- possible_s_position(4).

% (D) second or seventh
option(d) :- possible_s_position(2).
option(d) :- possible_s_position(7).

% (E) first or fourth
option(e) :- possible_s_position(1).
option(e) :- possible_s_position(4).

#show option/1.