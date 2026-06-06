% Domain and instance data
% Ranks: commander > lieutenant > sergeant
rank("G1", "commander"). weight("G1", 3). order("G1", 3).
rank("G2", "lieutenant"). weight("G2", 2). order("G2", 2).
rank("G3", "lieutenant"). weight("G3", 2). order("G3", 2).
rank("G4", "sergeant"). weight("G4", 1). order("G4", 1).
rank("G5", "sergeant"). weight("G5", 1). order("G5", 1).
rank("G6", "sergeant"). weight("G6", 1). order("G6", 1).

% Initial beliefs (Round 0)
initial_belief("G1", 1).
initial_belief("G2", 1).
initial_belief("G3", 0).
initial_belief("G4", 0).
initial_belief("G5", 1).
initial_belief("G6", 1).

% Trust network (high trust pairs with bonus)
trust_bonus("G1", "G2").
trust_bonus("G2", "G1").

% Rounds
round(0..2).

% General domain
general(G) :- rank(G, _).

% Helper: higher rank (strictly higher order)
higher_rank(G1, G2) :- order(G1, O1), order(G2, O2), O1 > O2.

% Helper: same or lower rank (order(G1) =< order(G2))
same_or_lower_rank(G1, G2) :- order(G1, O1), order(G2, O2), O1 = O2.
same_or_lower_rank(G1, G2) :- order(G1, O1), order(G2, O2), O1 < O2.

% Exactly 2 traitors
1 { traitor(G) : general(G) } 2.

% Derive honest generals
honest(G) :- general(G), not traitor(G).

% Initial beliefs (Round 0)
belief_round(0, G, V) :- initial_belief(G, V).

% Message passing for rounds 1 and 2
% Messages are sent from every general to every other general
% The value sent depends on whether the sender is honest or a traitor

% Honest generals always send their true belief
message_round(R, Sender, Receiver, V) :-
    honest(Sender),
    belief_round(R-1, Sender, V),
    honest(Receiver),
    general(Sender),
    general(Receiver),
    round(R),
    R > 0.

% Traitors send lies to generals of equal or lower rank, truth to higher rank
message_round(R, Sender, Receiver, V) :-
    traitor(Sender),
    belief_round(R-1, Sender, V_orig),
    V = 1 - V_orig,  % Lie by default
    same_or_lower_rank(Sender, Receiver),
    honest(Receiver),
    general(Sender),
    general(Receiver),
    round(R),
    R > 0.

% Traitors send truth to higher-ranked generals
message_round(R, Sender, Receiver, V) :-
    traitor(Sender),
    belief_round(R-1, Sender, V),
    higher_rank(Sender, Receiver),
    honest(Receiver),
    general(Sender),
    general(Receiver),
    round(R),
    R > 0.

% Belief update for honest generals after receiving messages
% Compute weighted sum of received messages
% Weight = sender's base weight + trust bonus if trusted

% Count weighted votes for each value
weighted_vote(R, Receiver, V, TotalWeight) :-
    honest(Receiver),
    round(R),
    V = 0 ; V = 1,
    TotalWeight = #sum { W : message_round(R, Sender, Receiver, V), 
                          weight(Sender, BaseW), 
                          (trust_bonus(Sender, Receiver) ? BaseW + 1 : BaseW) = W }.

% Belief update rule: honest generals adopt the value with higher weighted vote
% Tie defaults to 0
belief_round(R, Receiver, 0) :-
    honest(Receiver),
    round(R),
    R > 0,
    weighted_vote(R, Receiver, 0, W0),
    weighted_vote(R, Receiver, 1, W1),
    W0 > W1.

belief_round(R, Receiver, 1) :-
    honest(Receiver),
    round(R),
    R > 0,
    weighted_vote(R, Receiver, 1, W1),
    weighted_vote(R, Receiver, 0, W0),
    W1 > W0.

belief_round(R, Receiver, 0) :-
    honest(Receiver),
    round(R),
    R > 0,
    weighted_vote(R, Receiver, 0, W0),
    weighted_vote(R, Receiver, 1, W1),
    W0 = W1.

% Consensus requirement: all honest generals must have the same final belief
% Final round is round 2
final_belief(G, V) :- honest(G), belief_round(2, G, V).

% Exactly one consensus value among honest generals
1 { consensus_value(V) : V = 0 ; V = 1 } 1.

% Constraint: all honest generals must agree with the consensus value
:- honest(G), final_belief(G, V), consensus_value(V1), V != V1.

% Show the solution
#show traitor/1.
#show consensus_value/1.
#show final_belief/2.