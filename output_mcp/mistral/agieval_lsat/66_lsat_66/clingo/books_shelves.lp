% Define the books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(top). shelf(middle). shelf(bottom).

% Each book is on exactly one shelf
1 { on(B, S) : shelf(S) } 1 :- book(B).

% Helper predicate to count books on a shelf
books_on_shelf(S, N) :- shelf(S), N = #count{B : on(B, S)}.

% At least two books on each shelf
:- shelf(S), books_on_shelf(S, N), N < 2.

% More books on bottom shelf than top shelf
:- shelf(top), shelf(bottom), books_on_shelf(top, N1), books_on_shelf(bottom, N2), N1 >= N2.

% I is on the middle shelf
on(i, middle).

% Define what it means for a shelf to be higher (top > middle > bottom)
higher(top, middle).
higher(top, bottom).
higher(middle, bottom).

% K is on a higher shelf than F
:- on(f, S1), on(k, S2), not higher(S2, S1).

% O is on a higher shelf than L
:- on(l, S1), on(o, S2), not higher(S2, S1).

% F is on the same shelf as M
:- on(f, S), on(m, S1), S != S1.

% Check each option for the bottom shelf
% Option A: F, M on bottom
option(a) :- on(f, bottom), on(m, bottom), books_on_shelf(bottom, 2).

% Option B: F, H, M on bottom
option(b) :- on(f, bottom), on(h, bottom), on(m, bottom), books_on_shelf(bottom, 3).

% Option C: G, H, K on bottom
option(c) :- on(g, bottom), on(h, bottom), on(k, bottom), books_on_shelf(bottom, 3).

% Option D: F, G, M, O on bottom
option(d) :- on(f, bottom), on(g, bottom), on(m, bottom), on(o, bottom), books_on_shelf(bottom, 4).

% Option E: G, H, L, M on bottom
option(e) :- on(g, bottom), on(h, bottom), on(l, bottom), on(m, bottom), books_on_shelf(bottom, 4).

#show option/1.