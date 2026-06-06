% Articles and topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).
topic(g, finance). topic(h, finance). topic(j, finance). 
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition). 
topic(y, wildlife).

% Positions
position(1..7).

% Orders (each order is a set of facts order(Order, Article, Position))
order(a, h, 1). order(a, s, 2). order(a, j, 3). order(a, q, 4). order(a, y, 5). order(a, g, 6). order(a, r, 7).
order(b, j, 1). order(b, q, 2). order(b, g, 3). order(b, h, 4). order(b, s, 5). order(b, y, 6). order(b, r, 7).
order(c, q, 1). order(c, j, 2). order(c, s, 3). order(c, h, 4). order(c, y, 5). order(c, g, 6). order(c, r, 7).
order(d, q, 1). order(d, j, 2). order(d, y, 3). order(d, s, 4). order(d, g, 5). order(d, r, 6). order(d, h, 7).
order(e, s, 1). order(e, g, 2). order(e, q, 3). order(e, j, 4). order(e, y, 5). order(e, r, 6). order(e, h, 7).

% Violation predicates
% 1. Consecutive articles cannot cover the same topic.
violates_consecutive_same_topic(Order) :-
    order(Order, A1, P),
    order(Order, A2, P+1),
    topic(A1, T),
    topic(A2, T).

% 2. S can be earlier than Q only if Q is third.
%    If S is earlier than Q, then Q must be at position 3.
%    Forbidden: S earlier than Q and Q not at position 3.
violates_s_q_condition(Order) :-
    order(Order, s, Ps),
    order(Order, q, Pq),
    Ps < Pq,
    Pq != 3.

% 3. S must be earlier than Y.
violates_s_y_condition(Order) :-
    order(Order, s, Ps),
    order(Order, y, Py),
    Ps >= Py.

% 4. J must be earlier than G, and G must be earlier than R.
%    We break into two separate violations for safety.
violates_j_g_r_condition(Order) :-
    order(Order, j, Pj),
    order(Order, g, Pg),
    order(Order, r, Pr),
    Pj >= Pg.

violates_j_g_r_condition(Order) :-
    order(Order, j, Pj),
    order(Order, g, Pg),
    order(Order, r, Pr),
    Pg >= Pr.

% Holds predicate: an order is acceptable if it violates none of the conditions.
holds(Order) :-
    order(Order, _, _),
    not violates_consecutive_same_topic(Order),
    not violates_s_q_condition(Order),
    not violates_s_y_condition(Order),
    not violates_j_g_r_condition(Order).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- holds(a).
option(b) :- holds(b).
option(c) :- holds(c).
option(d) :- holds(d).
option(e) :- holds(e).

#show option/1.