% ===== DOMAINS =====
user(u1). user(u2). user(u3). user(u4). user(u5).
user(u6). user(u7). user(u8). user(u9). user(u10).
user(u11). user(u12). user(u13). user(u14). user(u15).
user(u16). user(u17). user(u18). user(u19). user(u20).
user(u21). user(u22). user(u23). user(u24). user(u25).

% ===== USER PROPERTIES =====
cost(u1, 250). cost(u2, 80). cost(u3, 70). cost(u4, 150). cost(u5, 90).
cost(u6, 200). cost(u7, 300). cost(u8, 110). cost(u9, 60). cost(u10, 220).
cost(u11, 50). cost(u12, 130). cost(u13, 280). cost(u14, 85). cost(u15, 180).
cost(u16, 95). cost(u17, 40). cost(u18, 190). cost(u19, 210). cost(u20, 75).
cost(u21, 100). cost(u22, 120). cost(u23, 140). cost(u24, 160). cost(u25, 240).

category(u1, influencer). category(u2, regular). category(u3, regular). category(u4, expert).
category(u5, regular). category(u6, influencer). category(u7, influencer). category(u8, regular).
category(u9, regular). category(u10, expert). category(u11, regular). category(u12, regular).
category(u13, influencer). category(u14, regular). category(u15, expert). category(u16, regular).
category(u17, regular). category(u18, expert). category(u19, influencer). category(u20, regular).
category(u21, expert). category(u22, regular). category(u23, regular). category(u24, expert).
category(u25, influencer).

threshold(u1, 10). threshold(u2, 60). threshold(u3, 90). threshold(u4, 100).
threshold(u5, 70). threshold(u6, 120). threshold(u7, 10). threshold(u8, 40).
threshold(u9, 80). threshold(u10, 150). threshold(u11, 50). threshold(u12, 90).
threshold(u13, 10). threshold(u14, 60). threshold(u15, 10). threshold(u16, 50).
threshold(u17, 100). threshold(u18, 110). threshold(u19, 130). threshold(u20, 70).
threshold(u21, 80). threshold(u22, 10). threshold(u23, 120). threshold(u24, 90).
threshold(u25, 10).

% ===== CONNECTIONS (directed: from -> to with strength) =====
conn(u1, u2, 70). conn(u1, u5, 50). conn(u7, u8, 50). conn(u7, u9, 30).
conn(u15, u16, 60). conn(u22, u5, 30). conn(u2, u3, 40). conn(u8, u3, 50).
conn(u8, u9, 60).

% ===== PARAMETERS =====
budget_total(1000).
budget_influencer(600).
max_seeds_limit(5).
key_user(u4).

% ===== TIME HORIZON FOR CASCADE =====
time(0..10).

% ===== DECISION: SELECT SEEDS (choice rule) =====
{ seed(U) } :- user(U).

% ===== HARD CONSTRAINTS =====

% At most 5 seeds
:- #count{U : seed(U)} > 5.

% Total cost of seeds must not exceed total budget
total_cost(S) :- S = #sum{C, U : seed(U), cost(U, C)}.
:- total_cost(S), budget_total(B), S > B.

% Total cost of influencer seeds must not exceed influencer budget
influencer_cost(S) :- S = #sum{C, U : seed(U), cost(U, C), category(U, influencer)}.
:- influencer_cost(S), budget_influencer(B), S > B.

% At least one seed must be from the "expert" category
has_expert_seed :- seed(U), category(U, expert).
:- not has_expert_seed.

% ===== CASCADE ACTIVATION MODEL =====

% Step 1: Seeds are activated at time 0
activated(U, 0) :- seed(U).

% Step 2: Persistence - once activated, stays activated at all future steps
activated(U, T) :- activated(U, T-1), time(T), T > 0.

% Step 3: Compute total incoming influence at each time step
% For each user U at time T, sum strengths from all neighbors activated at T-1
% Using tuple (S, V) to avoid deduplication of equal strengths from different neighbors
total_influence(U, T, N) :- N = #sum{S, V : conn(V, U, S), activated(V, T-1)}, user(U), time(T), T > 0.

% Step 4: A non-seed user becomes activated if incoming influence >= threshold
activated(U, T) :- total_influence(U, T, N), threshold(U, Thr), N >= Thr, time(T), T > 0.

% Derive final activation status (activated at any time step)
is_activated(U) :- activated(U, T), time(T).

% ===== SCORING =====

% Count total activated users
activated_count(N) :- N = #count{U : is_activated(U)}.

% Check if key user (u4) is activated
key_activated :- is_activated(u4).

% Compute composite score:
%   10 points per activated user + 50 bonus if key user is activated
score(S) :- activated_count(N), key_activated, S = N * 10 + 50.
score(S) :- activated_count(N), not key_activated, S = N * 10.

% ===== OPTIMIZATION: Maximize the composite score =====
#maximize{S : score(S)}.

% ===== OUTPUT =====
#show seed/1.
#show is_activated/1.
#show total_cost/1.
#show activated_count/1.
#show key_activated/0.
#show score/1.