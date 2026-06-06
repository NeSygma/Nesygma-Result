% Define the genes
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).

% Define possible state values
state_value(0). state_value(1).

% Generate all possible state assignments (each gene has exactly one state)
{ state(G, V) : state_value(V) } = 1 :- gene(G).

% Regulatory constraints

% g4 and g5 are always active (constitutive expression)
:- not state(g4, 1).
:- not state(g5, 1).

% g3 is active iff (g4 is active AND g5 is active)
% Since g4 and g5 are always active, g3 must be active
:- not state(g3, 1).

% g1 is active iff g2 is not active
% This is equivalent to: g1 and g2 must have different values
:- state(g1, 1), state(g2, 1).  % Cannot both be 1
:- state(g1, 0), state(g2, 0).  % Cannot both be 0

% Show the steady states
#show state/2.