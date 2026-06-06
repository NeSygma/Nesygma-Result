%% Domain
position(1..7).
article(g;h;j;q;r;s;y).

%% Topics
topic(g, fin). topic(h, fin). topic(j, fin).
topic(q, nut). topic(r, nut). topic(s, nut).
topic(y, wild).

%% Each position gets exactly one article; each article gets exactly one position
1 { assign(A, P) : article(A) } 1 :- position(P).
1 { assign(A, P) : position(P) } 1 :- article(A).

%% Consecutive articles cannot have the same topic
:- assign(A1, P), assign(A2, P+1), topic(A1, T), topic(A2, T), position(P), P < 7.

%% S can be earlier than Q only if Q is third
:- assign(s, Ps), assign(q, Pq), Ps < Pq, Pq != 3.

%% S must be earlier than Y
:- assign(s, Ps), assign(y, Py), Ps >= Py.

%% J < G < R
:- assign(j, Pj), assign(g, Pg), Pj >= Pg.
:- assign(g, Pg), assign(r, Pr), Pg >= Pr.

#show assign/2.