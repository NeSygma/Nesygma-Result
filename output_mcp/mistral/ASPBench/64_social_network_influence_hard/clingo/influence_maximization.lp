% Define users
user("u1", 250, "influencer", 10).
user("u2", 80, "regular", 60).
user("u3", 70, "regular", 90).
user("u4", 150, "expert", 100).  % key user
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

% Define connections
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
budget(total, 1000).
budget(influencer, 600).
max_seeds(5).
required_category("expert").

% Helper predicates
user_cost(U, C) :- user(U, C, _, _).
user_category(U, Cat) :- user(U, _, Cat, _).
user_threshold(U, T) :- user(U, _, _, T).

category_influencer("influencer").
category_expert("expert").

% Select seeds with constraints
% At most max_seeds seeds
{ selected(U) : user(U, _, _, _) } <= max_seeds.

% At least one expert seed (required_category is "expert")
:- required_category(Cat), not selected_expert.
selected_expert :- selected(U), user_category(U, Cat), Cat = "expert".

% Influencer cost constraint: sum of costs for influencer seeds <= influencer budget
total_influencer_cost(C) :- C = #sum { Cost : selected(U), user(U, Cost, Cat, _), category_influencer(Cat) }.
:- budget(influencer, B), total_influencer_cost(C), C > B.

% Total cost constraint: sum of all selected seed costs <= total budget
total_cost(C) :- C = #sum { Cost : selected(U), user(U, Cost, _, _) }.
:- budget(total, B), total_cost(C), C > B.

% Cascade activation model
% We use a time-based fixed point computation
time(0..10).  % Sufficient steps for cascade propagation

% Base case: seeds are activated at time 0
activated(U, 0) :- selected(U).

% Recursive case: if not activated at T-1, check if neighbors provide enough influence
activated(U, T) :- time(T), T > 0, not activated(U, T-1),
                   user(U, _, _, Threshold),
                   #sum { S, V : connection(V, U, S), activated(V, T-1) } >= Threshold.

% A user is activated if activated at any time
activated(U) :- activated(U, T), time(T).

% Compute total activated count
activated_count(N) :- N = #count { U : activated(U) }.

% Check if key user (u4) is activated
key_user_activated :- activated("u4").

% Compute final score: 10 points per activated user + 50 if key user activated
final_score(Score) :- activated_count(N), key_user_activated,
                      Score = 10 * N + 50.
final_score(Score) :- activated_count(N), not key_user_activated,
                      Score = 10 * N.

% Maximize the score
#maximize { Score : final_score(Score) }.

% Show the solution
#show selected/1.
#show activated/1.
#show total_cost/1.
#show activated_count/1.
#show key_user_activated/0.
#show final_score/1.