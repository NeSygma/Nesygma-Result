% Articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).
topic(finance). topic(nutrition). topic(wildlife).

% Assign topics to articles
has_topic(g, finance). has_topic(h, finance). has_topic(j, finance).
has_topic(q, nutrition). has_topic(r, nutrition). has_topic(s, nutrition).
has_topic(y, wildlife).

% Positions 1 through 7
position(1..7).

% Each article occupies exactly one position
1 { at_position(A, P) : position(P) } 1 :- article(A).

% Each position has exactly one article
1 { at_position(A, P) : article(A) } 1 :- position(P).

% Consecutive articles cannot have the same topic
:- at_position(A1, P), at_position(A2, P+1), has_topic(A1, T), has_topic(A2, T).

% S can be earlier than Q only if Q is third
% This means: if S is before Q, then Q must be at position 3
:- at_position(s, Ps), at_position(q, Pq), Ps < Pq, Pq != 3.

% S must be earlier than Y
:- at_position(s, Ps), at_position(y, Py), Ps >= Py.

% J must be earlier than G, and G must be earlier than R
:- at_position(j, Pj), at_position(g, Pg), Pj >= Pg.
:- at_position(g, Pg), at_position(r, Pr), Pg >= Pr.

% Helper: article at position
article_at(P, A) :- at_position(A, P).

% Check each answer choice in any valid sequence
possible_a :- article_at(2, g).
possible_b :- article_at(2, h).
possible_c :- article_at(2, s).
possible_d :- article_at(3, r).
possible_e :- article_at(3, y).

% Map the correct answer to option/1
% We need to find which choice(s) are possible in at least one valid sequence
option(a) :- possible_a.
option(b) :- possible_b.
option(c) :- possible_c.
option(d) :- possible_d.
option(e) :- possible_e.

#show option/1.