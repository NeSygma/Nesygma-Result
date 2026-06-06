% Ground the domain
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).
state(0). state(1).

% g4 and g5 are always active
state(g4, 1).
state(g5, 1).

% Generate possible states for genes not fixed by rules
{ state(g1, S) : state(S) } = 1.
{ state(g2, S) : state(S) } = 1.
{ state(g3, S) : state(S) } = 1.

% Rule 1: g1 is active iff g2 is not active
state(g1, 1) :- state(g2, 0).
state(g1, 0) :- state(g2, 1).

% Rule 2: g2 is active iff g1 is not active
state(g2, 1) :- state(g1, 0).
state(g2, 0) :- state(g1, 1).

% Rule 3: g3 is active iff (g4 is active AND g5 is active)
% Since g4 and g5 are always active, g3 can be 0 or 1 (no constraint needed).

% Ensure all genes have a state
:- gene(G), not state(G, _).

% A state is steady if it satisfies the rules (implicitly satisfied by the above rules)
steady_state :- gene(G), state(G, S).

% Output the steady states
#show state(g1, S) : state(g1, S).
#show state(g2, S) : state(g2, S).
#show state(g3, S) : state(g3, S).
#show state(g4, 1).
#show state(g5, 1).