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
% Belief at time 0 (initial)
belief(G,0) :- initial_belief(G,0).
belief(G,0) :- initial_belief(G,1).

% For traitors, belief stays constant (initial belief) for all times
belief(G,T) :- traitor(G), initial_belief(G,B), T = 1..2, belief(G,0) = B.  % Actually, we need to set belief(G,T) = B
% But we can simply state that for traitors, belief(G,T) = initial_belief(G) for T=0,1,2.
% We'll derive belief(G,T) for traitors separately.

% For honest generals, belief at T>0 is derived from messages.

% --- Message sending ---
% Rounds: 1 and 2
round(1). round(2).

% Message value from S to Rcv at round R
message_value(S,Rcv,R,Val) :-
    honest(S), round(R), general(S), general(Rcv), S != Rcv,
    Val = belief(S, R-1).

message_value(S,Rcv,R,Val) :-
    traitor(S), round(R), general(S), general(Rcv), S != Rcv,
    rank(S) > rank(Rcv),
    Val = belief(S, R-1).

message_value(S,Rcv,R,Val) :-
    traitor(S), round(R), general(S), general(Rcv), S != Rcv,
    rank(S) <= rank(Rcv),
    belief(S, R-1, Bel),  % We need to get belief value
    Val = 1 - Bel.

% But we need to define belief(S, R-1, Bel) for traitors. Let's define a helper.
belief_val(G,T,Val) :- belief(G,T) = Val.  % This is not valid ASP. Instead, we can use belief(G,T) as value.

% Actually, we can just use belief(G,T) as the value. So we can write:
% For traitors, belief(G,T) is defined as initial_belief(G) for all T.
% Let's define that explicitly.

% For traitors, belief at any time is their initial belief.
belief(G,T) :- traitor(G), initial_belief(G,B), T = 0..2, B = 0.  % This sets belief(G,T)=0 if initial is 0
belief(G,T) :- traitor(G), initial_belief(G,B), T = 0..2, B = 1.  % This sets belief(G,T)=1 if initial is 1

% But this will create multiple beliefs for same G,T? Actually, it's fine because B is fixed.

% However, we already defined belief(G,0) for all. For traitors, we need to override belief(G,1) and belief(G,2).
% Let's remove the earlier belief(G,0) for traitors and define uniformly.

% Redefine belief for all generals at all times:
% For traitors: belief(G,T) = initial_belief(G) for T=0,1,2.
% For honest: belief(G,0) = initial_belief(G); belief(G,1) and belief(G,2) derived later.

% We'll use separate rules.

% First, clear previous belief definitions.
% We'll start fresh.

% Let's rewrite the belief section more cleanly.

% --- Belief definitions ---
% Time points: 0,1,2
time(0..2).

% For traitors: belief is constant initial belief.
belief(G,T) :- traitor(G), initial_belief(G,B), time(T), B = 0.
belief(G,T) :- traitor(G), initial_belief(G,B), time(T), B = 1.

% For honest: belief at time 0 is initial belief.
belief(G,0) :- honest(G), initial_belief(G,B), B = 0.
belief(G,0) :- honest(G), initial_belief(G,B), B = 1.

% Now, for honest at time 1 and 2, we need to compute based on messages.

% --- Message weight ---
message_weight(S,Rcv,R,W) :-
    round(R), general(S), general(Rcv), S != Rcv,
    weight(S, WS),
    (trust(S,Rcv) -> W = WS + 1 ; W = WS).

% --- Weighted majority for honest generals at each round ---
% For each honest G at round R (R=1,2), compute total weight for value 0 and 1.
% We'll use aggregates.

% Total weight for value 0 received by G at round R
total_weight_0(G,R) = #sum{ W, S : message_weight(S,G,R,W), message_value(S,G,R,0) }.

% Total weight for value 1 received by G at round R
total_weight_1(G,R) = #sum{ W, S : message_weight(S,G,R,W), message_value(S,G,R,1) }.

% Belief update for honest G at time R (where R=1,2)
belief(G,R) :- honest(G), round(R),
    total_weight_0(G,R) >= total_weight_1(G,R),
    belief(G,R) = 0.

belief(G,R) :- honest(G), round(R),
    total_weight_0(G,R) < total_weight_1(G,R),
    belief(G,R) = 1.

% Tie-breaking: default to 0 (already covered by >=).

% --- Consensus requirement ---
% All honest generals must agree on the same final value after round 2.
consensus_value(V) :- V = belief(G,2), honest(G), #count{ G : honest(G) } = N, #count{ G : honest(G), belief(G,2) = V } = N.

% Alternatively, we can enforce that all honest have same belief.
:- honest(G1), honest(G2), belief(G1,2) != belief(G2,2).

% --- Output ---
% Show consensus value and final beliefs of honest generals.
#show consensus_value/1.
#show final_belief/2.  % final_belief(G, V) for honest G at time 2
final_belief(G,V) :- honest(G), belief(G,2) = V.

% Also show traitors for debugging.
#show traitor/1.