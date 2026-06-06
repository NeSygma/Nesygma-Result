% Define the books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(top). shelf(middle). shelf(bottom).

% Define shelf hierarchy (higher shelf means closer to top)
higher(top, middle).
higher(middle, bottom).
higher(top, bottom).

% Each book is on exactly one shelf
1 { on(B, S) : shelf(S) } 1 :- book(B).

% At least two books on each shelf
:- shelf(S), #count{ B : on(B, S) } < 2.

% More books on the bottom shelf than the top shelf
:- shelf(S1), shelf(S2), S1 = top, S2 = bottom, 
   #count { B : on(B, S1) } >= #count { B : on(B, S2) }.

% Given conditions
on(i, middle).

% K is on a higher shelf than F
:- on(f, S1), on(k, S2), shelf(S1), shelf(S2), not higher(S2, S1).

% O is on a higher shelf than L
:- on(l, S1), on(o, S2), shelf(S1), shelf(S2), not higher(S2, S1).

% F is on the same shelf as M
:- on(f, S), on(m, S1), S != S1.

% Option A: I and M are on the same shelf
option(a) :- on(i, S), on(m, S).

% Option B: K and G are on the same shelf
option(b) :- on(k, S), on(g, S).

% Option C: L and F are on the same shelf
option(c) :- on(l, S), on(f, S).

% Option D: M and H are on the same shelf
option(d) :- on(m, S), on(h, S).

% Option E: H and O are on the same shelf
option(e) :- on(h, S), on(o, S).

#show option/1.