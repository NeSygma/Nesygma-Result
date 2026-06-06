% Articles and topics (use lowercase constants)
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

topic(g, finance). topic(h, finance). topic(j, finance).
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition).
topic(y, wildlife).

% Positions 1 to 7
position(1..7).

% Permutation: each position gets exactly one article
1 { position(A, P) : article(A) } 1 :- position(P).
% Each article gets exactly one position
1 { position(A, P) : position(P) } 1 :- article(A).

% Constraint 1: Consecutive articles cannot cover the same topic
:- position(A, P), position(B, P+1), topic(A, T1), topic(B, T2), T1 = T2.

% Constraint 2: S can be earlier than Q only if Q is third
:- position(s, Ps), position(q, Pq), Ps < Pq, Pq != 3.

% Constraint 3: S must be earlier than Y
:- position(s, Ps), position(y, Py), Ps >= Py.

% Constraint 4: J must be earlier than G, and G must be earlier than R
:- position(j, Pj), position(g, Pg), Pj >= Pg.
:- position(g, Pg), position(r, Pr), Pg >= Pr.

% Options
option(a) :- position(g, 2).
option(b) :- position(h, 2).
option(c) :- position(s, 2).
option(d) :- position(r, 3).
option(e) :- position(y, 3).

% Ensure at least one option is true (assuming at least one is possible)
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.