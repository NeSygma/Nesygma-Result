% === Domain: Generals ===
general(g1). general(g2). general(g3). general(g4).

% === Initial Proposals ===
proposal(g1, 1).
proposal(g2, 1).
proposal(g3, 0).
proposal(g4, 1).

% === Traitor Identification ===
traitor(g4).

% === Honest Generals (not traitors) ===
honest(G) :- general(G), not traitor(G).

% === Count honest votes for each value ===
honest_vote_count(Val, N) :- 
    N = #count{G : honest(G), proposal(G, Val)}, 
    Val = 0..1.

% === Majority Rule ===
% Find the maximum honest vote count
max_honest_votes(MaxN) :- 
    MaxN = #max{N : honest_vote_count(_, N)}.

% A value wins majority if its honest vote count equals the max
majority_value(Val) :- 
    honest_vote_count(Val, N), 
    max_honest_votes(N).

% === Tie-Breaking: default to 0 if tie ===
% Count how many values achieve the majority count
majority_count(C) :- C = #count{Val : majority_value(Val)}.

% If tie (multiple values with same max count), consensus is 0
consensus(0) :- majority_count(C), C > 1.

% If unique majority, consensus is that value
consensus(Val) :- majority_value(Val), majority_count(1).

% === Output ===
#show consensus/1.
#show honest/1.
#show traitor/1.