% Hierarchical Boolean Gene Regulatory Network - Steady States

% Define all genes
gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

% Module membership
module1(m1_g1). module1(m1_g2). module1(m1_g3).
module2(m2_g1). module2(m2_g2). module2(m2_g3).

% Each gene has exactly one state: 0 (inactive) or 1 (active)
{ state(G, 0) } 1 :- gene(G).
{ state(G, 1) } 1 :- gene(G).

% Compute active counts for each module
active_m1(N) :- N = #count{ G : module1(G), state(G, 1) }.
active_m2(N) :- N = #count{ G : module2(G), state(G, 1) }.

% 1. Master Regulator Rule: active iff #active in Module 1 = #active in Module 2
state(master_reg, 1) :- active_m1(N), active_m2(N).
state(master_reg, 0) :- active_m1(N1), active_m2(N2), N1 != N2.

% 2. Module 1 Conditional Rules
% If master_reg is inactive (0):
state(m1_g3, 1) :- state(master_reg, 0).  % constitutively active
state(m1_g2, 0) :- state(master_reg, 0), state(m1_g3, 1).  % m1_g2 active iff m1_g3 inactive
state(m1_g1, 1) :- state(master_reg, 0), state(m1_g2, 0).  % m1_g1 active iff m1_g2 inactive
state(m1_g1, 0) :- state(master_reg, 0), state(m1_g2, 1).  % (complement)

% If master_reg is active (1):
state(m1_g1, 0) :- state(master_reg, 1).
state(m1_g2, 0) :- state(master_reg, 1).
state(m1_g3, 0) :- state(master_reg, 1).

% 3. Module 2 Conditional Rules
% If master_reg is inactive (0):
state(m2_g1, 1) :- state(master_reg, 0), state(m1_g1, 0), state(m1_g2, 0).
state(m2_g1, 0) :- state(master_reg, 0), state(m1_g1, 1).
state(m2_g1, 0) :- state(master_reg, 0), state(m1_g2, 1).

state(m2_g2, 1) :- state(master_reg, 0), active_m1(2).
state(m2_g2, 0) :- state(master_reg, 0), active_m1(N), N != 2.

state(m2_g3, 1) :- state(master_reg, 0), state(m2_g1, 1), state(m2_g2, 0).
state(m2_g3, 0) :- state(master_reg, 0), state(m2_g1, 0).
state(m2_g3, 0) :- state(master_reg, 0), state(m2_g2, 1).

% If master_reg is active (1): repressive ring oscillator (no steady state)
state(m2_g1, 1) :- state(master_reg, 1), state(m2_g2, 0).
state(m2_g1, 0) :- state(master_reg, 1), state(m2_g2, 1).

state(m2_g2, 1) :- state(master_reg, 1), state(m2_g3, 0).
state(m2_g2, 0) :- state(master_reg, 1), state(m2_g3, 1).

state(m2_g3, 1) :- state(master_reg, 1), state(m2_g1, 0).
state(m2_g3, 0) :- state(master_reg, 1), state(m2_g1, 1).

% 4. Reporter Rule: active iff at least 2 of Module 2 genes are inactive
inactive_m2(N) :- N = #count{ G : module2(G), state(G, 0) }.
state(reporter, 1) :- inactive_m2(N), N >= 2.
state(reporter, 0) :- inactive_m2(N), N < 2.

% Show all gene states in steady states
#show state/2.