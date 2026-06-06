% Define the compositions and their positions
compositions(f; h; l; o; p; r; s; t).
positions(1..8).

% Assign each composition to a unique position
1 { assigned(C, P) : compositions(C) } 1 :- positions(P).
:- assigned(C1, P), assigned(C2, P), C1 != C2.

% T is performed either immediately before F or immediately after R
:- assigned(t, P), assigned(f, P+1), not assigned(r, P-1).
:- assigned(t, P), assigned(r, P-1), not assigned(f, P+1).

% At least two compositions are performed either after F and before R, or after R and before F
:- assigned(f, P1), assigned(r, P2), P1 < P2, (P2 - P1 - 1) < 2.
:- assigned(r, P1), assigned(f, P2), P1 < P2, (P2 - P1 - 1) < 2.

% O is performed either first or fifth
:- assigned(o, P), P != 1, P != 5.

% The eighth composition performed is either L or H
:- assigned(C, 8), C != l, C != h.

% P is performed at some time before S
:- assigned(s, P1), assigned(p, P2), P2 >= P1.

% At least one composition is performed either after O and before S, or after S and before O
:- assigned(o, P1), assigned(s, P2), P1 < P2, (P2 - P1 - 1) < 1.
:- assigned(s, P1), assigned(o, P2), P1 < P2, (P2 - P1 - 1) < 1.

% Additional constraints for the specific scenario: P is third and S is sixth
:- not assigned(p, 3).
:- not assigned(s, 6).

% Derive the fifth composition
fifth(f) :- assigned(f, 5).
fifth(h) :- assigned(h, 5).
fifth(l) :- assigned(l, 5).
fifth(o) :- assigned(o, 5).
fifth(p) :- assigned(p, 5).
fifth(r) :- assigned(r, 5).
fifth(s) :- assigned(s, 5).
fifth(t) :- assigned(t, 5).

% Map the correct answer to option/1 based on the fifth composition
% Answer choices:
% (A) F or H
% (B) F or O
% (C) F or T
% (D) H or L
% (E) O or R

% Ensure only one option is selected
1 { option(a) ; option(b) ; option(c) ; option(d) ; option(e) } 1.

% Define the conditions for each option
option(a) :- fifth(f).
option(a) :- fifth(h).

option(b) :- fifth(f).
option(b) :- fifth(o).

option(c) :- fifth(f).
option(c) :- fifth(t).

option(d) :- fifth(h).
option(d) :- fifth(l).

option(e) :- fifth(o).
option(e) :- fifth(r).

% Show the selected option
#show option/1.