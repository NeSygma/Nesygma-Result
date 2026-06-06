% ==================
% Domain: Users
% ==================
user(user1). user(user2). user(user3). user(user4).
user(user5). user(user6). user(user7). user(user8).

% User Properties (weights scaled by 10)
influence_weight(user1, 8).
influence_weight(user2, 3).
influence_weight(user3, 5).
influence_weight(user4, 9).
influence_weight(user5, 4).
influence_weight(user6, 6).
influence_weight(user7, 7).
influence_weight(user8, 2).

cost(user1, 100).
cost(user2, 50).
cost(user3, 80).
cost(user4, 150).
cost(user5, 60).
cost(user6, 90).
cost(user7, 120).
cost(user8, 40).

category(user1, "influencer").
category(user2, "regular").
category(user3, "regular").
category(user4, "influencer").
category(user5, "regular").
category(user6, "regular").
category(user7, "influencer").
category(user8, "regular").

% Directed edges with strength (scaled by 10)
edge(user1, user2, 6).
edge(user1, user3, 7).
edge(user2, user3, 4).
edge(user2, user5, 5).
edge(user3, user4, 3).
edge(user4, user5, 8).
edge(user4, user6, 6).
edge(user5, user7, 5).
edge(user6, user7, 7).
edge(user7, user8, 4).

% ==================
% Decision: Select up to 2 seeds
% ==================
{ seed(U) : user(U) } 2.

% Budget constraint: total cost must not exceed 300
total_budget_used(B) :- B = #sum{ C,U : seed(U), cost(U,C) }.
:- total_budget_used(B), B > 300.

% ==================
% Propagation: Threshold Model
% ==================

% Direct influence: user is directly influenced if connected FROM a seed with strength >= 3 (0.3)
direct(U) :- user(U), not seed(U), seed(S), edge(S, U, W), W >= 3.

% Secondary influence: user is secondary influenced if connected FROM a directly influenced
% user with strength >= 2 (0.2), and not already a seed or directly influenced
secondary(U) :- user(U), not seed(U), not direct(U), direct(D), edge(D, U, W), W >= 2.

% Reached users (seeds + direct + secondary)
reached(U) :- seed(U).
reached(U) :- direct(U).
reached(U) :- secondary(U).

% ==================
% Metrics Computation
% ==================

% Total reach count
total_reach(N) :- N = #count{ U : reached(U) }.

% --- Per-seed expected reach (independent cascade for each seed) ---
% Direct influence from a specific seed S
direct_from(S, U) :- seed(S), user(U), U != S, edge(S, U, W), W >= 3.

% Secondary influence from direct influence of seed S
secondary_from(S, U) :- seed(S), user(U), U != S, not direct_from(S, U),
                         direct_from(S, D), edge(D, U, W), W >= 2.

% Users reached from seed S (independent cascade)
reached_from(S, S) :- seed(S).
reached_from(S, U) :- direct_from(S, U).
reached_from(S, U) :- secondary_from(S, U).

% Expected reach per seed
expected_reach(S, N) :- seed(S), N = #count{ U : reached_from(S, U) }.

% --- Cascade depth ---
has_direct :- direct(U).
has_secondary :- secondary(U).
cascade_depth(1) :- not has_direct.
cascade_depth(2) :- has_direct, not has_secondary.
cascade_depth(3) :- has_secondary.

% --- Coverage ratio: total_reach / total_users (scaled by 1000 for integer) ---
total_users(8).
coverage_ratio(R) :- total_reach(N), total_users(T), T > 0, R = N * 1000 / T.

% --- Efficiency score: total_reach / total_budget_used (scaled by 10000 for integer) ---
efficiency_score(E) :- total_reach(N), total_budget_used(B), B > 0, E = N * 10000 / B.

% --- Influence probability: average influence weight of reached users (scaled by 10) ---
influence_weight_sum(S) :- S = #sum{ W,U : reached(U), influence_weight(U, W) }.
influence_probability(P) :- influence_weight_sum(S), total_reach(N), N > 0, P = S / N.

% ==================
% Optimization: Maximize total reach
% ==================
#maximize { 1,U : reached(U) }.

% ==================
% Output
% ==================
#show seed/1.
#show direct/1.
#show secondary/1.
#show reached/1.
#show total_reach/1.
#show total_budget_used/1.
#show expected_reach/2.
#show cascade_depth/1.
#show coverage_ratio/1.
#show efficiency_score/1.
#show influence_probability/1.