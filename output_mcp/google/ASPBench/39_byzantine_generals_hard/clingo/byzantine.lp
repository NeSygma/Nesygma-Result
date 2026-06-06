% --- Data ---
general(g1, 3, 3).
general(g2, 2, 2).
general(g3, 2, 2).
general(g4, 1, 1).
general(g5, 1, 1).
general(g6, 1, 1).

initial_belief(g1, 1).
initial_belief(g2, 1).
initial_belief(g3, 0).
initial_belief(g4, 0).
initial_belief(g5, 1).
initial_belief(g6, 1).

trusted(g1, g2).
trusted(g2, g1).

% --- Traitor Identification ---
{traitor(G) : general(G, _, _)} = 2.
honest(G) :- general(G, _, _), not traitor(G).

% --- Weight Calculation ---
weight(S, R, W) :- general(S, _, BaseW), general(R, _, _), trusted(S, R), W = BaseW + 1.
weight(S, R, W) :- general(S, _, BaseW), general(R, _, _), not trusted(S, R), W = BaseW.

% --- Message Passing ---
% Round 0 beliefs
belief(G, 0, V) :- initial_belief(G, V).

% Round 1 and 2
round(1..2).

% Honest generals send truth
msg(S, R, Round, Val) :- honest(S), general(R, _, _), S != R, belief(S, Round-1, Val), round(Round).

% Traitor deception
% "Traitors send lies (opposite of their belief) to generals of equal or lower rank, 
% but send truth to higher-ranked generals."
msg(S, R, Round, Val) :- traitor(S), general(S, RankS, _), general(R, RankR, _), S != R, 
                         belief(S, Round-1, B), round(Round),
                         RankR > RankS, Val = B.
msg(S, R, Round, Val) :- traitor(S), general(S, RankS, _), general(R, RankR, _), S != R, 
                         belief(S, Round-1, B), round(Round),
                         RankR <= RankS, Val = 1 - B.

% --- Belief Update ---
% Weighted majority
% Sum of weights for value 0 and 1
sum_val(G, Round, Val, Sum) :- general(G, _, _), round(Round), Val = 0..1,
                               Sum = #sum { W, S : msg(S, G, Round, Val), weight(S, G, W) }.

% Tie-breaking rule: defaults to 0
% If no messages received, sum is 0, so defaults to 0.
belief(G, Round, 1) :- general(G, _, _), round(Round), 
                       sum_val(G, Round, 1, S1), sum_val(G, Round, 0, S0), S1 > S0.
belief(G, Round, 0) :- general(G, _, _), round(Round), 
                       sum_val(G, Round, 1, S1), sum_val(G, Round, 0, S0), S1 <= S0.

% --- Consensus Requirement ---
% All honest generals must agree on the same final value after the final round
consensus_value(V) :- V = 0..1, honest(G), belief(G, 2, V),
                      not { honest(G2), belief(G2, 2, V2) : V2 != V }.

% --- Output Mapping ---
#show traitor/1.
#show consensus_value/1.
#show belief/3.