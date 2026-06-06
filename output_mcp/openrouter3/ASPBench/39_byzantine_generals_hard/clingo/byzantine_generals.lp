% Byzantine Generals Problem with Hierarchy and Deception

% ===== DOMAIN DECLARATIONS =====
% Generals and their properties
general(g1). general(g2). general(g3). general(g4). general(g5). general(g6).

% Ranks: commander=3, lieutenant=2, sergeant=1
rank(g1, 3). rank(g2, 2). rank(g3, 2). rank(g4, 1). rank(g5, 1). rank(g6, 1).

% Weights (same as rank for simplicity)
weight(g1, 3). weight(g2, 2). weight(g3, 2). weight(g4, 1). weight(g5, 1). weight(g6, 1).

% Initial proposals (round 0 beliefs)
initial_belief(g1, 1). initial_belief(g2, 1). initial_belief(g3, 0).
initial_belief(g4, 0). initial_belief(g5, 1). initial_belief(g6, 1).

% Trust network: high trust pairs (G1,G2) and (G2,G1) with +1 bonus
trust(g1, g2). trust(g2, g1).

% Rounds: 0 (initial), 1, 2 (final)
round(0). round(1). round(2).

% ===== TRAITOR SELECTION =====
% Exactly 2 traitors
1 { traitor(G) : general(G) } 2.

% ===== BELIEF PREDICATES =====
% belief(G, R, V) - general G has belief value V at round R

% Honest generals' true belief at each round (what they actually believe)
honest_belief(G, R, V) :- general(G), round(R), not traitor(G),
    R = 0, initial_belief(G, V).

% ===== MESSAGE PASSING =====
% Messages sent from G_from to G_to at round R

% Helper: rank comparison
higher_rank(G1, G2) :- rank(G1, R1), rank(G2, R2), R1 > R2.
equal_rank(G1, G2) :- rank(G1, R), rank(G2, R), G1 != G2.
lower_rank(G1, G2) :- rank(G1, R1), rank(G2, R2), R1 < R2.

% Message value sent by honest general
message(G_from, G_to, R, V) :-
    general(G_from), general(G_to), round(R), G_from != G_to,
    not traitor(G_from),
    honest_belief(G_from, R, V).

% Message value sent by traitor
% Traitors send lies (opposite of their belief) to equal or lower rank
% But send truth to higher-ranked generals
message(G_from, G_to, R, V) :-
    general(G_from), general(G_to), round(R), G_from != G_to,
    traitor(G_from),
    higher_rank(G_to, G_from),  % G_to has higher rank
    honest_belief(G_from, R, V).  % Send truth to higher rank

message(G_from, G_to, R, V) :-
    general(G_from), general(G_to), round(R), G_from != G_to,
    traitor(G_from),
    not higher_rank(G_to, G_from),  % G_to has equal or lower rank
    honest_belief(G_from, R, B),
    V = 1 - B.  % Send opposite (lie) to equal or lower rank

% ===== BELIEF UPDATE =====
% Weighted majority calculation for honest generals

% Trust weight calculation - fixed version
trust_weight(G_from, G_to, W) :-
    weight(G_from, BaseW),
    trust(G_from, G_to),
    W = BaseW + 1.

trust_weight(G_from, G_to, W) :-
    weight(G_from, BaseW),
    not trust(G_from, G_to),
    W = BaseW.

% Calculate total weight for each value at each round for each general
total_weight_trust(G_to, R, 0, W0) :-
    general(G_to), round(R),
    W0 = #sum { TW, G_from : message(G_from, G_to, R, 0), trust_weight(G_from, G_to, TW) }.

total_weight_trust(G_to, R, 1, W1) :-
    general(G_to), round(R),
    W1 = #sum { TW, G_from : message(G_from, G_to, R, 1), trust_weight(G_from, G_to, TW) }.

% Update honest belief based on weighted majority
% For round 1 and 2 (not round 0, which is initial)
honest_belief(G, R, 0) :-
    general(G), round(R), R > 0, not traitor(G),
    total_weight_trust(G, R, 0, W0),
    total_weight_trust(G, R, 1, W1),
    W0 >= W1.  % Tie-breaking: defaults to 0

honest_belief(G, R, 1) :-
    general(G), round(R), R > 0, not traitor(G),
    total_weight_trust(G, R, 0, W0),
    total_weight_trust(G, R, 1, W1),
    W1 > W0.

% ===== CONSENSUS CHECK =====
% All honest generals must agree on the same final value
consensus_value(V) :-
    general(G), not traitor(G),
    honest_belief(G, 2, V),
    #count { G : general(G), not traitor(G) } = N,
    #count { G : general(G), not traitor(G), honest_belief(G, 2, V) } = N.

% ===== FINAL BELIEFS OUTPUT =====
final_belief(G, V) :- general(G), not traitor(G), honest_belief(G, 2, V).

% ===== SHOW DIRECTIVES =====
#show traitor/1.
#show consensus_value/1.
#show final_belief/2.