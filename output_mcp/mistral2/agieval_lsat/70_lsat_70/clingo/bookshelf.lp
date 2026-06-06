% Define the books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(top). shelf(middle). shelf(bottom).

% Each book is on exactly one shelf
1 { on(B, S) : shelf(S) } 1 :- book(B).

% At least two books on each shelf
:- shelf(S), #count{ B : on(B, S) } < 2.

% More books on the bottom shelf than the top shelf
bottom_count(N) :- N = #count{ B : on(B, bottom) }.
top_count(N) :- N = #count{ B : on(B, top) }.
:- bottom_count(B), top_count(T), B =< T.

% Given conditions
on(i, middle).

% K is on a higher shelf than F
:- on(f, S1), on(k, S2), shelf(S1), shelf(S2), higher(S2, S1).

% O is on a higher shelf than L
:- on(l, S1), on(o, S2), shelf(S1), shelf(S2), higher(S2, S1).

% F is on the same shelf as M
:- on(f, S), on(m, S1), S != S1.

% Define shelf hierarchy (higher means closer to top)
higher(top, middle).
higher(middle, bottom).
higher(top, bottom).

% Given condition: L is on a shelf higher than H
:- on(h, S1), on(l, S2), shelf(S1), shelf(S2), not higher(S2, S1).

% Define the answer choices as conditions
% (A) F and G are on the same shelf
same_shelf(f, g) :- on(f, S), on(g, S).

% (B) G and H are on the same shelf
same_shelf(g, h) :- on(g, S), on(h, S).

% (C) H and M are on the same shelf
same_shelf(h, m) :- on(h, S), on(m, S).

% (D) I and G are on the same shelf
same_shelf(i, g) :- on(i, S), on(g, S).

% (E) K and O are on the same shelf
same_shelf(k, o) :- on(k, S), on(o, S).

% Map the correct answer to option/1
option(a) :- same_shelf(f, g).
option(b) :- same_shelf(g, h).
option(c) :- same_shelf(h, m).
option(d) :- same_shelf(i, g).
option(e) :- same_shelf(k, o).

#show option/1.