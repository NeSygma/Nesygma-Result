% --- Generals and their attributes ---
general("G1"; "G2"; "G3"; "G4"; "G5"; "G6").

order("G1", 3). order("G2", 2). order("G3", 2). order("G4", 1). order("G5", 1). order("G6", 1).
weight("G1", 3). weight("G2", 2). weight("G3", 2). weight("G4", 1). weight("G5", 1). weight("G6", 1).

% Initial proposals (Round 0)
init_belief("G1", 1). init_belief("G2", 1). init_belief("G3", 0). init_belief("G4", 0). init_belief("G5", 1). init_belief("G6", 1).

% Trust network
trust("G1", "G2"). trust("G2", "G1").

% Rounds: 0 = initial, 1 and 2 = message exchange rounds
round(0..2).
value(0;1).

% --- Traitor identification ---
% Exactly 2 traitors among the 6 generals
{traitor(G)} :- general(G).
:- #count{G : traitor(G)} != 2.

% Honest generals are those not identified as traitors
honest(G) :- general(G), not traitor(G).

% --- Belief evolution ---

% Belief at round 0 = initial proposal
belief(G, 0, V) :- init_belief(G, V).

% For rounds 1 and 2:
% Traitors' beliefs are unconstrained (can be 0 or 1)
{belief(G, R, V)} :- traitor(G), round(R), R >= 1, value(V).
:- traitor(G), round(R), R >= 1, #count{V : belief(G, R, V)} != 1.

% --- Message passing ---
% Each general S sends a message to each other general H in round R (R >= 1)
% based on belief(S, R-1)

% Honest sender: sends true belief
msg(S, H, R, V) :- general(S), general(H), S != H, round(R), R >= 1,
    honest(S), belief(S, R-1, V).

% Traitor sender: 
% Sends truth to higher-ranked generals
msg(S, H, R, V) :- general(S), general(H), S != H, round(R), R >= 1,
    traitor(S), belief(S, R-1, V),
    order(H, OH), order(S, OS), OH > OS.

% Sends lie (opposite) to equal or lower ranked generals
msg(S, H, R, V) :- general(S), general(H), S != H, round(R), R >= 1,
    traitor(S), belief(S, R-1, B),
    order(H, OH), order(S, OS), OH <= OS, V = 1 - B.

% --- Message weight calculation ---
msg_weight(S, H, W) :- general(S), general(H), S != H,
    weight(S, W0),
    trust(S, H),
    W = W0 + 1.

msg_weight(S, H, W) :- general(S), general(H), S != H,
    weight(S, W0),
    not trust(S, H),
    W = W0.

% --- Weighted majority for honest generals ---
% Collect message info for each honest receiver
msg_info(H, S, R, V, W) :- honest(H), general(S), S != H, round(R), R >= 1,
    msg(S, H, R, V), msg_weight(S, H, W).

% Total weight of messages with value V received by honest H in round R
total_weight(H, R, V, TW) :- honest(H), round(R), R >= 1, value(V),
    TW = #sum { W, S : msg_info(H, S, R, V, W) }.

% Honest general adopts belief with higher total weight
belief(H, R, 0) :- honest(H), round(R), R >= 1,
    total_weight(H, R, 0, W0), total_weight(H, R, 1, W1), W0 > W1.

belief(H, R, 1) :- honest(H), round(R), R >= 1,
    total_weight(H, R, 1, W1), total_weight(H, R, 0, W0), W1 > W0.

% Tie-breaking rule: defaults to 0
belief(H, R, 0) :- honest(H), round(R), R >= 1,
    total_weight(H, R, 0, W0), total_weight(H, R, 1, W1), W0 = W1.

% --- Consensus requirement ---
% After round 2, all honest generals must agree on the same value
:- honest(G1), honest(G2), belief(G1, 2, V1), belief(G2, 2, V2), V1 != V2.

% --- Output predicates ---
% The consensus value (all honest agree on this after round 2)
consensus_value(V) :- honest(G), belief(G, 2, V).

% Final beliefs of honest generals
final_belief(G, V) :- honest(G), belief(G, 2, V).

#show traitor/1.
#show consensus_value/1.
#show final_belief/2.