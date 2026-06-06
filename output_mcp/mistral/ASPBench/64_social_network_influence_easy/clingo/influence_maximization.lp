%% Define the domain of users
user(user1). user(user2). user(user3). user(user4). user(user5). user(user6). user(user7). user(user8).

% User properties (using integers for simplicity)
influence_weight(user1, 8). cost(user1, 100). category(user1, influencer).
influence_weight(user2, 3). cost(user2, 50). category(user2, regular).
influence_weight(user3, 5). cost(user3, 80). category(user3, regular).
influence_weight(user4, 9). cost(user4, 150). category(user4, influencer).
influence_weight(user5, 4). cost(user5, 60). category(user5, regular).
influence_weight(user6, 6). cost(user6, 90). category(user6, regular).
influence_weight(user7, 7). cost(user7, 120). category(user7, influencer).
influence_weight(user8, 2). cost(user8, 40). category(user8, regular).

% Directed edges with strength (scaled by 10 for simplicity)
edge(user1, user2, 6). edge(user1, user3, 7).
edge(user2, user3, 4). edge(user2, user5, 5).
edge(user3, user4, 3). edge(user4, user5, 8).
edge(user4, user6, 6). edge(user5, user7, 5).
edge(user6, user7, 7). edge(user7, user8, 4).

% Budget and max seeds constraints
max_seeds(2).
budget_limit(300).

% Select up to max_seeds users as seeds, respecting budget
1 { selected_seed(U) : user(U) } max_seeds.

% Budget constraint for single seed
:- selected_seed(U), cost(U, C), C > budget_limit(B).

% Budget constraint for two seeds
:- selected_seed(U1), selected_seed(U2), U1 != U2, cost(U1, C1), cost(U2, C2), C1 + C2 > budget_limit(B).

% Direct influence: strength >= 3 (0.3 in original scale) from a seed
{ directly_influenced(U) : user(U) } :- selected_seed(S), edge(S, U, Strength), Strength >= 3.

% Secondary influence: strength >= 2 (0.2 in original scale) from a directly influenced user, not already a seed or directly influenced
{ secondary_influenced(U) : user(U) } :-
    directly_influenced(D),
    edge(D, U, Strength),
    Strength >= 2,
    not selected_seed(U),
    not directly_influenced(U).

% Calculate total budget used
total_budget_used(B) :- B = #sum { C : selected_seed(U), cost(U, C) }.

% Calculate total reach: seeds + directly influenced + secondary influenced
total_reach(R) :- R = #sum { 1 : selected_seed(_) } + #sum { 1 : directly_influenced(_) } + #sum { 1 : secondary_influenced(_) }.

% Coverage ratio: total_reach / total_users (8 users)
coverage_ratio(Ratio) :- total_reach(R), total_users(T), T = 8, Ratio = R / T.

% Efficiency score: total_reach / total_budget_used
efficiency_score(Score) :- total_reach(R), total_budget_used(B), B > 0, Score = R / B.

% Cascade depth: maximum depth of influence (1-3)
cascade_depth(1) :- selected_seed(_).
cascade_depth(2) :- directly_influenced(_).
cascade_depth(3) :- secondary_influenced(_).

% Ensure cascade_depth is at least 1 and at most 3
:- cascade_depth(D), D < 1.
:- cascade_depth(D), D > 3.

% Objective: maximize total reach
#maximize { R : total_reach(R) }.

% Show the relevant outputs
#show selected_seed/1.
#show directly_influenced/1.
#show secondary_influenced/1.
#show total_budget_used/1.
#show total_reach/1.
#show coverage_ratio/1.
#show efficiency_score/1.
#show cascade_depth/1.