% --- Data ---
user(user1; user2; user3; user4; user5; user6; user7; user8).

cost(user1, 100). cost(user2, 50). cost(user3, 80). cost(user4, 150).
cost(user5, 60). cost(user6, 90). cost(user7, 120). cost(user8, 40).

% Strengths multiplied by 10 to use integers
edge(user1, user2, 6). edge(user1, user3, 7).
edge(user2, user3, 4). edge(user2, user5, 5).
edge(user3, user4, 3).
edge(user4, user5, 8). edge(user4, user6, 6).
edge(user5, user7, 5).
edge(user6, user7, 7).
edge(user7, user8, 4).

% --- Constraints ---
% Select up to 2 seeds
{ seed(U) : user(U) } 2.

% Budget limit 300
:- #sum { C, U : seed(U), cost(U, C) } > 300.

% --- Influence Logic ---
% Directly influenced: connected from a seed with strength >= 3 (0.3 * 10)
directly_influenced(V) :- seed(U), edge(U, V, S), S >= 3, not seed(V).

% Secondary influenced: connected from a directly influenced user with strength >= 2 (0.2 * 10)
% (not already a seed or directly influenced)
secondary_influenced(W) :- directly_influenced(V), edge(V, W, S), S >= 2, not seed(W), not directly_influenced(W).

% Total reach
reached(U) :- seed(U).
reached(U) :- directly_influenced(U).
reached(U) :- secondary_influenced(U).

total_reach(N) :- N = #count { U : reached(U) }.

% --- Objective ---
#maximize { N : total_reach(N) }.

% --- Output ---
#show seed/1.
#show directly_influenced/1.
#show secondary_influenced/1.
#show total_reach/1.
#show total_budget_used/1.

total_budget_used(C) :- C = #sum { Cost, U : seed(U), cost(U, Cost) }.