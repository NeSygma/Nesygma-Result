% Define the genes
 gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

% Define the possible states (0 or 1)
state(0..1).

% Choice rule: assign a state to each gene
{ state(G, S) : state(S) } = 1 :- gene(G).

% Helper: count active genes in Module 1
active_m1(N) :-
    N = #count { G : gene(G), G = m1_g1, state(G, 1);
                 G : gene(G), G = m1_g2, state(G, 1);
                 G : gene(G), G = m1_g3, state(G, 1) }.

% Helper: count active genes in Module 2
active_m2(N) :-
    N = #count { G : gene(G), G = m2_g1, state(G, 1);
                 G : gene(G), G = m2_g2, state(G, 1);
                 G : gene(G), G = m2_g3, state(G, 1) }.

% Master regulator rule: active iff active_m1 = active_m2
:- state(master_reg, 1), active_m1(N1), active_m2(N2), N1 != N2.
:- state(master_reg, 0), active_m1(N1), active_m2(N2), N1 == N2.

% Module 1 rules
% m1_g3 is constitutively active
:- state(m1_g3, 0).

% If master_reg is inactive (0)
% m1_g1 active iff m1_g2 inactive
:- state(master_reg, 0),
   state(m1_g1, 1), state(m1_g2, 1).
:- state(master_reg, 0),
   state(m1_g1, 0), state(m1_g2, 0).

% m1_g2 active iff m1_g3 inactive (but m1_g3 is always active, so m1_g2 must be inactive)
:- state(master_reg, 0),
   state(m1_g2, 1).

% If master_reg is active (1), all Module 1 genes are inactive
:- state(master_reg, 1),
   state(m1_g1, 1).
:- state(master_reg, 1),
   state(m1_g2, 1).
:- state(master_reg, 1),
   state(m1_g3, 1).

% Module 2 rules
% If master_reg is inactive (0)
% m2_g1 active iff both m1_g1 and m1_g2 are inactive
:- state(master_reg, 0),
   state(m2_g1, 1), state(m1_g1, 1).
:- state(master_reg, 0),
   state(m2_g1, 1), state(m1_g2, 1).
:- state(master_reg, 0),
   state(m2_g1, 0),
   state(m1_g1, 0),
   state(m1_g2, 0).

% m2_g2 active iff exactly 2 genes in Module 1 are active
% Since m1_g3 is always active, active_m1 can only be 1 or 2 or 3
% But m1_g2 is always inactive when master_reg is inactive, so active_m1 is 1 (only m1_g3) or 2 (m1_g1 and m1_g3)
:- state(master_reg, 0),
   state(m2_g2, 1), active_m1(1).
:- state(master_reg, 0),
   state(m2_g2, 1), active_m1(3).
:- state(master_reg, 0),
   state(m2_g2, 0), active_m1(2).

% m2_g3 active iff m2_g1 active AND m2_g2 inactive
:- state(master_reg, 0),
   state(m2_g3, 1), state(m2_g1, 0).
:- state(master_reg, 0),
   state(m2_g3, 1), state(m2_g2, 1).
:- state(master_reg, 0),
   state(m2_g3, 0),
   state(m2_g1, 1),
   state(m2_g2, 0).

% If master_reg is active (1), Module 2 forms a repressive ring oscillator (no steady state)
% So we forbid any state where master_reg=1 because the ring oscillator has no steady state
:- state(master_reg, 1).

% Reporter rule: active iff at least 2 of the 3 Module 2 genes are inactive
inactive_m2(N) :-
    N = #count { G : gene(G), G = m2_g1, state(G, 0);
                 G : gene(G), G = m2_g2, state(G, 0);
                 G : gene(G), G = m2_g3, state(G, 0) }.
:- state(reporter, 1), inactive_m2(N), N < 2.
:- state(reporter, 0), inactive_m2(N), N >= 2.

% Show the steady states
#show state/2.