% Gene Regulatory Network Steady States

% Domains
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).
value(0). value(1).
time(0). time(1).

% Choose state for g1, g2, g3 at time 0 (each exactly one value)
1 { state(G, V, 0) : value(V) } 1 :- gene(G), G != g4, G != g5.

% Constitutive genes: always active
state(g4, 1, 0).
state(g5, 1, 0).

% Update rules for next state (time 1) based on current state (time 0)

% g1 active iff g2 not active
state(g1, 1, 1) :- state(g2, 0, 0).
state(g1, 0, 1) :- state(g2, 1, 0).

% g2 active iff g1 not active (redundant but explicit)
state(g2, 1, 1) :- state(g1, 0, 0).
state(g2, 0, 1) :- state(g1, 1, 0).

% g3 active iff g4 active AND g5 active
state(g3, 1, 1) :- state(g4, 1, 0), state(g5, 1, 0).
state(g3, 0, 1) :- state(g4, 0, 0); state(g5, 0, 0).

% g4 and g5 always active: next state equals current state
state(g4, 1, 1) :- state(g4, 1, 0).
state(g5, 1, 1) :- state(g5, 1, 0).

% Steady state condition: state at time 0 equals state at time 1
:- gene(G), state(G, V0, 0), state(G, V1, 1), V0 != V1.

% Show the steady states (state at time 0)
#show state/3.