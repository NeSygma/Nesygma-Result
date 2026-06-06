% Social Network Influence Maximization

% Domain: users
user(1..8).

% Costs
cost(1, 100).
cost(2, 50).
cost(3, 80).
cost(4, 150).
cost(5, 60).
cost(6, 90).
cost(7, 120).
cost(8, 40).

% Directed edges with strength (multiplied by 10 to avoid decimals)
edge(1, 2, 6).
edge(1, 3, 7).
edge(2, 3, 4).
edge(2, 5, 5).
edge(3, 4, 3).
edge(4, 5, 8).
edge(4, 6, 6).
edge(5, 7, 5).
edge(6, 7, 7).
edge(7, 8, 4).

% Thresholds (multiplied by 10)
threshold_direct(3).   % 0.3 * 10
threshold_secondary(2). % 0.2 * 10

% Seed selection: at most 2 seeds
{ seed(U) : user(U) } 2.

% Total cost of selected seeds
total_cost(C) :- C = #sum{ Cost, U : seed(U), cost(U, Cost) }.

% Budget constraint
:- total_cost(C), C > 300.

% Direct influence: a user is directly influenced if connected from a seed with strength >= threshold_direct
direct_influence(U) :- seed(S), edge(S, U, Strength), Strength >= 3, user(U).

% Secondary influence: a user is secondary influenced if connected from a directly influenced user with strength >= threshold_secondary,
% and not already a seed or directly influenced
secondary_influence(U) :- not seed(U), not direct_influence(U),
    direct_influence(D), edge(D, U, Strength), Strength >= 2, user(U).

% Influenced users: seeds, directly influenced, or secondary influenced
influenced(U) :- seed(U).
influenced(U) :- direct_influence(U).
influenced(U) :- secondary_influence(U).

% Total reach (number of influenced users)
total_reach(N) :- N = #count{ U : influenced(U) }.

% Per-seed reach (independent cascade)
% Direct influence from seed S
direct_from_S(S, U) :- seed(S), edge(S, U, Strength), Strength >= 3, user(U).
% Secondary influence from seed S
secondary_from_S(S, U) :- seed(S), direct_from_S(S, D), edge(D, U, Strength), Strength >= 2, user(U),
    not direct_from_S(S, U), U != S.
% Reach from seed S
reach_from_S(S, S) :- seed(S).
reach_from_S(S, U) :- direct_from_S(S, U).
reach_from_S(S, U) :- secondary_from_S(S, U).

% Expected reach for each seed
expected_reach(S, N) :- seed(S), N = #count{ U : reach_from_S(S, U) }.

% Output: selected seeds with cost and expected reach
selected_seed(U, Cost, Reach) :- seed(U), cost(U, Cost), expected_reach(U, Reach).

% Cascade analysis
total_budget_used(C) :- total_cost(C).
direct_influence_list(U) :- direct_influence(U).
secondary_influence_list(U) :- secondary_influence(U).
influence_probability(1).

% Network metrics
coverage_ratio(R) :- total_reach(N), R = N / 8.
efficiency_score(S) :- total_reach(N), total_budget_used(C), S = N / C.
cascade_depth(2). % seeds (depth 0), direct (depth 1), secondary (depth 2)

% Maximize total reach
#maximize{ N : total_reach(N) }.

% Show only output predicates
#show selected_seed/3.
#show total_budget_used/1.
#show direct_influence_list/1.
#show secondary_influence_list/1.
#show total_reach/1.
#show influence_probability/1.
#show coverage_ratio/1.
#show efficiency_score/1.
#show cascade_depth/1.