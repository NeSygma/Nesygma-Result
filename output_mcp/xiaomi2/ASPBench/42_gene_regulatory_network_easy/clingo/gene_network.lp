% ============================================
% Boolean Gene Regulatory Network - Steady States
% ============================================

% Domain: Genes
gene(g1). gene(g2). gene(g3). gene(g4). gene(g5).

% Domain: States (0 = inactive, 1 = active)
state(0). state(1).

% Choice: Assign each gene a current state (0 or 1)
1 { current_state(G, S) : state(S) } 1 :- gene(G).

% ============================================
% Regulatory Rules: Define next_state for each gene
% ============================================

% g1 is active IFF g2 is not active
% g1_next = 1 if g2_current = 0, else g1_next = 0
next_state(g1, 1) :- current_state(g2, 0).
next_state(g1, 0) :- current_state(g2, 1).

% g2 is active IFF g1 is not active
% g2_next = 1 if g1_current = 0, else g2_next = 0
next_state(g2, 1) :- current_state(g1, 0).
next_state(g2, 0) :- current_state(g1, 1).

% g3 is active IFF (g4 is active AND g5 is active)
% g3_next = 1 if g4_current = 1 AND g5_current = 1, else g3_next = 0
next_state(g3, 1) :- current_state(g4, 1), current_state(g5, 1).
next_state(g3, 0) :- current_state(g4, 0).
next_state(g3, 0) :- current_state(g5, 0).

% g4 is always active (constitutive expression)
next_state(g4, 1).
% g4 can never be 0 as next state
% (no rule produces next_state(g4, 0))

% g5 is always active (constitutive expression)
next_state(g5, 1).
% g5 can never be 0 as next state
% (no rule produces next_state(g5, 0))

% ============================================
% Steady State Constraint
% A state is steady if current_state = next_state for ALL genes
% ============================================

% Forbid any gene where current state != next state
:- current_state(G, S1), next_state(G, S2), S1 != S2.

% ============================================
% Output: Show the steady states
% ============================================

#show current_state/2.