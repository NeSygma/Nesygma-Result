% Base facts: compositions and their positions
composition(f; h; l; o; p; r; s; t).
position(1..8).

% Assign each composition to a unique position
1 { assigned(C, P) : position(P) } 1 :- composition(C).

% Ensure no two compositions share the same position
:- assigned(C1, P), assigned(C2, P), C1 != C2.

% T is performed either immediately before F or immediately after R
:- assigned(t, P), assigned(f, P+1), not assigned(r, P-1).
:- assigned(t, P), assigned(r, P-1), not assigned(f, P+1).

% At least two compositions are performed either after F and before R, or after R and before F
% This means the positions of F and R must have at least two compositions between them in one direction
:- assigned(f, PF), assigned(r, PR), PF < PR, PR - PF - 1 < 2.
:- assigned(f, PF), assigned(r, PR), PF > PR, PF - PR - 1 < 2.

% O is performed either first or fifth
:- assigned(o, P), P != 1, P != 5.

% The eighth composition performed is either L or H
:- assigned(C, 8), C != l, C != h.

% P is performed at some time before S
:- assigned(s, PS), assigned(p, PP), PS < PP.

% At least one composition is performed either after O and before S, or after S and before O
% This means the positions of O and S must have at least one composition between them in one direction
:- assigned(o, PO), assigned(s, PS), PO < PS, PS - PO - 1 < 1.
:- assigned(o, PO), assigned(s, PS), PO > PS, PO - PS - 1 < 1.

% Given conditions: T is performed fifth and F is performed sixth
assigned(t, 5).
assigned(f, 6).

% Derive the position of S
position(S) :- assigned(s, S).

% Map the correct answer to option/1 based on the position of S
% (A) fourth or seventh
option(a) :- assigned(s, 4).
option(a) :- assigned(s, 7).

% (B) third or sixth
option(b) :- assigned(s, 3).
option(b) :- assigned(s, 6).

% (C) third or fourth
option(c) :- assigned(s, 3).
option(c) :- assigned(s, 4).

% (D) second or seventh
option(d) :- assigned(s, 2).
option(d) :- assigned(s, 7).

% (E) first or fourth
option(e) :- assigned(s, 1).
option(e) :- assigned(s, 4).

#show option/1.