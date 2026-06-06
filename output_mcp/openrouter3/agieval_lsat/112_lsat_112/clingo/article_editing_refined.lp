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

% For each answer choice, check if there exists a valid sequence where that condition holds
% We'll use separate runs for each choice, but since we need one file, we'll use choice rules

% Define which answer we're testing
{ test_choice(a); test_choice(b); test_choice(c); test_choice(d); test_choice(e) } 1.

% Apply the specific condition based on which choice we're testing
% (A) G is second
test_a :- test_choice(a), article_at(2, g).
% (B) H is second  
test_b :- test_choice(b), article_at(2, h).
% (C) S is second
test_c :- test_choice(c), article_at(2, s).
% (D) R is third
test_d :- test_choice(d), article_at(3, r).
% (E) Y is third
test_e :- test_choice(e), article_at(3, y).

% Only allow the test if the condition is satisfied
:- test_choice(a), not test_a.
:- test_choice(b), not test_b.
:- test_choice(c), not test_c.
:- test_choice(d), not test_d.
:- test_choice(e), not test_e.

% Map the correct answer to option/1
% We need to find which choice(s) are possible
option(a) :- test_choice(a), test_a.
option(b) :- test_choice(b), test_b.
option(c) :- test_choice(c), test_c.
option(d) :- test_choice(d), test_d.
option(e) :- test_choice(e), test_e.

#show option/1.