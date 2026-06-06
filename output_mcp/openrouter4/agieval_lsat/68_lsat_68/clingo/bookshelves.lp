% Domain
book(f; g; h; i; k; l; m; o).
shelf(top; middle; bottom).

% Higher order: top > middle > bottom
higher(top, middle). higher(top, bottom). higher(middle, bottom).
higher(S1, S3) :- higher(S1, S2), higher(S2, S3).

% Each book on exactly one shelf
1 { placed_on(B, S) : shelf(S) } 1 :- book(B).

% At least 2 books per shelf
:- shelf(S), N = #count { B : placed_on(B, S) }, N < 2.

% More books on bottom than top
:- Nbottom = #count { B : placed_on(B, bottom) }, Ntop = #count { B : placed_on(B, top) }, Nbottom <= Ntop.

% I is on middle
placed_on(i, middle).

% K is on a higher shelf than F
:- placed_on(k, SK), placed_on(f, SF), not higher(SK, SF).

% O is on a higher shelf than L
:- placed_on(o, SO), placed_on(l, SL), not higher(SO, SL).

% F and M are on the same shelf
:- placed_on(f, S1), placed_on(m, S2), S1 != S2.

% Show results
#show placed_on/2.