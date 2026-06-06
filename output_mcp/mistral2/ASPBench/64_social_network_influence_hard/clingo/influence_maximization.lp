% --- Facts ---
% Users: user(id, cost, category, activation_threshold)
user("u1", 250, "influencer", 10).
user("u2", 80, "regular", 60).
user("u3", 70, "regular", 90).
user("u4", 150, "expert", 100).
user("u5", 90, "regular", 70).
user("u6", 200, "influencer", 120).
user("u7", 300, "influencer", 10).
user("u8", 110, "regular", 40).
user("u9", 60, "regular", 80).
user("u10", 220, "expert", 150).
user("u11", 50, "regular", 50).
user("u12", 130, "regular", 90).
user("u13", 280, "influencer", 10).
user("u14", 85, "regular", 60).
user("u15", 180, "expert", 10).
user("u16", 95, "regular", 50).
user("u17", 40, "regular", 100).
user("u18", 190, "expert", 110).
user("u19", 210, "influencer", 130).
user("u20", 75, "regular", 70).
user("u21", 100, "expert", 80).
user("u22", 120, "regular", 10).
user("u23", 140, "regular", 120).
user("u24", 160, "expert", 90).
user("u25", 240, "influencer", 10).

% Connections: connection(from, to, strength)
connection("u1", "u2", 70).
connection("u1", "u5", 50).
connection("u7", "u8", 50).
connection("u7", "u9", 30).
connection("u15", "u16", 60).
connection("u22", "u5", 30).
connection("u2", "u3", 40).
connection("u8", "u3", 50).
connection("u8", "u9", 60).

% Budget and constraints
budget(1000, 600).
max_seeds(5).
key_user("u4").

% --- Derived predicates ---
influencer(U) :- user(U, _, "influencer", _).
expert(U) :- user(U, _, "expert", _).
regular(U) :- user(U, _, "regular", _).

% --- Selection ---
{ selected(U) : user(U, _, _, _) } <= MaxSeeds :- max_seeds(MaxSeeds).

% Budget constraints
total_cost(C) :- C = #sum { Cost : selected(U), user(U, Cost, _, _) }.
:- total_cost(C), budget(TotalBudget, _), C > TotalBudget.

total_influencer_cost(C) :- C = #sum { Cost : selected(U), user(U, Cost, Cat, _), influencer(U) }.
:- total_influencer_cost(C), budget(_, InfluencerBudget), C > InfluencerBudget.

% Expert seed constraint
expert_seed_selected :- selected(U), expert(U).
:- not expert_seed_selected.

% --- Activation ---
% Time steps for cascade
time(0..MaxTime) :- max_seeds(MaxSeeds), MaxTime = MaxSeeds + 1.

% Seeds are activated at time 0
activated(U, 0) :- selected(U).

% For non-seeds, compute influence sum from activated neighbors
influence_sum(U, T) :-
    time(T),
    user(U, _, _, Threshold),
    not selected(U),
    T > 0,
    Sum = #sum { Strength : connection(V, U, Strength), activated(V, T-1) },
    Sum >= Threshold.

% Activation at time T if influence sum meets threshold
activated(U, T) :-
    time(T),
    user(U, _, _, Threshold),
    not selected(U),
    T > 0,
    Sum = #sum { Strength : connection(V, U, Strength), activated(V, T-1) },
    Sum >= Threshold.

% Ensure activation persists
activated(U, T) :- activated(U, T-1), time(T).

% Key user activation
key_user_activated :- activated("u4", _).

% Total activated users
total_activated(N) :- N = #count { U : activated(U, _) }.

% --- Scoring ---
base_score(N) :- total_activated(N).
bonus_score(50) :- key_user_activated.
bonus_score(0) :- not key_user_activated.
score(S) :- base_score(N), bonus_score(B), S = 10 * N + B.

% --- Show directives ---
#show selected/1.
#show activated/1.
#show total_cost/1.
#show total_activated/1.
#show key_user_activated/0.
#show score/1.
#maximize { S : score(S) }.