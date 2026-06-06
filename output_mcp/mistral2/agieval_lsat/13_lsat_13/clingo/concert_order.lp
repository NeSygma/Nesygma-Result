% Define the compositions and their positions
composition(f; h; l; o; p; r; s; t).
position(1..8).

% Assign each composition to a unique position
1 { assigned(C, P) : position(P) } 1 :- composition(C).
:- assigned(C1, P), assigned(C2, P), C1 != C2.

% T is performed either immediately before F or immediately after R
:- assigned(t, P), assigned(f, P+1), not assigned(r, P-1).
:- assigned(t, P), assigned(r, P-1), not assigned(f, P+1).

% At least two compositions are performed either after F and before R, or after R and before F
:- assigned(f, P1), assigned(r, P2), P2 > P1 + 2, not (assigned(C, P) : position(P), P1 < P < P2).
:- assigned(r, P1), assigned(f, P2), P2 > P1 + 2, not (assigned(C, P) : position(P), P1 < P < P2).

% O is performed either first or fifth
:- assigned(o, P), P != 1, P != 5.

% The eighth composition performed is either L or H
:- assigned(C, 8), C != l, C != h.

% P is performed at some time before S
:- assigned(s, P1), assigned(p, P2), P2 >= P1.

% At least one composition is performed either after O and before S, or after S and before O
:- assigned(o, P1), assigned(s, P2), P2 > P1 + 1, not (assigned(C, P) : position(P), P1 < P < P2).
:- assigned(s, P1), assigned(o, P2), P2 > P1 + 1, not (assigned(C, P) : position(P), P1 < P < P2).

% Define the position of P
position_p(P) :- assigned(p, P).

% Map the correct answer to option/1
% P CANNOT be performed in certain positions
% We will derive the correct option based on the constraints

% If P cannot be in position 2, then option(a) is correct
option(a) :- not position_p(2).

% If P cannot be in position 3, then option(b) is correct
option(b) :- not position_p(3).

% If P cannot be in position 4, then option(c) is correct
option(c) :- not position_p(4).

% If P cannot be in position 6, then option(d) is correct
option(d) :- not position_p(6).

% If P cannot be in position 7, then option(e) is correct
option(e) :- not position_p(7).

#show option/1.