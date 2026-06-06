% Gene Regulatory Network - Steady States Analysis

% Domain: Genes
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).

% Each gene can be either active (1) or inactive (0)
{ active(G) } :- gene(G).

% Regulatory Rules (as constraints)
% Rule 1: g1 is active IF AND ONLY IF g2 is not active
:- active(g1), active(g2).  % Can't both be active
:- not active(g1), not active(g2).  % Can't both be inactive

% Rule 2: g2 is active IF AND ONLY IF g1 is not active (same as rule 1, already covered)

% Rule 3: g3 is active IF AND ONLY IF (g4 is active AND g5 is active)
:- active(g3), not active(g4).  % g3 active requires g4 active
:- active(g3), not active(g5).  % g3 active requires g5 active
:- not active(g3), active(g4), active(g5).  % g3 inactive when both g4 and g5 are active

% Rule 4: g4 is ALWAYS active
:- not active(g4).

% Rule 5: g5 is ALWAYS active  
:- not active(g5).

% Helper to show the complete state as 0/1 values
state(g1, 1) :- active(g1).
state(g1, 0) :- not active(g1).
state(g2, 1) :- active(g2).
state(g2, 0) :- not active(g2).
state(g3, 1) :- active(g3).
state(g3, 0) :- not active(g3).
state(g4, 1) :- active(g4).
state(g4, 0) :- not active(g4).
state(g5, 1) :- active(g5).
state(g5, 0) :- not active(g5).

% Show the steady state
#show active/1.
#show state/2.