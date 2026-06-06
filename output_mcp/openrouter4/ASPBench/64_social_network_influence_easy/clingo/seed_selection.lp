% ---- DATA (scaled to integers: multiply weights/strengths by 10) ----
% Users
user(1..8).

% user_info(id, weight*10, cost, category)
user_info(1, 8, 100, "influencer").
user_info(2, 3, 50,  "regular").
user_info(3, 5, 80,  "regular").
user_info(4, 9, 150, "influencer").
user_info(5, 4, 60,  "regular").
user_info(6, 6, 90,  "regular").
user_info(7, 7, 120, "influencer").
user_info(8, 2, 40,  "regular").

% directed edge(from, to, strength*10)
edge(1,2,6).
edge(1,3,7).
edge(2,3,4).
edge(2,5,5).
edge(3,4,3).
edge(4,5,8).
edge(4,6,6).
edge(5,7,5).
edge(6,7,7).
edge(7,8,4).

% Constants (thresholds scaled by 10)
direct_threshold(3).   % 0.3
secondary_threshold(2). % 0.2
budget_max(300).
max_seeds_allowed(2).
max_cascade_depth(3).

% ---- CHOICE: Select seeds ----
{ seed(U) } :- user(U).

% At most 2 seeds
:- #count { U : seed(U) } > M, max_seeds_allowed(M).

% Budget constraint
:- #sum { C, U : seed(U), user_info(U, _, C, _) } > B, budget_max(B).

% ---- INFLUENCE CASCADE ----
% Depth 0: seeds
reached(U, 0) :- seed(U).

% Depth 1: directly from seeds (strength >= 0.3, i.e., scaled >= 3)
reached(V, 1) :- seed(U), edge(U, V, S), S >= 3, user(V), not reached(V, 0).

% Depth D+1: from users reached at depth D (D >= 1), strength >= 0.2 (scaled >= 2)
reached(V, D+1) :- reached(U, D), edge(U, V, S), S >= 2, 
                   user(V), not reached(V, _), D >= 1, D <= 2.

% No duplicate depths
:- reached(U, D1), reached(U, D2), D1 != D2.

% ---- DERIVED PREDICATES ----
% Any reached user
reached_any(U) :- reached(U, _).

% Directly influenced: depth = 1
directly_influenced(U) :- reached(U, 1).

% Secondary influenced: depth >= 2
secondary_influenced(U) :- reached(U, D), D >= 2.

% ---- COMPUTATIONS ----
total_cost(C) :- C = #sum { Cst, U : seed(U), user_info(U, _, Cst, _) }.

total_reach(R) :- R = #count { U : reached_any(U) }.

total_users(8).

coverage_ratio(R) :- total_reach(Rch), total_users(T), R = Rch / T.

efficiency_score(S) :- total_reach(Rch), total_cost(C), C > 0, S = Rch / C.

% Cascade depth: maximum D among reached
cascade_depth(Dep) :- Dep = #max { D : reached(_, D) }.

% Direct / secondary counts
direct_count(N) :- N = #count { U : directly_influenced(U) }.
secondary_count(N) :- N = #count { U : secondary_influenced(U) }.

% ---- OPTIMIZATION ----
#maximize { 1, U : reached_any(U) }.

% ---- OUTPUT ----
#show seed/1.
#show directly_influenced/1.
#show secondary_influenced/1.
#show total_reach/1.
#show total_cost/1.
#show cascade_depth/1.
#show coverage_ratio/1.
#show efficiency_score/1.
#show direct_count/1.
#show secondary_count/1.