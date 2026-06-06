% Define all genes
all_genes(master_reg).
all_genes(m1_g1). all_genes(m1_g2). all_genes(m1_g3).
all_genes(m2_g1). all_genes(m2_g2). all_genes(m2_g3).
all_genes(reporter).

% Define modules
module1(m1_g1). module1(m1_g2). module1(m1_g3).
module2(m2_g1). module2(m2_g2). module2(m2_g3).

% Active/Inactive definitions
inactive(G) :- all_genes(G), not active(G).

% Count active genes in Module 1 and Module 2
count_active_module1(N) :- N = #count { G : module1(G), active(G) }.
count_active_module2(N) :- N = #count { G : module2(G), active(G) }.

% Master Regulator Rule: active(master_reg) iff count_active_module1 == count_active_module2
active(master_reg) :- count_active_module1(N), count_active_module2(N).
:- active(master_reg), count_active_module1(N1), count_active_module2(N2), N1 != N2.
:- inactive(master_reg), count_active_module1(N1), count_active_module2(N2), N1 == N2.

% Module 1 Rules
% If master_reg is inactive
active(m1_g3).

active(m1_g1) :- inactive(m1_g2).
inactive(m1_g1) :- active(m1_g2).
active(m1_g2) :- inactive(m1_g3).
inactive(m1_g2) :- active(m1_g3).

% If master_reg is active: all Module 1 genes are inactive
inactive(m1_g1) :- active(master_reg).
inactive(m1_g2) :- active(master_reg).
inactive(m1_g3) :- active(master_reg).

% Module 2 Rules
% If master_reg is inactive
active(m2_g1) :- inactive(m1_g1), inactive(m1_g2).
inactive(m2_g1) :- active(m1_g1).
inactive(m2_g1) :- active(m1_g2).

active(m2_g2) :- count_active_module1(2).
inactive(m2_g2) :- count_active_module1(N), N != 2.

active(m2_g3) :- active(m2_g1), inactive(m2_g2).
inactive(m2_g3) :- inactive(m2_g1).
inactive(m2_g3) :- active(m2_g2).

% If master_reg is active: repressive ring oscillator (no steady state)
:- active(master_reg), active(m2_g1), active(m2_g2).
:- active(master_reg), active(m2_g2), active(m2_g3).
:- active(master_reg), active(m2_g3), active(m2_g1).
:- active(master_reg), inactive(m2_g1), inactive(m2_g2), inactive(m2_g3).

% Reporter Rule
inactive_count_module2(N) :- N = #count { G : module2(G), inactive(G) }.
active(reporter) :- inactive_count_module2(N), N >= 2.
inactive(reporter) :- inactive_count_module2(N), N < 2.

% Choice rule: allow all genes to be active or inactive
{ active(G) : all_genes(G) }.

% Show all active/inactive states for all genes
#show active/1.
#show inactive/1.