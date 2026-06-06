% Books and shelves
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).
shelf(1). shelf(2). shelf(3). % 1=top, 2=middle, 3=bottom

% Each book is placed on exactly one shelf
1 { placed(B, S) : shelf(S) } 1 :- book(B).

% At least two books per shelf
:- shelf(S), #count { B : placed(B, S) } < 2.

% More books on bottom than top
count_top(N) :- N = #count { B : placed(B, 1) }.
count_bottom(N) :- N = #count { B : placed(B, 3) }.
:- count_top(N1), count_bottom(N2), N2 <= N1.

% I is on middle shelf
placed(i, 2).

% K is on a higher shelf than F (higher shelf means smaller number)
:- placed(k, S1), placed(f, S2), S1 >= S2.

% O is on a higher shelf than L
:- placed(o, S1), placed(l, S2), S1 >= S2.

% F and M are on the same shelf
:- placed(f, S1), placed(m, S2), S1 != S2.

% Conditional: L is on a higher shelf than H
:- placed(l, S1), placed(h, S2), S1 >= S2.

% Define options
option_a :- placed(f, S), placed(g, S).
option_b :- placed(g, S), placed(h, S).
option_c :- placed(h, S), placed(m, S).
option_d :- placed(i, S), placed(g, S).
option_e :- placed(k, S), placed(o, S).

#show placed/2.
#show option_a.
#show option_b.
#show option_c.
#show option_d.
#show option_e.