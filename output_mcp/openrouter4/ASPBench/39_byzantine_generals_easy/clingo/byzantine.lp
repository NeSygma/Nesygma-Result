% ----------------------------------------------------------------------
% Byzantine Generals Problem
% 4 generals, 1 traitor (G4), initial proposals given
% ----------------------------------------------------------------------

% --- Facts from problem statement ---

% The four generals
general(g1; g2; g3; g4).

% Initial proposals (values each general initially proposes)
proposal(g1, 1).
proposal(g2, 1).
proposal(g3, 0).
proposal(g4, 1).

% The traitor is identified as G4
traitor(g4).

% --- Derived facts ---

% An honest general is any general who is not a traitor
honest_general(G) :- general(G), not traitor(G).

% Count how many honest generals there are
honest_count(N) :- N = #count{ G : honest_general(G) }.

% Count honest votes for value 0 and value 1
honest_vote_count(V, N) :- V=0..1, N = #count{ G : honest_general(G), proposal(G, V) }.

% --- Consensus determination ---

% Constraint 2 (Validity): If ALL honest generals have the same initial value,
% that MUST be the consensus.
% We check: if count for value V equals total honest count, consensus must be V.
consensus(V) :- honest_vote_count(V, N), honest_count(N).

% Constraint 3 (Majority Rule): The consensus reflects the majority among honest votes.
% If more honest generals proposed 1 than 0, consensus is 1.
consensus(1) :- honest_vote_count(1, C1), honest_vote_count(0, C0), C1 > C0.

% If more honest generals proposed 0 than 1, consensus is 0.
consensus(0) :- honest_vote_count(0, C0), honest_vote_count(1, C1), C0 > C1.

% Constraint 4 (Tie-Breaking): If honest votes are tied, default to 0.
consensus(0) :- honest_vote_count(0, C0), honest_vote_count(1, C1), C0 = C1.

% Constraint 1 (Agreement): All honest generals decide on the same value.
% This is implicitly satisfied because we derive a single consensus/1 value.

% Ensure exactly one consensus value is derived
:- not consensus(0), not consensus(1).

% --- Display ---
#show consensus/1.
#show honest_general/1.
#show traitor/1.