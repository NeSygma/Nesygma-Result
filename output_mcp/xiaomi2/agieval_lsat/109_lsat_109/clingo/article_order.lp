% Articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).
topic(finance). topic(nutrition). topic(wildlife).

topic_of(g, finance). topic_of(h, finance). topic_of(j, finance).
topic_of(q, nutrition). topic_of(r, nutrition). topic_of(s, nutrition).
topic_of(y, wildlife).

% Define each answer choice's ordering
% Option A: H, S, J, Q, Y, G, R
at_a(h,1). at_a(s,2). at_a(j,3). at_a(q,4). at_a(y,5). at_a(g,6). at_a(r,7).

% Option B: J, Q, G, H, S, Y, R
at_b(j,1). at_b(q,2). at_b(g,3). at_b(h,4). at_b(s,5). at_b(y,6). at_b(r,7).

% Option C: Q, J, S, H, Y, G, R
at_c(q,1). at_c(j,2). at_c(s,3). at_c(h,4). at_c(y,5). at_c(g,6). at_c(r,7).

% Option D: Q, J, Y, S, G, R, H
at_d(q,1). at_d(j,2). at_d(y,3). at_d(s,4). at_d(g,5). at_d(r,6). at_d(h,7).

% Option E: S, G, Q, J, Y, R, H
at_e(s,1). at_e(g,2). at_e(q,3). at_e(j,4). at_e(y,5). at_e(r,6). at_e(h,7).

% Select exactly one option to evaluate
option_id(a; b; c; d; e).
1 { check(O) : option_id(O) } 1.

% Use the selected option's ordering
at(A, P) :- check(a), at_a(A, P).
at(A, P) :- check(b), at_b(A, P).
at(A, P) :- check(c), at_c(A, P).
at(A, P) :- check(d), at_d(A, P).
at(A, P) :- check(e), at_e(A, P).

% Condition 1: Consecutive articles cannot cover the same topic
:- at(A1, P), at(A2, P2), P2 = P+1, topic_of(A1, T), topic_of(A2, T).

% Condition 2: S can be earlier than Q only if Q is third
% If S < Q then Q must be 3
:- at(s, Ps), at(q, Pq), Ps < Pq, Pq != 3.

% Condition 3: S must be earlier than Y
:- at(s, Ps), at(y, Py), Ps >= Py.

% Condition 4: J must be earlier than G, and G must be earlier than R
:- at(j, Pj), at(g, Pg), Pj >= Pg.
:- at(g, Pg), at(r, Pr), Pg >= Pr.

% Map the correct answer to option/1
option(a) :- check(a).
option(b) :- check(b).
option(c) :- check(c).
option(d) :- check(d).
option(e) :- check(e).

#show option/1.