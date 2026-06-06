% Define domains
book(f;g;h;i;k;l;m;o).
shelf(1..3).  % 1=top, 2=middle, 3=bottom

% Each book assigned to exactly one shelf
1 { assign(B, S) : shelf(S) } 1 :- book(B).

% Count books per shelf
count_shelf(S, C) :- shelf(S), C = #count{ B : assign(B, S) }.

% At least 2 books per shelf
:- count_shelf(S, C), C < 2.

% More books on bottom than top
:- count_shelf(3, C3), count_shelf(1, C1), C3 <= C1.

% I on middle (shelf 2)
:- not assign(i, 2).

% K higher than F (higher means smaller shelf number)
:- assign(k, Sk), assign(f, Sf), Sk >= Sf.

% O higher than L
:- assign(o, So), assign(l, Sl), So >= Sl.

% F and M same shelf
:- assign(f, Sf), assign(m, Sm), Sf != Sm.

% Additional condition: L higher than H
:- assign(l, Sl), assign(h, Sh), Sl >= Sh.

% Options
option_true(a) :- assign(f, S), assign(g, S).  % F and G same shelf
option_true(b) :- assign(g, S), assign(h, S).  % G and H same shelf
option_true(c) :- assign(h, S), assign(m, S).  % H and M same shelf
option_true(d) :- assign(i, S), assign(g, S).  % I and G same shelf
option_true(e) :- assign(k, S), assign(o, S).  % K and O same shelf

#show assign/2.
#show option_true/1.