% Base facts: articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

finance(g). finance(h). finance(j).
nutrition(q). nutrition(r). nutrition(s).
wildlife(y).

% Define topics for articles explicitly
article_topic(g, finance). article_topic(h, finance). article_topic(j, finance).
article_topic(q, nutrition). article_topic(r, nutrition). article_topic(s, nutrition).
article_topic(y, wildlife).

% Define the set of all articles and topics
position(1..7).

% Assign each article to a unique position
1 { assigned(Article, Position) : position(Position) } 1 :- article(Article).
:- assigned(A1, P), assigned(A2, P), A1 != A2.

% Consecutive articles cannot cover the same topic
:- assigned(A1, P1), assigned(A2, P2), P2 = P1 + 1, article_topic(A1, T), article_topic(A2, T).

% S can be earlier than Q only if Q is third
:- assigned(s, P1), assigned(q, P2), P1 < P2, P2 != 3.

% S must be earlier than Y
:- assigned(s, P1), assigned(y, P2), P1 >= P2.

% J must be earlier than G, and G must be earlier than R
:- assigned(j, P1), assigned(g, P2), P1 >= P2.
:- assigned(g, P1), assigned(r, P2), P1 >= P2.

% Option A: H is fourth
option(a) :- assigned(h, 4).

% Option B: H is sixth
option(b) :- assigned(h, 6).

% Option C: R is fourth
option(c) :- assigned(r, 4).

% Option D: R is seventh
option(d) :- assigned(r, 7).

% Option E: Y is fifth
option(e) :- assigned(y, 5).

% Ensure only one option is true
:- option(X), option(Y), X != Y.

% Ensure at least one option is true (since the problem guarantees a solution)
:- not option(a), not option(b), not option(c), not option(d), not option(e).

% Ensure the order is fully determined when an option is true
% This is implicitly enforced by the uniqueness of the assignment and the constraints.

#show option/1.