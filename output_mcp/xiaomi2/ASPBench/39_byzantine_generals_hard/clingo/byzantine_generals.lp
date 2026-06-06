% ===== Domain =====
general(g1). general(g2). general(g3). general(g4). general(g5). general(g6).
round(0). round(1). round(2).
value(0). value(1).

% ===== Weights and Orders =====
weight(g1, 3). weight(g2, 2). weight(g3, 2).
weight(g4, 1). weight(g5, 1). weight(g6, 1).

order_val(g1, 3). order_val(g2, 2). order_val(g3, 2).
order_val(g4, 1). order_val(g5, 1). order_val(g6, 1).

% ===== Initial Beliefs (Round 0) =====
belief(g1, 0, 1). belief(g2, 0, 1). belief(g3, 0, 0).
belief(g4, 0, 0). belief(g5, 0, 1). belief(g6, 0, 1).

% ===== Trust Network =====
trust(g1, g2). trust(g2, g1).
trust_bonus(1).

% ===== Traitor Selection (exactly 2) =====
2 { traitor(G) : general(G) } 2.

honest(G) :- general(G), not traitor(G).

% ===== Effective Weight (rank weight + trust bonus if trusted) =====
eff_weight(S, G, W) :- weight(S, W), general(S), general(G), S != G, not trust(S, G).
eff_weight(S, G, W) :- weight(S, W0), trust_bonus(B), W = W0 + B, trust(S, G), general(S), general(G), S != G.

% ===== Message Sending (Round R uses beliefs from Round R-1) =====
% Honest generals send their true belief from previous round
msg(S, G, R, V) :- honest(S), belief(S, R-1, V), general(G), S != G, round(R), R > 0.

% Traitors send lies (opposite of belief) to generals of equal or lower rank
msg(S, G, R, V) :- traitor(S), belief(S, R-1, V0), V = 1 - V0,
                    order_val(S, OS), order_val(G, OG), OG <= OS,
                    general(G), S != G, round(R), R > 0.

% Traitors send truth to higher-ranked generals
msg(S, G, R, V) :- traitor(S), belief(S, R-1, V),
                    order_val(S, OS), order_val(G, OG), OG > OS,
                    general(G), S != G, round(R), R > 0.

% ===== Weighted Sum Computation =====
weight_sum(G, R, 0, S) :- S = #sum{W, S2 : msg(S2, G, R, 0), eff_weight(S2, G, W)},
                           general(G), round(R), R > 0.
weight_sum(G, R, 1, S) :- S = #sum{W, S2 : msg(S2, G, R, 1), eff_weight(S2, G, W)},
                           general(G), round(R), R > 0.

% ===== Belief Update (weighted majority, tie-break to 0) =====
belief(G, R, 1) :- weight_sum(G, R, 1, S1), weight_sum(G, R, 0, S0), S1 > S0,
                   general(G), round(R), R > 0.
belief(G, R, 0) :- weight_sum(G, R, 1, S1), weight_sum(G, R, 0, S0), S0 >= S1,
                   general(G), round(R), R > 0.

% ===== Consensus Constraint: all honest generals must agree after round 2 =====
:- honest(G1), honest(G2), belief(G1, 2, V1), belief(G2, 2, V2), V1 != V2.

% ===== Consensus Value =====
consensus_value(V) :- value(V), belief(G, 2, V), honest(G).

% ===== Final Beliefs (only honest generals) =====
final_belief(G, V) :- honest(G), belief(G, 2, V).

% ===== Output =====
#show traitor/1.
#show consensus_value/1.
#show final_belief/2.