%%% Byzantine Generals Problem - Consensus Determination %%%

%%% Domain Facts %%%
% Generals
general(g1; g2; g3; g4).

% Initial proposals
proposal(g1, 1).
proposal(g2, 1).
proposal(g3, 0).
proposal(g4, 1).

% Traitor (Byzantine faulty general)
traitor(g4).

% Honest generals are those not traitors
honest(G) :- general(G), not traitor(G).

%%% Compute honest votes %%%
% The honest generals' initial proposals are their true votes
honest_vote(G, V) :- honest(G), proposal(G, V).

%%% Count honest votes for each value %%%
vote_count_0(N0) :- N0 = #count{ G : honest_vote(G, 0) }.
vote_count_1(N1) :- N1 = #count{ G : honest_vote(G, 1) }.

%%% Determine consensus %%%
% If more honest votes for 1 than 0, consensus is 1
consensus(1) :- vote_count_1(N1), vote_count_0(N0), N1 > N0.

% If more honest votes for 0 than 1, consensus is 0
consensus(0) :- vote_count_1(N1), vote_count_0(N0), N0 > N1.

% Tie-breaking: if equal honest votes, default to 0
consensus(0) :- vote_count_1(N1), vote_count_0(N0), N1 = N0.

%%% Validity check: If all honest generals have same initial value, that must be consensus %%%
% All honest have value 1
all_honest_1 :- #count{ G : honest(G), proposal(G, 1) } = #count{ G : honest(G) }.
% All honest have value 0
all_honest_0 :- #count{ G : honest(G), proposal(G, 0) } = #count{ G : honest(G) }.

% Constraint: if all honest are 1, consensus must be 1
:- all_honest_1, not consensus(1).
% Constraint: if all honest are 0, consensus must be 0
:- all_honest_0, not consensus(0).

%%% Show results %%%
#show consensus/1.
#show honest_general(G) : honest(G).
#show traitor/1.