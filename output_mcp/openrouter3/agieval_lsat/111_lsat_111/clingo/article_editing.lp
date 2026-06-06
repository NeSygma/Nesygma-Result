% Articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).
topic(finance). topic(nutrition). topic(wildlife).

% Assign topics to articles
topic(g, finance). topic(h, finance). topic(j, finance).
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition).
topic(y, wildlife).

% Positions 1-7
position(1..7).

% Each article gets exactly one position
1 { position_of(A, P) : position(P) } 1 :- article(A).

% No two articles at same position
:- position_of(A1, P), position_of(A2, P), A1 != A2.

% Consecutive articles cannot have same topic
:- position_of(A1, P), position_of(A2, P+1), topic(A1, T), topic(A2, T).

% S can be earlier than Q only if Q is third
% This means: if S is before Q, then Q must be at position 3
:- position_of(s, Ps), position_of(q, Pq), Ps < Pq, Pq != 3.

% S must be earlier than Y
:- position_of(s, Ps), position_of(y, Py), Ps >= Py.

% J must be earlier than G, and G must be earlier than R
:- position_of(j, Pj), position_of(g, Pg), Pj >= Pg.
:- position_of(g, Pg), position_of(r, Pr), Pg >= Pr.

% Specific condition: G is fourth
position_of(g, 4).

% Answer choices - check if they could be true
% (A) H is fifth
could_be_a :- position_of(h, 5).

% (B) J is first
could_be_b :- position_of(j, 1).

% (C) Q is second
could_be_c :- position_of(q, 2).

% (D) S is fifth
could_be_d :- position_of(s, 5).

% (E) Y is sixth
could_be_e :- position_of(y, 6).

% Map the correct answer to option/1
% We need to find which one could be true (i.e., is consistent with all constraints)
% Since we're looking for "could be true", we need to check which option is possible
% In ASP, if an option is possible, it will appear in some answer set
% We'll use choice rules to allow each option to be true or false, then see which ones are possible

% For each option, we need to check if it's possible given all constraints
% We'll use a different approach: check each option separately
% Actually, let's use the standard approach: derive which options are possible

% Option A: H is fifth
option(a) :- could_be_a.

% Option B: J is first  
option(b) :- could_be_b.

% Option C: Q is second
option(c) :- could_be_c.

% Option D: S is fifth
option(d) :- could_be_d.

% Option E: Y is sixth
option(e) :- could_be_e.

#show option/1.
#show position_of/2.