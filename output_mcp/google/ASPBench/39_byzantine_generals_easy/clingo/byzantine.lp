% --- Instance Data ---
general(g1; g2; g3; g4).
proposal(g1, 1).
proposal(g2, 1).
proposal(g3, 0).
proposal(g4, 1).
traitor(g4).

% --- Logic ---
honest(G) :- general(G), not traitor(G).

% Collect honest proposals
honest_proposal(G, V) :- honest(G), proposal(G, V).

% Count votes for each value
count_votes(V, N) :- V = 0..1, N = #count { G : honest_proposal(G, V) }.

% Determine consensus based on majority
% Majority Rule
consensus(1) :- count_votes(1, N1), count_votes(0, N0), N1 > N0.
consensus(0) :- count_votes(1, N1), count_votes(0, N0), N0 > N1.

% Tie-Breaking
consensus(0) :- count_votes(1, N1), count_votes(0, N0), N1 == N0.

% --- Output ---
#show consensus/1.
#show honest/1.
#show traitor/1.