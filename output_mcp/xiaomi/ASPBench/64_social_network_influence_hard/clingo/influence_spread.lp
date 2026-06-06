% === Domain Facts ===
user(u1). user(u2). user(u3). user(u4). user(u5).
user(u6). user(u7). user(u8). user(u9). user(u10).
user(u11). user(u12). user(u13). user(u14). user(u15).
user(u16). user(u17). user(u18). user(u19). user(u20).
user(u21). user(u22). user(u23). user(u24). user(u25).

cost(u1,250). cost(u2,80). cost(u3,70). cost(u4,150). cost(u5,90).
cost(u6,200). cost(u7,300). cost(u8,110). cost(u9,60). cost(u10,220).
cost(u11,50). cost(u12,130). cost(u13,280). cost(u14,85). cost(u15,180).
cost(u16,95). cost(u17,40). cost(u18,190). cost(u19,210). cost(u20,75).
cost(u21,100). cost(u22,120). cost(u23,140). cost(u24,160). cost(u25,240).

category(u1,influencer). category(u2,regular). category(u3,regular).
category(u4,expert). category(u5,regular). category(u6,influencer).
category(u7,influencer). category(u8,regular). category(u9,regular).
category(u10,expert). category(u11,regular). category(u12,regular).
category(u13,influencer). category(u14,regular). category(u15,expert).
category(u16,regular). category(u17,regular). category(u18,expert).
category(u19,influencer). category(u20,regular). category(u21,expert).
category(u22,regular). category(u23,regular). category(u24,expert).
category(u25,influencer).

threshold(u1,10). threshold(u2,60). threshold(u3,90). threshold(u4,100).
threshold(u5,70). threshold(u6,120). threshold(u7,10). threshold(u8,40).
threshold(u9,80). threshold(u10,150). threshold(u11,50). threshold(u12,90).
threshold(u13,10). threshold(u14,60). threshold(u15,10). threshold(u16,50).
threshold(u17,100). threshold(u18,110). threshold(u19,130). threshold(u20,70).
threshold(u21,80). threshold(u22,10). threshold(u23,120). threshold(u24,90).
threshold(u25,10).

% Connections: connection(from, to, strength)
connection(u1,u2,70). connection(u1,u5,50). connection(u7,u8,50).
connection(u7,u9,30). connection(u15,u16,60). connection(u22,u5,30).
connection(u2,u3,40). connection(u8,u3,50). connection(u8,u9,60).

% Key user
key_user(u4).

% === Seed Selection (Choice) ===
{ seed(U) : user(U) } 5.

% === Budget Constraints ===
% Total cost constraint
total_cost(C) :- C = #sum{ Cost,U : seed(U), cost(U,Cost) }.
:- total_cost(C), C > 1000.

% Influencer budget constraint
influencer_cost(C) :- C = #sum{ Cost,U : seed(U), cost(U,Cost), category(U,influencer) }.
:- influencer_cost(C), C > 600.

% Required seed category: at least one seed must be expert
has_expert_seed :- seed(U), category(U,expert).
:- not has_expert_seed.

% === Cascade Activation ===
% A user is activated if they are a seed
activated(U) :- seed(U).

% Compute influence received from activated neighbors
influence(U, S) :- connection(F, U, S), activated(F).

total_influence(U, T) :- T = #sum{ S : influence(U, S) }, user(U).

% A user becomes activated if total influence >= threshold
activated(U) :- user(U), total_influence(U, T), threshold(U, Th), T >= Th.

% === Objective: Maximize composite score ===
activated_count(N) :- N = #count{ U : activated(U) }.
key_activated :- activated(u4).

score_reach(S) :- activated_count(N), S = N * 10.
score_key(50) :- key_activated.
score_key(0) :- not key_activated.

final_score(S) :- score_reach(R), score_key(K), S = R + K.

#maximize { S : final_score(S) }.

% === Output ===
#show seed/1.
#show activated/1.
#show total_cost/1.
#show activated_count/1.
#show key_activated/0.
#show final_score/1.