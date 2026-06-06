% DNA Fragments
fragment(0, a, t, c, g, a, t, c, g).
fragment(1, c, g, a, t, c, g, t, a).
fragment(2, a, t, c, g, t, a, a, c).
fragment(3, c, g, t, a, a, c, g, g).
fragment(4, t, a, a, c, g, g, c, t).
fragment(5, a, c, g, g, c, t, g, a).
fragment(6, g, g, c, t, g, a, a, a).
fragment(7, c, t, g, a, a, a, t, c).

% Helper to get character at index (0-indexed)
char(ID, 0, C) :- fragment(ID, C, _, _, _, _, _, _, _).
char(ID, 1, C) :- fragment(ID, _, C, _, _, _, _, _, _).
char(ID, 2, C) :- fragment(ID, _, _, C, _, _, _, _, _).
char(ID, 3, C) :- fragment(ID, _, _, _, C, _, _, _, _).
char(ID, 4, C) :- fragment(ID, _, _, _, _, C, _, _, _).
char(ID, 5, C) :- fragment(ID, _, _, _, _, _, C, _, _).
char(ID, 6, C) :- fragment(ID, _, _, _, _, _, _, C, _).
char(ID, 7, C) :- fragment(ID, _, _, _, _, _, _, _, C).

% Precompute overlap lengths
% overlap(ID1, ID2, L)
% Suffix of S1 of length L (indices 8-L to 7) matches prefix of S2 of length L (indices 0 to L-1)
overlap(ID1, ID2, L) :- 
    fragment(ID1, _, _, _, _, _, _, _, _), 
    fragment(ID2, _, _, _, _, _, _, _, _), 
    ID1 != ID2,
    L = 3..7,
    match(ID1, ID2, L).

match(ID1, ID2, L) :-
    fragment(ID1, _, _, _, _, _, _, _, _), 
    fragment(ID2, _, _, _, _, _, _, _, _), 
    L = 3..7,
    #count { I : I = 0..L-1, char(ID1, 8-L+I, C), char(ID2, I, C) } = L.

% --- Assembly Logic ---
% Each fragment used exactly once
{ pos(ID, P) : P = 0..7 } = 1 :- fragment(ID, _, _, _, _, _, _, _, _).
{ pos(ID, P) : fragment(ID, _, _, _, _, _, _, _, _) } = 1 :- P = 0..7.

% Define next relationship
next(ID1, ID2) :- pos(ID1, P), pos(ID2, P+1).

% Constraints
% Adjacent fragments must have overlap >= 3
:- next(ID1, ID2), not overlap(ID1, ID2, _).

% Objective: Maximize total overlap
#maximize { L, ID1, ID2 : next(ID1, ID2), overlap(ID1, ID2, L) }.

% Output
#show next/2.
#show pos/2.
#show overlap/3.