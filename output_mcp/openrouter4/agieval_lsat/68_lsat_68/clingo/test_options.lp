% Domain
book(f; g; h; i; k; l; m; o).
shelf(top; middle; bottom).

% Higher order: top > middle > bottom
higher(top, middle). higher(top, bottom). higher(middle, bottom).

% Each book on exactly one shelf
1 { placed_on(B, S) : shelf(S) } 1 :- book(B).

% At least 2 books per shelf
:- shelf(S), #count { B : placed_on(B, S) } < 2.

% More books on bottom than top
:- #count { B : placed_on(B, bottom) } <= #count { B : placed_on(B, top) }.

% I is on middle
placed_on(i, middle).

% K is on a higher shelf than F
:- placed_on(k, SK), placed_on(f, SF), not higher(SK, SF).

% O is on a higher shelf than L
:- placed_on(o, SO), placed_on(l, SL), not higher(SO, SL).

% F and M are on the same shelf
:- placed_on(f, S1), placed_on(m, S2), S1 != S2.

% Option A: O is higher than M?
% Let's test if there's a model where O is NOT higher than M
:- placed_on(o, SO), placed_on(m, SM), higher(SO, SM).

#show placed_on/2.