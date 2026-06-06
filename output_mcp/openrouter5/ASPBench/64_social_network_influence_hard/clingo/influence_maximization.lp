%%% Influence Maximization Problem %%%

%%% DOMAIN DEFINITIONS %%%

% Users
user("u1"). user("u2"). user("u3"). user("u4"). user("u5").
user("u6"). user("u7"). user("u8"). user("u9"). user("u10").
user("u11"). user("u12"). user("u13"). user("u14"). user("u15").
user("u16"). user("u17"). user("u18"). user("u19"). user("u20").
user("u21"). user("u22"). user("u23"). user("u24"). user("u25").

% User costs
cost("u1", 250). cost("u2", 80). cost("u3", 70). cost("u4", 150).
cost("u5", 90). cost("u6", 200). cost("u7", 300). cost("u8", 110).
cost("u9", 60). cost("u10", 220). cost("u11", 50). cost("u12", 130).
cost("u13", 280). cost("u14", 85). cost("u15", 180). cost("u16", 95).
cost("u17", 40). cost("u18", 190). cost("u19", 210). cost("u20", 75).
cost("u21", 100). cost("u22", 120). cost("u23", 140). cost("u24", 160).
cost("u25", 240).

% User categories
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

% Connections (directed edges with influence strength)
edge("u1","u2",70). edge("u1","u5",50). edge("u7","u8",50).
edge("u7","u9",30). edge("u15","u16",60). edge("u22","u5",30).
edge("u2","u3",40). edge("u8","u3",50). edge("u8","u9",60).

% Budget constraints
budget_total(1000).
budget_influencer(600).
max_seeds(5).

% Key user
key_user("u4").

%%% CHOICE: Select seeds %%%

% Select at most max_seeds users as seeds
{ seed(U) : user(U) } <= N :- max_seeds(N).

% Constraint: total cost of seeds <= total budget
total_seed_cost(C) :- C = #sum { Cost,U : seed(U), cost(U,Cost) }.
:- total_seed_cost(C), budget_total(B), C > B.

% Constraint: total cost of influencer seeds <= influencer budget
total_influencer_cost(C) :- C = #sum { Cost,U : seed(U), cost(U,Cost), category(U,"influencer") }.
:- total_influencer_cost(C), budget_influencer(B), C > B.

% Required seed category: at least one expert must be selected as seed
expert_seed :- seed(U), category(U, "expert").
:- not expert_seed.

%%% CASCADE ACTIVATION MODELING %%%

% Time horizon: at most number of users steps for cascade
time(0..25).

% Step 0: seeds are activated
activated(U, 0) :- seed(U).

% Activation at step T+1: a user becomes activated if sum of incoming influence
% from neighbors activated at step T (or earlier) meets threshold
% Frame: once activated, stays activated
activated(U, T+1) :- activated(U, T), time(T), time(T+1).

% New activation: sum of influence from already-activated neighbors >= threshold
activated(U, T+1) :- 
    user(U),
    time(T), time(T+1),
    threshold(U, Thresh),
    #sum { S, V : edge(V, U, S), activated(V, T) } >= Thresh,
    not activated(U, T).

% A user is ultimately activated if activated at any time step
ultimately_activated(U) :- activated(U, T), time(T).

%%% OBJECTIVE %%%

% Score: 10 points per activated user
activated_count(N) :- N = #count { U : ultimately_activated(U) }.

% Bonus: 50 points if key user (u4) is activated
key_activated :- ultimately_activated("u4").

% Total score
score(S) :- 
    activated_count(N),
    key_activated,
    S = N * 10 + 50.
score(S) :- 
    activated_count(N),
    not key_activated,
    S = N * 10.

% Maximize score
#maximize { S@1 : score(S) }.

%%% OUTPUT %%%

% Show selected seeds
#show seed/1.
% Show ultimately activated users
#show ultimately_activated/1.
% Show total cost
#show total_seed_cost/1.
% Show total influencer cost
#show total_influencer_cost/1.
% Show activated count
#show activated_count/1.
% Show key activated status
#show key_activated/0.
% Show score
#show score/1.