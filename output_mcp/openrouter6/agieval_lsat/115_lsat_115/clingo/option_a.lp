% Articles
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

% Positions
position(1..7).

% Topics
topic(g, f). topic(h, f). topic(j, f).
topic(q, n). topic(r, n). topic(s, n).
topic(y, w).

% Assignment: each position has exactly one article, each article exactly one position
1 { pos(A, P) : article(A) } 1 :- position(P).
1 { pos(A, P) : position(P) } 1 :- article(A).

% No two consecutive same topic
:- pos(A1, P), pos(A2, P+1), topic(A1, T1), topic(A2, T2), T1 = T2.

% S < Y
:- pos(s, Ps), pos(y, Py), Ps >= Py.

% J < G < R
:- pos(j, Pj), pos(g, Pg), Pj >= Pg.
:- pos(g, Pg), pos(r, Pr), Pg >= Pr.

% S < Q only if Q is third
% Forbid S < Q when Q != 3
:- pos(s, Ps), pos(q, Pq), Ps < Pq, Pq != 3.

% Option A: H is fourth
pos(h, 4).

#show pos/2.