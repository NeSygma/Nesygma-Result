% Define the books and shelves
book(f;g;h;i;k;l;m;o).
shelf(top;middle;bottom).

% Define the higher relationship (higher shelf means closer to top)
higher(top, middle).
higher(top, bottom).
higher(middle, bottom).

% Choice rule: each book is placed on exactly one shelf
{ on_shelf(Book, Shelf) : shelf(Shelf) } 1 :- book(Book).

% At least two books on each shelf
:- shelf(S), { on_shelf(Book, S) : book(Book) } < 2.

% More books on bottom shelf than top shelf
:- { on_shelf(Book, top) : book(Book) } >= { on_shelf(Book, bottom) : book(Book) }.

% I is placed on the middle shelf
:- not on_shelf(i, middle).

% K is placed on a higher shelf than F
:- on_shelf(f, Sf), on_shelf(k, Sk), not higher(Sk, Sf).

% O is placed on a higher shelf than L
:- on_shelf(l, Sl), on_shelf(o, So), not higher(So, Sl).

% F is placed on the same shelf as M
:- on_shelf(f, S), not on_shelf(m, S).

% Map the options to conditions
% (A) O is placed on a shelf higher than the shelf M is placed on
option(a) :- on_shelf(m, Sm), on_shelf(o, So), higher(So, Sm).

% (B) K is placed on a shelf higher than the shelf G is placed on
option(b) :- on_shelf(g, Sg), on_shelf(k, Sk), higher(Sk, Sg).

% (C) I is placed on a shelf higher than the shelf F is placed on
option(c) :- on_shelf(f, Sf), higher(middle, Sf).

% (D) G is placed on a shelf higher than the shelf O is placed on
option(d) :- on_shelf(g, Sg), on_shelf(o, So), higher(Sg, So).

% (E) F is placed on a shelf higher than the shelf L is placed on
option(e) :- on_shelf(f, Sf), on_shelf(l, Sl), higher(Sf, Sl).

#show option/1.