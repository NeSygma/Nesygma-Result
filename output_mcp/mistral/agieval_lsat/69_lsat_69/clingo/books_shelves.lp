% Books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(top). shelf(middle). shelf(bottom).

% Higher shelf relationship (top > middle > bottom)
higher(S1, S2) :- shelf(S1), shelf(S2), S1 = top, S2 = middle.
higher(S1, S2) :- shelf(S1), shelf(S2), S1 = top, S2 = bottom.
higher(S1, S2) :- shelf(S1), shelf(S2), S1 = middle, S2 = bottom.

% Each book must be on exactly one shelf
1 { placed_on(B, S) : shelf(S) } 1 :- book(B).

% Helper predicates for counting books on each shelf
books_on_shelf(S, N) :- shelf(S), N = #count { B : placed_on(B, S) }.

% At least 2 books per shelf
:- shelf(S), books_on_shelf(S, N), N < 2.

% More books on bottom than top
:- books_on_shelf(top, N1), books_on_shelf(bottom, N2), N2 <= N1.

% I is on middle shelf
:- not placed_on(i, middle).

% K is on a higher shelf than F
:- placed_on(f, S1), placed_on(k, S2), not higher(S1, S2).

% O is on a higher shelf than L
:- placed_on(l, S1), placed_on(o, S2), not higher(S1, S2).

% F is on the same shelf as M
:- placed_on(f, S), placed_on(m, S1), S != S1.

% Condition: G is on top shelf
:- not placed_on(g, top).

% Define the options
% Option A: H, I on middle shelf (exactly these two)
option(a) :- placed_on(h, middle), placed_on(i, middle),
             books_on_shelf(middle, 2),
             not placed_on(l, middle),
             not placed_on(k, middle),
             not placed_on(f, middle),
             not placed_on(m, middle),
             not placed_on(o, middle),
             not placed_on(g, middle).

% Option B: I, L on middle shelf (exactly these two)
option(b) :- placed_on(i, middle), placed_on(l, middle),
             books_on_shelf(middle, 2),
             not placed_on(h, middle),
             not placed_on(k, middle),
             not placed_on(f, middle),
             not placed_on(m, middle),
             not placed_on(o, middle),
             not placed_on(g, middle).

% Option C: H, I, L on middle shelf (exactly these three)
option(c) :- placed_on(h, middle), placed_on(i, middle), placed_on(l, middle),
             books_on_shelf(middle, 3),
             not placed_on(k, middle),
             not placed_on(f, middle),
             not placed_on(m, middle),
             not placed_on(o, middle),
             not placed_on(g, middle).

% Option D: I, K, L on middle shelf (exactly these three)
option(d) :- placed_on(i, middle), placed_on(k, middle), placed_on(l, middle),
             books_on_shelf(middle, 3),
             not placed_on(h, middle),
             not placed_on(f, middle),
             not placed_on(m, middle),
             not placed_on(o, middle),
             not placed_on(g, middle).

% Option E: F, I, M on middle shelf (exactly these three)
option(e) :- placed_on(f, middle), placed_on(i, middle), placed_on(m, middle),
             books_on_shelf(middle, 3),
             not placed_on(h, middle),
             not placed_on(k, middle),
             not placed_on(l, middle),
             not placed_on(o, middle),
             not placed_on(g, middle).

#show option/1.