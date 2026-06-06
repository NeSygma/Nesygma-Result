% Define the articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

finance(g). finance(h). finance(j).
nutrition(q). nutrition(r). nutrition(s).
wildlife(y).

% Define positions (1 through 7)
position(1..7).

% Assign each article to exactly one position
1 { assigned(A, P) : position(P) } 1 :- article(A).

% Each position has exactly one article
1 { assigned(A, P) : article(A) } 1 :- position(P).

% Given condition: J is third
assigned(j, 3).

% Define topic at each position
finance_at(P) :- assigned(A, P), finance(A).
nutrition_at(P) :- assigned(A, P), nutrition(A).
wildlife_at(P) :- assigned(A, P), wildlife(A).

% Constraint 1: Consecutive articles cannot cover the same topic
:- finance_at(P), finance_at(P+1), P < 7.
:- nutrition_at(P), nutrition_at(P+1), P < 7.
:- wildlife_at(P), wildlife_at(P+1), P < 7.

% Constraint 2: S must be earlier than Y
:- assigned(s, P1), assigned(y, P2), P1 >= P2.

% Constraint 3: J must be earlier than G, and G must be earlier than R
:- assigned(j, Pj), assigned(g, Pg), Pj >= Pg.
:- assigned(g, Pg), assigned(r, Pr), Pg >= Pr.

% Constraint 4: S can be earlier than Q only if Q is third
% Since J is third, Q cannot be third, so S must be after Q
:- assigned(s, P1), assigned(q, P2), P1 < P2.

% Ensure Q is not third (since J is third)
:- assigned(q, 3).

% Map answer choices to conditions
% A: G is fourth
option(a) :- assigned(g, 4), not option(b), not option(c), not option(d), not option(e).

% B: H is sixth
option(b) :- assigned(h, 6), not option(a), not option(c), not option(d), not option(e).

% C: Q is first
option(c) :- assigned(q, 1), not option(a), not option(b), not option(d), not option(e).

% D: S is second
option(d) :- assigned(s, 2), not option(a), not option(b), not option(c), not option(e).

% E: Y is fifth
option(e) :- assigned(y, 5), not option(a), not option(b), not option(c), not option(d).

#show option/1.