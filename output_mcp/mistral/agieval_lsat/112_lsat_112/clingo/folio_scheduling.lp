% Domain: Articles and their topics
article(g; h; j; q; r; s; y).
topic(g, finance). topic(h, finance). topic(j, finance).
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition).
topic(y, wildlife).

% Positions (1 through 7)
position(1..7).

% Assign each article to exactly one position
1 { position(A, P) : position(P) } 1 :- article(A).

% Helper: article at position P
at_position(P, A) :- position(A, P).

% Helper: topic at position P
% Use a choice rule to ground topic_at/2 properly
topic_at(P, T) :- at_position(P, A), topic(A, T).

% Constraint 1: Consecutive articles cannot cover the same topic
:- topic_at(P, T), topic_at(P+1, T), position(P), position(P+1).

% Constraint 2: S can be earlier than Q only if Q is third
:- position(s, Ps), position(q, Pq), Ps < Pq, Pq != 3.

% Constraint 3: S must be earlier than Y
:- position(s, Ps), position(y, Py), Ps >= Py.

% Constraint 4: J must be earlier than G, and G must be earlier than R
:- position(j, Pj), position(g, Pg), Pj >= Pg.
:- position(g, Pg), position(r, Pr), Pg >= Pr.

% --- Multiple Choice Options ---
% A: G is second
could_be_a :- position(g, 2).

% B: H is second
could_be_b :- position(h, 2).

% C: S is second
could_be_c :- position(s, 2).

% D: R is third
could_be_d :- position(r, 3).

% E: Y is third
could_be_e :- position(y, 3).

% Map the correct answer to option/1
option(a) :- could_be_a.
option(b) :- could_be_b.
option(c) :- could_be_c.
option(d) :- could_be_d.
option(e) :- could_be_e.

#show option/1.