% Define the compositions and positions
composition(f; h; l; o; p; r; s; t).
position(1..8).

% Assign each composition to a unique position
1 { assigned(C, P) : position(P) } 1 :- composition(C).
:- composition(C1), composition(C2), C1 != C2, position(P), assigned(C1, P), assigned(C2, P).

% T is performed either immediately before F or immediately after R
% This means: either F = T+1, or T = R+1
:- assigned(t, T), assigned(f, F), assigned(r, R), F != T + 1, T != R + 1.

% At least two compositions are performed either after F and before R, or after R and before F
% This means |position(F) - position(R)| >= 3 (at least 2 compositions between them)
:- assigned(f, F), assigned(r, R), abs(F - R) < 3.

% O is performed either first or fifth
:- assigned(o, P), P != 1, P != 5.

% The eighth composition performed is either L or H
:- assigned(C, 8), C != l, C != h.

% P is performed at some time before S
:- assigned(p, P), assigned(s, S), P >= S.

% At least one composition is performed either after O and before S, or after S and before O
% This means |position(O) - position(S)| >= 2
:- assigned(o, O), assigned(s, S), abs(O - S) < 2.

% --- Question-specific constraint: O is performed immediately after T ---
% This means position(O) = position(T) + 1
:- assigned(t, T), assigned(o, O), O != T + 1.

% --- Derive the position of F ---
position_of_f(P) :- assigned(f, P).

% --- Map F's position to answer choices ---
% (A) first or second
option(a) :- position_of_f(1).
option(a) :- position_of_f(2).

% (B) second or third
option(b) :- position_of_f(2).
option(b) :- position_of_f(3).

% (C) fourth or sixth
option(c) :- position_of_f(4).
option(c) :- position_of_f(6).

% (D) fourth or seventh
option(d) :- position_of_f(4).
option(d) :- position_of_f(7).

% (E) sixth or seventh
option(e) :- position_of_f(6).
option(e) :- position_of_f(7).

#show option/1.