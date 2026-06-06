% --- Domain Declarations ---

% Generals and their ranks, weights, and orders
general(g1; g2; g3; g4; g5; g6).

rank(g1, commander). weight(g1, 3). order(g1, 3).
rank(g2, lieutenant). weight(g2, 2). order(g2, 2).
rank(g3, lieutenant). weight(g3, 2). order(g3, 2).
rank(g4, sergeant). weight(g4, 1). order(g4, 1).
rank(g5, sergeant). weight(g5, 1). order(g5, 1).
rank(g6, sergeant). weight(g6, 1). order(g6, 1).

% Initial beliefs (Round 0)
initial_belief(g1, 1).
initial_belief(g2, 1).
initial_belief(g3, 0).
initial_belief(g4, 0).
initial_belief(g5, 1).
initial_belief(g6, 1).

% Trust network
trust(g1, g2). trust(g2, g1).
trust_bonus(1).

% Time steps
time(0..2).

% --- Traitor Identification ---
1 { traitor(G) : general(G) } 2.
honest(G) :- general(G), not traitor(G).

% --- Initial Beliefs (Round 0) ---
belief(G, 0, V) :- initial_belief(G, V).

% --- Message Passing ---
% Sent messages
sent_message(S, R, Round, V) :-
    honest(S),
    honest(R),
    Round > 0,
    belief(S, Round-1, V),
    time(Round).

sent_message(S, R, Round, 1-V) :-
    traitor(S),
    honest(R),
    Round > 0,
    belief(S, Round-1, V),
    rank(S, RS),
    rank(R, RR),
    order(S, OS),
    order(R, OR),
    OS =< OR,
    time(Round).

sent_message(S, R, Round, V) :-
    traitor(S),
    honest(R),
    Round > 0,
    belief(S, Round-1, V),
    rank(S, RS),
    rank(R, RR),
    order(S, OS),
    order(R, OR),
    OS > OR,
    time(Round).

% Received messages
received_message(R, S, Round, V) :-
    sent_message(S, R, Round, V),
    time(Round).

% --- Effective Weight Calculation ---
effective_weight(G, W) :- weight(G, W), honest(G).

% Trust bonus applies if the sender is trusted by the receiver and the receiver is honest
effective_weight(R, W+TB) :-
    received_message(R, S, Round, _),
    trust(S, R),
    trust(R, S),
    traitor(S),
    honest(R),
    weight(S, W),
    trust_bonus(TB),
    time(Round).

% --- Belief Update ---
% Helper predicates for sums
sum_received_0(G, Round, Sum) :-
    honest(G),
    time(Round),
    Sum = #sum { W : received_message(G, S, Round-1, 0), effective_weight(S, W) }.

sum_received_1(G, Round, Sum) :-
    honest(G),
    time(Round),
    Sum = #sum { W : received_message(G, S, Round-1, 1), effective_weight(S, W) }.

% Update belief for honest generals in Round 1 and 2
belief(G, Round, 0) :-
    honest(G),
    Round > 0,
    time(Round),
    sum_received_0(G, Round, Sum0),
    sum_received_1(G, Round, Sum1),
    Sum0 > Sum1.

belief(G, Round, 1) :-
    honest(G),
    Round > 0,
    time(Round),
    sum_received_0(G, Round, Sum0),
    sum_received_1(G, Round, Sum1),
    Sum1 > Sum0.

% Tie-breaking rule: default to 0
belief(G, Round, 0) :-
    honest(G),
    Round > 0,
    time(Round),
    sum_received_0(G, Round, Sum0),
    sum_received_1(G, Round, Sum1),
    Sum0 = Sum1.

% --- Final Beliefs ---
final_belief(G, V) :- honest(G), belief(G, 2, V).

% --- Consensus ---
% Ensure all honest generals agree on the same final value
consensus_value(V) :-
    honest(G),
    final_belief(G, V),
    general(G).

:- honest(G1), honest(G2), final_belief(G1, V1), final_belief(G2, V2), V1 != V2.

% --- Show Directives ---
#show traitor/1.
#show consensus_value/1.
#show final_belief/2.