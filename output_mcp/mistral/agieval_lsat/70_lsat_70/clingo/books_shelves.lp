% Define shelves with ordering (1=top, 2=middle, 3=bottom)
shelf(top).
shelf(middle).
shelf(bottom).

% Define shelf ordering
shelf_order(top, 1).
shelf_order(middle, 2).
shelf_order(bottom, 3).

% Books
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).

% Assign books to shelves
1 { assigned(Book, Shelf) : shelf(Shelf) } 1 :- book(Book).

% At least two books per shelf
:- shelf(S), #count{Book : assigned(Book, S)} < 2.

% Precompute the number of books on top and bottom shelves
% Derive top_count(C) where C is the number of books on top shelf
top_count(C) :- C = #count{Book : assigned(Book, top), book(Book)}.

% Derive bottom_count(C) where C is the number of books on bottom shelf
bottom_count(C) :- C = #count{Book : assigned(Book, bottom), book(Book)}.

% More books on bottom shelf than top shelf
:- top_count(TC), bottom_count(BC), BC =< TC.

% I is on middle shelf
:- assigned(i, S), S != middle.

% K is on a higher shelf than F (K has smaller shelf number)
:- assigned(k, KShelf), assigned(f, FShelf),
   shelf_order(KShelf, KOrd), shelf_order(FShelf, FOrd),
   KOrd >= FOrd.

% O is on a higher shelf than L (O has smaller shelf number)
:- assigned(o, OShelf), assigned(l, LShelf),
   shelf_order(OShelf, OOrd), shelf_order(LShelf, LOrd),
   OOrd >= LOrd.

% F is on the same shelf as M
:- assigned(f, FShelf), assigned(m, MShelf), FShelf != MShelf.

% Condition: L is on a shelf higher than H (L has smaller shelf number than H)
:- assigned(l, LShelf), assigned(h, HShelf),
   shelf_order(LShelf, LOrd), shelf_order(HShelf, HOrd),
   LOrd >= HOrd.

% Define what it means for two books to be on the same shelf
same_shelf(B1, B2) :- assigned(B1, S), assigned(B2, S), B1 != B2.

% Now map the options:

% Option A: F and G are on the same shelf
option(a) :- same_shelf(f, g).

% Option B: G and H are on the same shelf
option(b) :- same_shelf(g, h).

% Option C: H and M are on the same shelf
option(c) :- same_shelf(h, m).

% Option D: I and G are on the same shelf
option(d) :- same_shelf(i, g).

% Option E: K and O are on the same shelf
option(e) :- same_shelf(k, o).

#show option/1.