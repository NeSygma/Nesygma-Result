% Domain: Genes
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).

% Each gene has exactly one state (0 or 1)
{ state(G, 0..1) } 1 :- gene(G).

% Regulatory Rules - Define next_state based on current state
% g1 is active IFF g2 is not active
next_state(g1, 1) :- state(g2, 0).
next_state(g1, 0) :- state(g2, 1).

% g2 is active IFF g1 is not active
next_state(g2, 1) :- state(g1, 0).
next_state(g2, 0) :- state(g1, 1).

% g3 is active IFF (g4 is active AND g5 is active)
next_state(g3, 1) :- state(g4, 1), state(g5, 1).
next_state(g3, 0) :- state(g4, 0).
next_state(g3, 0) :- state(g5, 0).

% g4 is always active (constitutive)
next_state(g4, 1).

% g5 is always active (constitutive)
next_state(g5, 1).

% Steady state: current state equals next state for ALL genes
steady :- state(G, V), next_state(G, V), gene(G).
:- not steady.

% Ensure next_state matches state for each gene
:- state(G, V), next_state(G, W), V != W.

% Output: show the state of each gene in steady states
#show state/2.