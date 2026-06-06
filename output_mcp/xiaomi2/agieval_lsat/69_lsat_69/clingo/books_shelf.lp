% Domain: books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(top). shelf(middle). shelf(bottom).

% Higher shelf means closer to top: top > middle > bottom
higher(top, middle).
higher(top, bottom).
higher(middle, bottom).

% Each book is placed on exactly one shelf
1 { placed(B, S) : shelf(S) } 1 :- book(B).

% At least two books on each shelf
:- shelf(S), #count{B : placed(B, S)} < 2.

% More books on bottom than top
bottom_count(N) :- N = #count{B : placed(B, bottom)}.
top_count(N) :- N = #count{B : placed(B, top)}.
:- bottom_count(NB), top_count(NT), NB <= NT.

% I is placed on the middle shelf
placed(i, middle).

% K is placed on a higher shelf than F
:- placed(k, SK), placed(f, SF), not higher(SK, SF).

% O is placed on a higher shelf than L
:- placed(o, SO), placed(l, SL), not higher(SO, SL).

% F is placed on the same shelf as M
:- placed(f, SF), placed(m, SM), SF != SM.

% G is placed on the top shelf (conditional in question)
placed(g, top).

% Define what each option means - check if the middle shelf contains EXACTLY those books
% Option A: Middle shelf = {H, I}
mid_a :- placed(h, middle), placed(i, middle),
         not placed(f, middle), not placed(g, middle),
         not placed(k, middle), not placed(l, middle),
         not placed(m, middle), not placed(o, middle).

% Option B: Middle shelf = {I, L}
mid_b :- placed(i, middle), placed(l, middle),
         not placed(f, middle), not placed(g, middle),
         not placed(h, middle), not placed(k, middle),
         not placed(m, middle), not placed(o, middle).

% Option C: Middle shelf = {H, I, L}
mid_c :- placed(h, middle), placed(i, middle), placed(l, middle),
         not placed(f, middle), not placed(g, middle),
         not placed(k, middle), not placed(m, middle),
         not placed(o, middle).

% Option D: Middle shelf = {I, K, L}
mid_d :- placed(i, middle), placed(k, middle), placed(l, middle),
         not placed(f, middle), not placed(g, middle),
         not placed(h, middle), not placed(m, middle),
         not placed(o, middle).

% Option E: Middle shelf = {F, I, M}
mid_e :- placed(f, middle), placed(i, middle), placed(m, middle),
         not placed(g, middle), not placed(h, middle),
         not placed(k, middle), not placed(l, middle),
         not placed(o, middle).

option(a) :- mid_a.
option(b) :- mid_b.
option(c) :- mid_c.
option(d) :- mid_d.
option(e) :- mid_e.

#show option/1.