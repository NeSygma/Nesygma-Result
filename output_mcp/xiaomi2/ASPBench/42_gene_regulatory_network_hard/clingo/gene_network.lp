% =============================================
% Hierarchical Boolean Gene Regulatory Network
% Finding all steady states (fixed points)
% =============================================

% --- Domain: Genes ---
gene(master_reg).
gene(m1_g1). gene(m1_g2). gene(m1_g3).
gene(m2_g1). gene(m2_g2). gene(m2_g3).
gene(reporter).

% --- Module membership ---
module1(m1_g1). module1(m1_g2). module1(m1_g3).
module2(m2_g1). module2(m2_g2). module2(m2_g3).

% --- Choice: each gene can be active (1) or inactive (0) ---
{active(G)} :- gene(G).

% --- Helper: count active genes in each module ---
m1_count(N) :- N = #count{G : module1(G), active(G)}.
m2_count(N) :- N = #count{G : module2(G), active(G)}.

% --- Helper: module counts are equal ---
counts_eq :- m1_count(N), m2_count(N).

% =============================================
% Rule 1: Master Regulator
% master_reg active <-> count_m1 = count_m2
% =============================================
:- active(master_reg), not counts_eq.
:- not active(master_reg), counts_eq.

% =============================================
% Rule 2: Module 1 Conditional Rules
% =============================================

% --- When master_reg is INACTIVE ---
% m1_g1 active <-> m1_g2 inactive
:- not active(master_reg), active(m1_g1), active(m1_g2).
:- not active(master_reg), not active(m1_g1), not active(m1_g2).

% m1_g2 active <-> m1_g3 inactive
:- not active(master_reg), active(m1_g2), active(m1_g3).
:- not active(master_reg), not active(m1_g2), not active(m1_g3).

% m1_g3 constitutively active (always 1)
:- not active(master_reg), not active(m1_g3).

% --- When master_reg is ACTIVE ---
% All Module 1 genes inactive
:- active(master_reg), active(m1_g1).
:- active(master_reg), active(m1_g2).
:- active(master_reg), active(m1_g3).

% =============================================
% Rule 3: Module 2 Conditional Rules
% =============================================

% --- When master_reg is INACTIVE ---

% m2_g1 active <-> (m1_g1 inactive AND m1_g2 inactive)
:- not active(master_reg), active(m2_g1), active(m1_g1).
:- not active(master_reg), active(m2_g1), active(m1_g2).
:- not active(master_reg), not active(m2_g1), not active(m1_g1), not active(m1_g2).

% m2_g2 active <-> exactly 2 genes in Module 1 are active
:- not active(master_reg), active(m2_g2), m1_count(N), N != 2.
:- not active(master_reg), not active(m2_g2), m1_count(2).

% m2_g3 active <-> (m2_g1 active AND m2_g2 inactive)
:- not active(master_reg), active(m2_g3), not active(m2_g1).
:- not active(master_reg), active(m2_g3), active(m2_g2).
:- not active(master_reg), not active(m2_g3), active(m2_g1), not active(m2_g2).

% --- When master_reg is ACTIVE (ring oscillator - no steady state) ---

% m2_g1 active <-> m2_g2 inactive
:- active(master_reg), active(m2_g1), active(m2_g2).
:- active(master_reg), not active(m2_g1), not active(m2_g2).

% m2_g2 active <-> m2_g3 inactive
:- active(master_reg), active(m2_g2), active(m2_g3).
:- active(master_reg), not active(m2_g2), not active(m2_g3).

% m2_g3 active <-> m2_g1 inactive
:- active(master_reg), active(m2_g3), active(m2_g1).
:- active(master_reg), not active(m2_g3), not active(m2_g1).

% =============================================
% Rule 4: Reporter
% reporter active <-> majority of Module 2 inactive (>=2 of 3 inactive, i.e., <=1 active)
% =============================================
:- active(reporter), m2_count(N), N > 1.
:- not active(reporter), m2_count(N), N <= 1.

% =============================================
% Display results
% =============================================
#show active/1.