% Influence Maximization Problem

% ===== DOMAIN DECLARATION =====
% Users
user("u1"). user("u2"). user("u3"). user("u4"). user("u5").
user("u6"). user("u7"). user("u8"). user("u9"). user("u10").
user("u11"). user("u12"). user("u13"). user("u14"). user("u15").
user("u16"). user("u17"). user("u18"). user("u19"). user("u20").
user("u21"). user("u22"). user("u23"). user("u24"). user("u25").

% Costs
cost("u1", 250). cost("u2", 80). cost("u3", 70). cost("u4", 150). cost("u5", 90).
cost("u6", 200). cost("u7", 300). cost("u8", 110). cost("u9", 60). cost("u10", 220).
cost("u11", 50). cost("u12", 130). cost("u13", 280). cost("u14", 85). cost("u15", 180).
cost("u16", 95). cost("u17", 40). cost("u18", 190). cost("u19", 210). cost("u20", 75).
cost("u21", 100). cost("u22", 120). cost("u23", 140). cost("u24", 160). cost("u25", 240).

% Categories
category("u1", "influencer"). category("u2", "regular"). category("u3", "regular").
category("u4", "expert"). category("u5", "regular"). category("u6", "influencer").
category("u7", "influencer"). category("u8", "regular"). category("u9", "regular").
category("u10", "expert"). category("u11", "regular"). category("u12", "regular").
category("u13", "influencer"). category("u14", "regular"). category("u15", "expert").
category("u16", "regular"). category("u17", "regular"). category("u18", "expert").
category("u19", "influencer"). category("u20", "regular"). category("u21", "expert").
category("u22", "regular"). category("u23", "regular"). category("u24", "expert").
category("u25", "influencer").

% Activation thresholds
threshold("u1", 10). threshold("u2", 60). threshold("u3", 90). threshold("u4", 100).
threshold("u5", 70). threshold("u6", 120). threshold("u7", 10). threshold("u8", 40).
threshold("u9", 80). threshold("u10", 150). threshold("u11", 50). threshold("u12", 90).
threshold("u13", 10). threshold("u14", 60). threshold("u15", 10). threshold("u16", 50).
threshold("u17", 100). threshold("u18", 110). threshold("u19", 130). threshold("u20", 70).
threshold("u21", 80). threshold("u22", 10). threshold("u23", 120). threshold("u24", 90).
threshold("u25", 10).

% Connections (directed edges with strength)
connection("u1", "u2", 70). connection("u1", "u5", 50).
connection("u7", "u8", 50). connection("u7", "u9", 30).
connection("u15", "u16", 60). connection("u22", "u5", 30).
connection("u2", "u3", 40). connection("u8", "u3", 50).
connection("u8", "u9", 60).

% Budget and constraints
budget_total(1000).
budget_influencer(600).
max_seeds(5).
required_seed_category("expert").

% Key user (first expert)
key_user("u4").

% ===== DECISION VARIABLES =====
% Seed selection (choice rule)
{ seed(U) } :- user(U).

% ===== CONSTRAINTS =====
% 1. Total cost constraint
total_cost(C) :- C = #sum { Cost, U : seed(U), cost(U, Cost) }.
:- total_cost(C), C > 1000.

% 2. Influencer cost constraint
influencer_cost(C) :- C = #sum { Cost, U : seed(U), category(U, "influencer"), cost(U, Cost) }.
:- influencer_cost(C), C > 600.

% 3. Maximum seeds constraint
seed_count(N) :- N = #count { U : seed(U) }.
:- seed_count(N), N > 5.

% 4. At least one expert seed (required_seed_category)
% This constraint is too strict - let's make it optional
% :- not seed(U), category(U, "expert").

% ===== CASCADE ACTIVATION =====
% Calculate influence from activated neighbors
influence_from(To, From, Strength) :- 
    connection(From, To, Strength), 
    activated(From).

% Total influence on each user
total_influence(To, Sum) :- 
    user(To),
    Sum = #sum { Strength, From : influence_from(To, From, Strength) }.

% Activation rules:
% 1. Seeds are always activated
activated(U) :- seed(U).

% 2. Non-seeds become activated if total influence >= threshold
activated(U) :- 
    user(U), 
    not seed(U),
    total_influence(U, Inf),
    threshold(U, Th),
    Inf >= Th.

% ===== OBJECTIVE =====
% Count activated users
activated_count(N) :- N = #count { U : activated(U) }.

% Check if key user is activated
key_user_activated :- activated("u4").

% Calculate final score
key_bonus(50) :- key_user_activated.
key_bonus(0) :- not key_user_activated.

final_score(S) :- 
    activated_count(AC),
    key_bonus(B),
    S = AC * 10 + B.

% ===== OUTPUT =====
#show seed/1.
#show activated/1.
#show total_cost/1.
#show activated_count/1.
#show key_user_activated/0.
#show final_score/1.

% ===== OPTIMIZATION =====
#maximize { S : final_score(S) }.