% ============================================
% Hierarchical Boolean Gene Regulatory Network
% Finding all steady states (fixed points)
% ============================================

% --- Domain: All Genes ---
gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

% Module groupings
module1(m1_g1). module1(m1_g2). module1(m1_g3).
module2(m2_g1). module2(m2_g2). module2(m2_g3).

% --- Choice: Each gene is either active or inactive ---
{active(G)} :- gene(G).
inactive(G) :- gene(G), not active(G).

% --- Helper: Count active genes in each module ---
count_m1(N) :- N = #count{G : module1(G), active(G)}.
count_m2(N) :- N = #count{G : module2(G), active(G)}.

% --- Helper: Module 1 active gene counts for specific conditions ---
m1_active_count(N) :- N = #count{G : module1(G), active(G)}.
m1_inactive_count(N) :- N = #count{G : module1(G), inactive(G)}.

% Helper: number of inactive genes in module 2
m2_inactive_count(N) :- N = #count{G : module2(G), inactive(G)}.

% ============================================
% CONSTRAINT 1: Master Regulator Rule
% master_reg active IFF count_m1 == count_m2
% ============================================

% If master_reg is active, then counts must be equal
:- active(master_reg), count_m1(N1), count_m2(N2), N1 != N2.

% If counts are equal, master_reg must be active
:- not active(master_reg), count_m1(N1), count_m2(N2), N1 == N2.

% ============================================
% CONSTRAINT 2: Module 1 Conditional Rules
% ============================================

% --- When master_reg is INACTIVE ---

% m1_g1 active IFF m1_g2 inactive
:- active(master_reg) == 0, active(m1_g1), active(m1_g2).
:- active(master_reg) == 0, inactive(m1_g1), inactive(m1_g2).

% m1_g2 active IFF m1_g3 inactive
:- active(master_reg) == 0, active(m1_g2), active(m1_g3).
:- active(master_reg) == 0, inactive(m1_g2), inactive(m1_g3).

% m1_g3 constitutively active when master_reg inactive
:- active(master_reg) == 0, inactive(m1_g3).

% --- When master_reg is ACTIVE ---
% All Module 1 genes inactive
:- active(master_reg), active(m1_g1).
:- active(master_reg), active(m1_g2).
:- active(master_reg), active(m1_g3).

% ============================================
% CONSTRAINT 3: Module 2 Conditional Rules
% ============================================

% --- When master_reg is INACTIVE ---

% m2_g1 active IFF both m1_g1 and m1_g2 are inactive
:- active(master_reg) == 0, active(m2_g1), active(m1_g1).
:- active(master_reg) == 0, active(m2_g1), active(m1_g2).
:- active(master_reg) == 0, inactive(m2_g1), inactive(m1_g1), inactive(m1_g2).

% m2_g2 active IFF exactly 2 genes in Module 1 are active
:- active(master_reg) == 0, active(m2_g2), m1_active_count(N), N != 2.
:- active(master_reg) == 0, inactive(m2_g2), m1_active_count(N), N == 2.

% m2_g3 active IFF m2_g1 active AND m2_g2 inactive
:- active(master_reg) == 0, active(m2_g3), inactive(m2_g1).
:- active(master_reg) == 0, active(m2_g3), active(m2_g2).
:- active(master_reg) == 0, inactive(m2_g3), active(m2_g1), inactive(m2_g2).

% --- When master_reg is ACTIVE ---
% Repressive ring oscillator: NO steady state possible
% m2_g1 active IFF m2_g2 inactive
:- active(master_reg), active(m2_g1), active(m2_g2).
:- active(master_reg), inactive(m2_g1), inactive(m2_g2).

% m2_g2 active IFF m2_g3 inactive
:- active(master_reg), active(m2_g2), active(m2_g3).
:- active(master_reg), inactive(m2_g2), inactive(m2_g3).

% m2_g3 active IFF m2_g1 inactive
:- active(master_reg), active(m2_g3), active(m2_g1).
:- active(master_reg), inactive(m2_g3), inactive(m2_g1).

% ============================================
% CONSTRAINT 4: Reporter Rule
% reporter active IFF majority of Module 2 inactive (>=2 of 3)
% ============================================

:- active(reporter), m2_inactive_count(N), N < 2.
:- inactive(reporter), m2_inactive_count(N), N >= 2.

% ============================================
% Output: Show all gene states
% ============================================
#show active/1.
#show inactive/1.