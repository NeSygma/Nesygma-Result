% ============================================================
% Byzantine Generals with Hierarchy and Deception
% ============================================================

% --- Domain: Generals ---
general(g1). general(g2). general(g3). general(g4). general(g5). general(g6).

% --- Ranks and Weights ---
rank(g1, commander). weight(g1, 3). order(g1, 3).
rank(g2, lieutenant). weight(g2, 2). order(g2, 2).
rank(g3, lieutenant). weight(g3, 2). order(g3, 2).
rank(g4, sergeant). weight(g4, 1). order(g4, 1).
rank(g5, sergeant). weight(g5, 1). order(g5, 1).
rank(g6, sergeant). weight(g6, 1). order(g6, 1).

% --- Trust Network ---
trust(g1, g2).
trust(g2, g1).

% Trust bonus
trust_bonus(1).

% --- Initial Proposals (Round 0) ---
initial_belief(g1, 1).
initial_belief(g2, 1).
initial_belief(g3, 0).
initial_belief(g4, 0).
initial_belief(g5, 1).
initial_belief(g6, 1).

% --- Protocol Parameters ---
num_traitors(2).
num_rounds(2).
round(0). round(1). round(2).

% --- Tie-breaking rule ---
tie_break(0).

% ============================================================
% Traitor Selection
% ============================================================

% Exactly 2 traitors
{ traitor(G) : general(G) } 2.
honest(G) :- general(G), not traitor(G).

% ============================================================
% Belief Initialization (Round 0)
% ============================================================

belief(G, 0, V) :- initial_belief(G, V).

% ============================================================
% Message Sending Rules
% ============================================================

% Honest generals send their true belief
sends(S, R, T, V) :- honest(S), belief(S, T, V), general(R), R != S, round(T), T < 2.

% Traitors send lies to equal or lower rank, truth to higher rank
% Lie = opposite of belief
sends(S, R, T, 0) :- traitor(S), belief(S, T, 1), general(R), R != S, round(T), T < 2,
                       order(S, OS), order(R, OR), OS >= OR.
sends(S, R, T, 1) :- traitor(S), belief(S, T, 0), general(R), R != S, round(T), T < 2,
                       order(S, OS), order(R, OR), OS >= OR.

% Traitors send truth to higher rank
sends(S, R, T, V) :- traitor(S), belief(S, T, V), general(R), R != S, round(T), T < 2,
                       order(S, OS), order(R, OR), OS < OR.

% ============================================================
% Weight Calculation for Received Messages
% ============================================================

% Base weight is sender's rank weight
msg_weight(S, R, T, W) :- sends(S, R, T, _), weight(S, W), round(T), T < 2.

% Trust bonus adds +1
msg_weight(S, R, T, W+1) :- sends(S, R, T, _), trust(S, R), weight(S, W), round(T), T < 2.

% ============================================================
% Weighted Majority for Honest Generals
% ============================================================

% Sum of weights for messages with value 1
sum_v1(R, T, S) :- S = #sum { W, S2 : sends(S2, R, T, 1), msg_weight(S2, R, T, W) },
                    honest(R), round(T), T < 2.

% Sum of weights for messages with value 0
sum_v0(R, T, S) :- S = #sum { W, S2 : sends(S2, R, T, 0), msg_weight(S2, R, T, W) },
                    honest(R), round(T), T < 2.

% Honest generals update belief based on weighted majority
belief(R, T+1, 1) :- honest(R), round(T), T < 2, sum_v1(R, T, S1), sum_v0(R, T, S0), S1 > S0.
belief(R, T+1, 0) :- honest(R), round(T), T < 2, sum_v1(R, T, S1), sum_v0(R, T, S0), S0 > S1.

% Tie-breaking: default to 0
belief(R, T+1, 0) :- honest(R), round(T), T < 2, sum_v1(R, T, S1), sum_v0(R, T, S0), S1 == S0.

% ============================================================
% Consensus Requirement
% ============================================================

% All honest generals must agree on the same final value
consensus_value(V) :- belief(g1, 2, V), honest(g1).
consensus_value(V) :- belief(g2, 2, V), honest(g2).
consensus_value(V) :- belief(g3, 2, V), honest(g3).
consensus_value(V) :- belief(g4, 2, V), honest(g4).
consensus_value(V) :- belief(g5, 2, V), honest(g5).
consensus_value(V) :- belief(g6, 2, V), honest(g6).

% Constraint: all honest generals must have the same final belief
:- honest(G1), honest(G2), belief(G1, 2, V1), belief(G2, 2, V2), V1 != V2.

% ============================================================
% Output
% ============================================================

#show traitor/1.
#show honest/1.
#show consensus_value/1.
#show belief/3.
#show final_belief/2.

% Final beliefs for honest generals
final_belief(G, V) :- honest(G), belief(G, 2, V).