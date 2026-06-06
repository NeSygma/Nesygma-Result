% Define the books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(top). shelf(middle). shelf(bottom).

% Each book is placed on exactly one shelf
1 { placed_on(B, S) : shelf(S) } 1 :- book(B).

% At least two books are placed on each shelf
:- shelf(S), #count { B : placed_on(B, S) } < 2.

% More books are placed on the bottom shelf than the top shelf
:- shelf(S1), shelf(S2), S1 = top, S2 = bottom,
   #count { B : placed_on(B, S1) } >= #count { B : placed_on(B, S2) }.

% I is placed on the middle shelf
:- not placed_on(i, middle).

% Define a higher shelf relation: top > middle > bottom
higher(top, middle).
higher(middle, bottom).
higher(top, bottom).

% K is placed on a higher shelf than F
:- placed_on(f, S1), placed_on(k, S2), not higher(S2, S1).

% O is placed on a higher shelf than L
:- placed_on(l, S2), placed_on(o, S1), not higher(S1, S2).

% F is placed on the same shelf as M
:- placed_on(f, S), not placed_on(m, S).

% Define the answer conditions for the multiple-choice options
% (A) O is placed on a shelf higher than the shelf M is placed on.
option(a) :- placed_on(o, S1), placed_on(m, S2), higher(S1, S2).

% (B) K is placed on a shelf higher than the shelf G is placed on.
option(b) :- placed_on(k, S1), placed_on(g, S2), higher(S1, S2).

% (C) I is placed on a shelf higher than the shelf F is placed on.
option(c) :- placed_on(i, S1), placed_on(f, S2), higher(S1, S2).

% (D) G is placed on a shelf higher than the shelf O is placed on.
option(d) :- placed_on(g, S1), placed_on(o, S2), higher(S1, S2).

% (E) F is placed on a shelf higher than the shelf L is placed on.
option(e) :- placed_on(f, S1), placed_on(l, S2), higher(S1, S2).

#show option/1.