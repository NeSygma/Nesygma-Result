% Define the articles and their topics
article(g; h; j; q; r; s; y).

% Topics:
% Finance: g, h, j
% Nutrition: q, r, s
% Wildlife: y

% Topic assignment
finance(g). finance(h). finance(j).
nutrition(q). nutrition(r). nutrition(s).
wildlife(y).

% Position (1..7)
position(1..7).

% Assign each article to a unique position
1 { assigned(A, P) : position(P) } 1 :- article(A).

% Ensure no two articles share the same position
:- assigned(A1, P), assigned(A2, P), A1 != A2.

% Consecutive articles cannot cover the same topic
:- assigned(A1, P), assigned(A2, P+1), topic(A1, T), topic(A2, T).

% Topic predicate for convenience
topic(A, T) :- assigned(A, P), finance(A), T = finance.
topic(A, T) :- assigned(A, P), nutrition(A), T = nutrition.
topic(A, T) :- assigned(A, P), wildlife(A), T = wildlife.

% S can be earlier than Q only if Q is third
:- assigned(s, P1), assigned(q, P2), P1 < P2, P2 != 3.

% S must be earlier than Y
:- assigned(s, P1), assigned(y, P2), P1 >= P2.

% J must be earlier than G, and G must be earlier than R
:- assigned(j, P1), assigned(g, P2), P1 >= P2.
:- assigned(g, P1), assigned(r, P2), P1 >= P2.

% Define the answer choices as possible scenarios
% (A) G is second
answer_a :- assigned(g, 2).

% (B) H is second
answer_b :- assigned(h, 2).

% (C) S is second
answer_c :- assigned(s, 2).

% (D) R is third
answer_d :- assigned(r, 3).

% (E) Y is third
answer_e :- assigned(y, 3).

% Map the correct answer to option/1
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.