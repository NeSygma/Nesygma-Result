% Genes
gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

gene_m1(m1_g1). gene_m1(m1_g2). gene_m1(m1_g3).
gene_m2(m2_g1). gene_m2(m2_g2). gene_m2(m2_g3).

% Choice: Each gene is either active (1) or inactive (0)
{ state(G, 0); state(G, 1) } = 1 :- gene(G).

active(G) :- state(G, 1).
inactive(G) :- state(G, 0).

% Counts
count_m1(N) :- N = #count { G : gene_m1(G), active(G) }.
count_m2(N) :- N = #count { G : gene_m2(G), active(G) }.
count_m2_inactive(N) :- N = #count { G : gene_m2(G), inactive(G) }.

% Rule 1: Master Regulator
active(master_reg) :- count_m1(N1), count_m2(N2), N1 == N2.
inactive(master_reg) :- count_m1(N1), count_m2(N2), N1 != N2.

% Rule 2: Module 1
active(m1_g1) :- inactive(master_reg), inactive(m1_g2).
inactive(m1_g1) :- inactive(master_reg), active(m1_g2).
active(m1_g2) :- inactive(master_reg), inactive(m1_g3).
inactive(m1_g2) :- inactive(master_reg), active(m1_g3).
active(m1_g3) :- inactive(master_reg).
inactive(m1_g1) :- active(master_reg).
inactive(m1_g2) :- active(master_reg).
inactive(m1_g3) :- active(master_reg).

% Rule 3: Module 2
% If master_reg inactive:
% m2_g1 active iff m1_g1, m1_g2 both inactive
m1_both_inactive :- inactive(m1_g1), inactive(m1_g2).
active(m2_g1) :- inactive(master_reg), m1_both_inactive.
inactive(m2_g1) :- inactive(master_reg), not m1_both_inactive.

% m2_g2 active iff count_m1 == 2
active(m2_g2) :- inactive(master_reg), count_m1(2).
inactive(m2_g2) :- inactive(master_reg), not count_m1(2).

% m2_g3 active iff m2_g1 active AND m2_g2 inactive
m2_g1_active_g2_inactive :- active(m2_g1), inactive(m2_g2).
active(m2_g3) :- inactive(master_reg), m2_g1_active_g2_inactive.
inactive(m2_g3) :- inactive(master_reg), not m2_g1_active_g2_inactive.

% If master_reg active:
% Repressive ring
active(m2_g1) :- active(master_reg), inactive(m2_g2).
inactive(m2_g1) :- active(master_reg), active(m2_g2).
active(m2_g2) :- active(master_reg), inactive(m2_g3).
inactive(m2_g2) :- active(master_reg), active(m2_g3).
active(m2_g3) :- active(master_reg), inactive(m2_g1).
inactive(m2_g3) :- active(master_reg), active(m2_g1).

% Rule 4: Reporter
active(reporter) :- count_m2_inactive(N), N >= 2.
inactive(reporter) :- count_m2_inactive(N), N < 2.

#show state/2.