% Genes
gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

% Module membership
module1(m1_g1). module1(m1_g2). module1(m1_g3).
module2(m2_g1). module2(m2_g2). module2(m2_g3).

% Choice of activity for each gene (each gene may be active or not)
{ active(G) } :- gene(G).

% Count active genes in modules
cnt1(N) :- N = #count { G : active(G), module1(G) }.
cnt2(N) :- N = #count { G : active(G), module2(G) }.

% Master regulator equivalence: active iff cnt1 == cnt2
active(master_reg) :- cnt1(N), cnt2(N).
:- active(master_reg), cnt1(N1), cnt2(N2), N1 != N2.
:- not active(master_reg), cnt1(N), cnt2(N).

% Module 1 rules when master is inactive
% Constitutive activation of m1_g3 when master inactive
active(m1_g3) :- not active(master_reg).
% When master active, all module1 genes must be inactive
:- active(master_reg), active(m1_g1).
:- active(master_reg), active(m1_g2).
:- active(master_reg), active(m1_g3).
% Equivalence m1_g1 <-> not m1_g2 (only when master inactive)
:- not active(master_reg), active(m1_g1), active(m1_g2).
:- not active(master_reg), not active(m1_g1), not active(m1_g2).
% Equivalence m1_g2 <-> not m1_g3 (only when master inactive)
:- not active(master_reg), active(m1_g2), active(m1_g3).
:- not active(master_reg), not active(m1_g2), not active(m1_g3).

% Module 2 rules when master is inactive
% m2_g1 <-> (not m1_g1 and not m1_g2)
active(m2_g1) :- not active(master_reg), not active(m1_g1), not active(m1_g2).
:- not active(master_reg), active(m2_g1), active(m1_g1).
:- not active(master_reg), active(m2_g1), active(m2_g1), active(m1_g2). % duplicate but ensures both
:- not active(master_reg), not active(m2_g1), not active(m1_g1), not active(m1_g2).
% m2_g2 <-> exactly 2 active in Module1
active(m2_g2) :- not active(master_reg), cnt1(2).
:- not active(master_reg), active(m2_g2), cnt1(N), N != 2.
:- not active(master_reg), not active(m2_g2), cnt1(2).
% m2_g3 <-> (m2_g1 active and m2_g2 inactive)
active(m2_g3) :- not active(master_reg), active(m2_g1), not active(m2_g2).
:- not active(master_reg), active(m2_g3), not active(m2_g1).
:- not active(master_reg), active(m2_g3), active(m2_g2).
:- not active(master_reg), not active(m2_g3), active(m2_g1), not active(m2_g2).

% Module 2 rules when master is active (repressive ring)
% m2_g1 <-> not m2_g2
active(m2_g1) :- active(master_reg), not active(m2_g2).
:- active(master_reg), active(m2_g1), active(m2_g2).
:- active(master_reg), not active(m2_g1), not active(m2_g2).
% m2_g2 <-> not m2_g3
active(m2_g2) :- active(master_reg), not active(m2_g3).
:- active(master_reg), active(m2_g2), active(m2_g3).
:- active(master_reg), not active(m2_g2), not active(m2_g3).
% m2_g3 <-> not m2_g1
active(m2_g3) :- active(master_reg), not active(m2_g1).
:- active(master_reg), active(m2_g3), active(m2_g1).
:- active(master_reg), not active(m2_g3), not active(m2_g1).

% Reporter rule: active iff at most 1 active in Module2 (majority inactive)
active(reporter) :- cnt2(N), N <= 1.
:- active(reporter), cnt2(N), N > 1.
:- not active(reporter), cnt2(N), N <= 1.

#show active/1.