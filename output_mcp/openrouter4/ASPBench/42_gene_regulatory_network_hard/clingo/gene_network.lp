% Genes
gene(master_reg; m1_g1; m1_g2; m1_g3; m2_g1; m2_g2; m2_g3; reporter).
m1_gene(m1_g1; m1_g2; m1_g3).
m2_gene(m2_g1; m2_g2; m2_g3).

% Each gene is either active (1) or inactive (0)
{ active(G) } :- gene(G).
inactive(G) :- gene(G), not active(G).

% ---- Helper counts ----
% Count active genes in Module 1
m1_active_count(C) :- C = #count { G : m1_gene(G), active(G) }.
% Count inactive genes in Module 2 (for reporter rule)
m2_inactive_count(C) :- C = #count { G : m2_gene(G), inactive(G) }.

% ============================================================
% RULE 1: Master Regulator
% master_reg is active iff #active(M1) == #active(M2)
% ============================================================
m2_active_count(C) :- C = #count { G : m2_gene(G), active(G) }.

% If counts equal, master_reg must be active; if not equal, must be inactive
:- active(master_reg), m1_active_count(C1), m2_active_count(C2), C1 != C2.
:- not active(master_reg), m1_active_count(C1), m2_active_count(C2), C1 = C2.

% ============================================================
% RULE 2: Module 1 Conditional Rules
% ============================================================

% Case: master_reg is ACTIVE → all Module 1 genes are inactive
:- active(master_reg), active(G), m1_gene(G).

% Case: master_reg is INACTIVE
% m1_g3 is constitutively active
:- not active(master_reg), not active(m1_g3).

% m1_g2 is active iff m1_g3 is inactive
:- not active(master_reg), active(m1_g2), active(m1_g3).
:- not active(master_reg), not active(m1_g3), not active(m1_g2).

% m1_g1 is active iff m1_g2 is inactive
:- not active(master_reg), active(m1_g1), active(m1_g2).
:- not active(master_reg), not active(m1_g2), not active(m1_g1).

% ============================================================
% RULE 3: Module 2 Conditional Rules
% ============================================================

% --- Sub-case: master_reg is INACTIVE ---

% m2_g1 is active iff (m1_g1 is inactive AND m1_g2 is inactive)
:- not active(master_reg), active(m2_g1), active(m1_g1).
:- not active(master_reg), active(m2_g1), active(m1_g2).
:- not active(master_reg), not active(m1_g1), not active(m1_g2), not active(m2_g1).

% m2_g2 is active iff exactly 2 genes in Module 1 are active
:- not active(master_reg), active(m2_g2), m1_active_count(C), C != 2.
:- not active(master_reg), m1_active_count(2), not active(m2_g2).

% m2_g3 is active iff (m2_g1 is active AND m2_g2 is inactive)
:- not active(master_reg), active(m2_g3), not active(m2_g1).
:- not active(master_reg), active(m2_g3), active(m2_g2).
:- not active(master_reg), active(m2_g1), not active(m2_g2), not active(m2_g3).

% --- Sub-case: master_reg is ACTIVE (Repressive Ring Oscillator) ---
% m2_g1 active iff m2_g2 inactive
:- active(master_reg), active(m2_g1), active(m2_g2).
:- active(master_reg), not active(m2_g1), not active(m2_g2).
% m2_g2 active iff m2_g3 inactive
:- active(master_reg), active(m2_g2), active(m2_g3).
:- active(master_reg), not active(m2_g2), not active(m2_g3).
% m2_g3 active iff m2_g1 inactive
:- active(master_reg), active(m2_g3), active(m2_g1).
:- active(master_reg), not active(m2_g3), not active(m2_g1).

% ============================================================
% RULE 4: Reporter Rule
% reporter is active iff majority (>=2) of Module 2 genes are inactive
% ============================================================
:- active(reporter), m2_inactive_count(C), C < 2.
:- m2_inactive_count(C), C >= 2, not active(reporter).

% ============================================================
% Show results
% ============================================================
#show active/1.