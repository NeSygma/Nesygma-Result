% Genes
gene(g1; g2; g3; g4; g5).

% Each gene is either 0 (inactive) or 1 (active)
{state(G, 0); state(G, 1)} = 1 :- gene(G).

% --- Regulatory Rules ---

% Rule 1: g1 is active IFF g2 is not active
% Rule 2: g2 is active IFF g1 is not active
% Together: g1 and g2 must have opposite states
:- state(g1, 1), state(g2, 1).
:- state(g1, 0), state(g2, 0).

% Rule 3: g3 is active IFF (g4 is active AND g5 is active)
% If g3 is 1, then g4 must be 1 and g5 must be 1
:- state(g3, 1), state(g4, 0).
:- state(g3, 1), state(g5, 0).
% If g4 is 1 and g5 is 1, then g3 must be 1 (cannot be 0)
:- state(g3, 0), state(g4, 1), state(g5, 1).

% Rule 4: g4 is active ALWAYS (constitutive expression)
:- state(g4, 0).

% Rule 5: g5 is active ALWAYS (constitutive expression)
:- state(g5, 0).

% Show results
#show state/2.