% Articles and their topics
article(g; h; j; q; r; s; y).

finance(g; h; j).
nutrition(q; r; s).
wildlife(y).

% Positions
position(1..7).

% Assign each article to a position
1 { assigned(A, P) : position(P) } 1 :- article(A).
1 { assigned(A, P) : article(A) } 1 :- position(P).

% Helper: position of an article
pos(A, P) :- assigned(A, P).

% Helper predicate: same_topic(A1, A2) means A1 and A2 cover the same topic
same_topic(A1, A2) :- finance(A1), finance(A2).
same_topic(A1, A2) :- nutrition(A1), nutrition(A2).
same_topic(A1, A2) :- wildlife(A1), wildlife(A2).

% Constraint 1: Consecutive articles cannot cover the same topic
:- assigned(A1, P), assigned(A2, P+1), P < 7, same_topic(A1, A2).

% Constraint 2: S can be earlier than Q only if Q is third
% This means: if S is before Q, then Q must be at position 3
:- pos(s, Ps), pos(q, Pq), Ps < Pq, Pq != 3.

% Constraint 3: S must be earlier than Y
:- pos(s, Ps), pos(y, Py), Ps >= Py.

% Constraint 4: J must be earlier than G, and G must be earlier than R
:- pos(j, Pj), pos(g, Pg), Pj >= Pg.
:- pos(g, Pg), pos(r, Pr), Pg >= Pr.

% Possible positions for S
possible_pos(P) :- pos(s, P).

% If a position is not possible for S, derive the corresponding option
option(a) :- not possible_pos(1).
option(b) :- not possible_pos(3).
option(c) :- not possible_pos(4).
option(d) :- not possible_pos(5).
option(e) :- not possible_pos(6).

#show option/1.