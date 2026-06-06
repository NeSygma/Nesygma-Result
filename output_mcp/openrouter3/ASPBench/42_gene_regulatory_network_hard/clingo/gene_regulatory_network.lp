% Hierarchical Boolean Gene Regulatory Network - Steady State Analysis

% Define all genes
gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

% States are binary (0 or 1)
state(0). state(1).

% Choice rule: Each gene can be active (1) or inactive (0)
{ active(G) } :- gene(G).

% Helper: inactive genes
inactive(G) :- gene(G), not active(G).

% Count active genes in each module
active_m1_count(N) :- N = #count{ G : active(G), module1(G) }.
active_m2_count(N) :- N = #count{ G : active(G), module2(G) }.

% Module membership
module1(m1_g1). module1(m1_g2). module1(m1_g3).
module2(m2_g1). module2(m2_g2). module2(m2_g3).

% ===== MASTER REGULATOR RULE =====
% master_reg is active iff #active in Module 1 = #active in Module 2
active(master_reg) :- active_m1_count(N1), active_m2_count(N2), N1 = N2.
inactive(master_reg) :- active_m1_count(N1), active_m2_count(N2), N1 != N2.

% ===== MODULE 1 RULES =====
% If master_reg is inactive:
%   m1_g1 active iff m1_g2 inactive
%   m1_g2 active iff m1_g3 inactive
%   m1_g3 is constitutively active (always 1)
% If master_reg is active:
%   All Module 1 genes are inactive

% m1_g3 is always active when master_reg is inactive
active(m1_g3) :- inactive(master_reg).
% m1_g3 is inactive when master_reg is active
inactive(m1_g3) :- active(master_reg).

% m1_g1 active iff m1_g2 inactive (when master_reg inactive)
active(m1_g1) :- inactive(master_reg), inactive(m1_g2).
inactive(m1_g1) :- inactive(master_reg), active(m1_g2).
% m1_g1 inactive when master_reg active
inactive(m1_g1) :- active(master_reg).

% m1_g2 active iff m1_g3 inactive (when master_reg inactive)
% But m1_g3 is always active when master_reg inactive, so m1_g2 must be inactive
active(m1_g2) :- inactive(master_reg), inactive(m1_g3).
inactive(m1_g2) :- inactive(master_reg), active(m1_g3).
% m1_g2 inactive when master_reg active
inactive(m1_g2) :- active(master_reg).

% ===== MODULE 2 RULES =====
% If master_reg is inactive:
%   m2_g1 active iff both m1_g1 and m1_g2 are inactive
%   m2_g2 active iff exactly 2 genes in Module 1 are active
%   m2_g3 active iff m2_g1 active AND m2_g2 inactive
% If master_reg is active:
%   Repressive ring oscillator (no steady state possible)

% Count active genes in Module 1
active_m1_genes(N) :- N = #count{ G : active(G), module1(G) }.

% When master_reg is inactive:
% m2_g1 active iff both m1_g1 and m1_g2 are inactive
active(m2_g1) :- inactive(master_reg), inactive(m1_g1), inactive(m1_g2).
inactive(m2_g1) :- inactive(master_reg), (active(m1_g1); active(m1_g2)).

% m2_g2 active iff exactly 2 genes in Module 1 are active
active(m2_g2) :- inactive(master_reg), active_m1_genes(2).
inactive(m2_g2) :- inactive(master_reg), active_m1_genes(N), N != 2.

% m2_g3 active iff m2_g1 active AND m2_g2 inactive
active(m2_g3) :- inactive(master_reg), active(m2_g1), inactive(m2_g2).
inactive(m2_g3) :- inactive(master_reg), (inactive(m2_g1); active(m2_g2)).

% When master_reg is active:
% Repressive ring: m2_g1 active iff m2_g2 inactive, etc.
% This creates a cycle with no steady state, so we must forbid master_reg active
% Actually, let's model it properly and see if any steady state exists

% For repressive ring when master_reg active:
% m2_g1 active iff m2_g2 inactive
active(m2_g1) :- active(master_reg), inactive(m2_g2).
inactive(m2_g1) :- active(master_reg), active(m2_g2).

% m2_g2 active iff m2_g3 inactive
active(m2_g2) :- active(master_reg), inactive(m2_g3).
inactive(m2_g2) :- active(master_reg), active(m2_g3).

% m2_g3 active iff m2_g1 inactive
active(m2_g3) :- active(master_reg), inactive(m2_g1).
inactive(m2_g3) :- active(master_reg), active(m2_g1).

% ===== REPORTER RULE =====
% reporter active iff at least 2 of 3 Module 2 genes are inactive
inactive_m2_count(N) :- N = #count{ G : inactive(G), module2(G) }.
active(reporter) :- inactive_m2_count(N), N >= 2.
inactive(reporter) :- inactive_m2_count(N), N < 2.

% ===== STEADY STATE CONSTRAINT =====
% For each gene, the state must be consistent (no change after one time step)
% This is already enforced by our rules above since we're deriving states directly

% Additional constraint: The repressive ring when master_reg active has no steady state
% Let's check if any assignment satisfies the ring constraints
% If master_reg is active, we have:
% m2_g1 = NOT m2_g2
% m2_g2 = NOT m2_g3  
% m2_g3 = NOT m2_g1
% This implies: m2_g1 = NOT (NOT m2_g1) = m2_g1, which is always true
% But also: m2_g1 = NOT m2_g2 = NOT (NOT m2_g3) = m2_g3 = NOT m2_g1
% So m2_g1 = NOT m2_g1, which is impossible for binary values
% Therefore, master_reg cannot be active in a steady state

% Force master_reg to be inactive to avoid the impossible ring
:- active(master_reg).

% Show all active genes in the steady state
#show active/1.
#show inactive/1.