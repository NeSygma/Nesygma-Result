% Byzantine Generals Problem with Hierarchy and Deception

% --- Domain ---
general(g1). general(g2). general(g3). general(g4). general(g5). general(g6).

% Ranks: commander=3, lieutenant=2, sergeant=1
rank(g1,3). rank(g2,2). rank(g3,2). rank(g4,1). rank(g5,1). rank(g6,1).

% Weights
weight(g1,3). weight(g2,2). weight(g3,2). weight(g4,1). weight(g5,1). weight(g6,1).

% Initial beliefs (Round 0)
initial_belief(g1,1). initial_belief(g2,1). initial_belief(g3,0).
initial_belief(g4,0). initial_belief(g5,1). initial_belief(g6,1).

% Trust network (high trust pairs)
trust(g1,g2). trust(g2,g1).

% --- Traitor selection ---
% Exactly 2 traitors
{ traitor(G) : general(G) } 2.
% Ensure exactly 2 (the choice rule already enforces exactly 2, but we can add constraint for safety)
:- #count{ G : traitor(G) } != 2.

% Honest generals
honest(G) :- general(G), not traitor(G).

% --- Beliefs ---
% Time points: 0,1,2
time(0..2).

% For traitors: belief is constant initial belief.
belief(G,T,B) :- traitor(G), initial_belief(G,B), time(T).

% For honest: belief at time 0 is initial belief.
belief(G,0,B) :- honest(G), initial_belief(G,B).

% --- Message sending ---
% Rounds: 1 and 2
round(1). round(2).

% Message value from S to Rcv at round R
message_value(S,Rcv,R,Val) :-
    honest(S), round(R), general(S), general(Rcv), S != Rcv,
    belief(S, R-1, Val).

message_value(S,Rcv,R,Val) :-
    traitor(S), round(R), general(S), general(Rcv), S != Rcv,
    rank(S, RS), rank(Rcv, RR), RS > RR,
    belief(S, R-1, Val).

message_value(S,Rcv,R,Val) :-
    traitor(S), round(R), general(S), general(Rcv), S != Rcv,
    rank(S, RS), rank(Rcv, RR), RS <= RR,
    belief(S, R-1, Bel),
    Val = 1 - Bel.

% --- Message weight ---
message_weight(S,Rcv,R,W) :-
    round(R), general(S), general(Rcv), S != Rcv,
    weight(S, WS),
    (trust(S,Rcv) -> W = WS + 1 ; W = WS).

% --- Weighted majority for honest generals at each round ---
% For each honest G at round R (R=1,2), compute total weight for value 0 and 1.
total_weight_0(G,R, Sum) :-
    honest(G), round(R),
    Sum = #sum{ W, S : message_weight(S,G,R,W), message_value(S,G,R,0) }.

total_weight_1(G,R, Sum) :-
    honest(G), round(R),
    Sum = #sum{ W, S : message_weight(S,G,R,W), message_value(S,G,R,1) }.

% Belief update for honest G at time R (where R=1,2)
belief(G,R,0) :- honest(G), round(R),
    total_weight_0(G,R, W0), total_weight_1(G,R, W1), W0 >= W1.

belief(G,R,1) :- honest(G), round(R),
    total_weight_0(G,R, W0), total_weight_1(G,R, W1), W0 < W1.

% --- Consensus requirement ---
% All honest generals must agree on the same final value after round 2.
% We'll enforce that all honest have same belief at time 2.
:- honest(G1), honest(G2), belief(G1,2,V1), belief(G2,2,V2), V1 != V2.

% Derive consensus value (any honest general's belief at time 2)
consensus_value(V) :- honest(G), belief(G,2,V).

% --- Output ---
% Show consensus value and final beliefs of honest generals.
#show consensus_value/1.
#show final_belief/2.  % final_belief(G, V) for honest G at time 2
final_belief(G,V) :- honest(G), belief(G,2,V).

% Also show traitors for debugging.
#show traitor/1.