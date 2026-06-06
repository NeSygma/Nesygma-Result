% Books
book(f). book(g). book(h). book(i). book(k). book(l). book(m). book(o).

% Shelves
shelf(top). shelf(middle). shelf(bottom).

% Levels
level(top,3). level(middle,2). level(bottom,1).

% Choice rule: each book assigned to exactly one shelf
1 { shelf(B,S) : shelf(S) } 1 :- book(B).

% Bottom has
bottom_has(B) :- shelf(B,bottom).

% Constraints
% At least two books per shelf
:- #count{B : shelf(B,S)} < 2 :- shelf(S).

% Bottom > top
:- #count{B : shelf(B,bottom)} <= #count{B : shelf(B,top)}.

% I on middle
:- shelf(i,top).
:- shelf(i,bottom).

% K higher than F
:- shelf(k,S1), shelf(f,S2), level(S1,L1), level(S2,L2), L1 <= L2.

% O higher than L
:- shelf(o,S1), shelf(l,S2), level(S1,L1), level(S2,L2), L1 <= L2.

% F same shelf as M
:- shelf(f,S), not shelf(m,S).
:- shelf(m,S), not shelf(f,S).

% Option definitions
option(a) :- bottom_has(f), bottom_has(m), not bottom_has(g), not bottom_has(h), not bottom_has(i), not bottom_has(k), not bottom_has(l), not bottom_has(o).
option(b) :- bottom_has(f), bottom_has(h), bottom_has(m), not bottom_has(g), not bottom_has(i), not bottom_has(k), not bottom_has(l), not bottom_has(o).
option(c) :- bottom_has(g), bottom_has(h), bottom_has(k), not bottom_has(f), not bottom_has(i), not bottom_has(l), not bottom_has(m), not bottom_has(o).
option(d) :- bottom_has(f), bottom_has(g), bottom_has(m), bottom_has(o), not bottom_has(h), not bottom_has(i), not bottom_has(k), not bottom_has(l).
option(e) :- bottom_has(g), bottom_has(h), bottom_has(l), bottom_has(m), not bottom_has(f), not bottom_has(i), not bottom_has(k), not bottom_has(o).

% Exactly one option
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.