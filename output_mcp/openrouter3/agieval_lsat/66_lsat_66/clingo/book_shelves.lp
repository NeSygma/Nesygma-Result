% Books
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).

% Shelves (ordered: top=1, middle=2, bottom=3)
shelf(1). shelf(2). shelf(3).

% Each book is on exactly one shelf
1 { on(Book, Shelf) : shelf(Shelf) } 1 :- book(Book).

% At least 2 books per shelf
:- shelf(S), #count{Book : on(Book, S)} < 2.

% Condition 1: More books on bottom shelf than top shelf
bottom_more_than_top :- #count{Book : on(Book, 3)} > #count{Book : on(Book, 1)}.
:- not bottom_more_than_top.

% Condition 2: I is on middle shelf
on(i, 2).

% Condition 3: K is on a higher shelf than F
% Higher shelf means smaller number (top=1 is highest)
:- on(k, Sk), on(f, Sf), Sk >= Sf.

% Condition 4: O is on a higher shelf than L
:- on(o, So), on(l, Sl), So >= Sl.

% Condition 5: F is on the same shelf as M
:- on(f, Sf), on(m, Sm), Sf != Sm.

% Helper: Count books on each shelf (using aggregate in body)
count_top(N) :- N = #count{Book : on(Book, 1)}.
count_middle(N) :- N = #count{Book : on(Book, 2)}.
count_bottom(N) :- N = #count{Book : on(Book, 3)}.

% Test each option for bottom shelf
% Option A: F, M
option_a :- on(f, 3), on(m, 3), 
            count_bottom(2),
            not on(g, 3), not on(h, 3), not on(i, 3), not on(k, 3), not on(l, 3), not on(o, 3).

% Option B: F, H, M
option_b :- on(f, 3), on(h, 3), on(m, 3),
            count_bottom(3),
            not on(g, 3), not on(i, 3), not on(k, 3), not on(l, 3), not on(o, 3).

% Option C: G, H, K
option_c :- on(g, 3), on(h, 3), on(k, 3),
            count_bottom(3),
            not on(f, 3), not on(i, 3), not on(l, 3), not on(m, 3), not on(o, 3).

% Option D: F, G, M, O
option_d :- on(f, 3), on(g, 3), on(m, 3), on(o, 3),
            count_bottom(4),
            not on(h, 3), not on(i, 3), not on(k, 3), not on(l, 3).

% Option E: G, H, L, M
option_e :- on(g, 3), on(h, 3), on(l, 3), on(m, 3),
            count_bottom(4),
            not on(f, 3), not on(i, 3), not on(k, 3), not on(o, 3).

% Map the correct answer to option/1
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.