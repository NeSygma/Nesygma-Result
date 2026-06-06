% Base facts: articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

% Topics: finance (g, h, j), nutrition (q, r, s), wildlife (y)
topic(g, finance). topic(h, finance). topic(j, finance).
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition).
topic(y, wildlife).

% Positions: 1 to 7
position(1..7).

% Assign each article to a unique position
1 { assigned(A, P) : position(P) } 1 :- article(A).
:- assigned(A1, P), assigned(A2, P), A1 != A2.

% Consecutive articles cannot cover the same topic
:- assigned(A1, P1), assigned(A2, P2), P2 = P1 + 1, topic(A1, T), topic(A2, T).

% S can be earlier than Q only if Q is third
:- assigned(s, P1), assigned(q, P2), P1 < P2, P2 != 3.

% S must be earlier than Y
:- assigned(s, P1), assigned(y, P2), P1 >= P2.

% J must be earlier than G, and G must be earlier than R
:- assigned(j, Pj), assigned(g, Pg), Pj >= Pg.
:- assigned(g, Pg), assigned(r, Pr), Pg >= Pr.

% Given: J is third
:- not assigned(j, 3).

% Map the correct answer to option/1
% (A) G is fourth
option(a) :- assigned(g, 4).

% (B) H is sixth
option(b) :- assigned(h, 6).

% (C) Q is first
option(c) :- assigned(q, 1).

% (D) S is second
option(d) :- assigned(s, 2).

% (E) Y is fifth
option(e) :- assigned(y, 5).

#show option/1.