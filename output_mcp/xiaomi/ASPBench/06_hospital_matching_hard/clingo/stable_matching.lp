% ============================================
% Stable Matching: 40 Residents, 20 Hospitals
% ============================================

% ---- Residents ----
resident(r1). resident(r2). resident(r3). resident(r4).
resident(r5). resident(r6). resident(r7). resident(r8).
resident(r9). resident(r10). resident(r11). resident(r12).
resident(r13). resident(r14). resident(r15). resident(r16).
resident(r17). resident(r18). resident(r19). resident(r20).
resident(r21). resident(r22). resident(r23). resident(r24).
resident(r25). resident(r26). resident(r27). resident(r28).
resident(r29). resident(r30). resident(r31). resident(r32).
resident(r33). resident(r34). resident(r35). resident(r36).
resident(r37). resident(r38). resident(r39). resident(r40).

% ---- Hospitals ----
hospital(h1). hospital(h2). hospital(h3). hospital(h4).
hospital(h5). hospital(h6). hospital(h7). hospital(h8).
hospital(h9). hospital(h10). hospital(h11). hospital(h12).
hospital(h13). hospital(h14). hospital(h15). hospital(h16).
hospital(h17). hospital(h18). hospital(h19). hospital(h20).

% ---- Capacities ----
capacity(h1, 2). capacity(h2, 2). capacity(h3, 2). capacity(h4, 2).
capacity(h5, 2). capacity(h6, 2). capacity(h7, 4). capacity(h8, 3).
capacity(h9, 1). capacity(h10, 3). capacity(h11, 3). capacity(h12, 2).
capacity(h13, 3). capacity(h14, 3). capacity(h15, 2). capacity(h16, 2).
capacity(h17, 2). capacity(h18, 1). capacity(h19, 1). capacity(h20, 1).

% ---- Resident Preferences (rank 1 = most preferred) ----
% Block A1
r_pref(r1, h1, 1). r_pref(r1, h2, 2).
r_pref(r2, h1, 1). r_pref(r2, h2, 2).
r_pref(r3, h2, 1). r_pref(r3, h1, 2).
r_pref(r4, h2, 1). r_pref(r4, h1, 2).

% Block A2
r_pref(r5, h3, 1). r_pref(r5, h4, 2).
r_pref(r6, h3, 1). r_pref(r6, h4, 2).
r_pref(r7, h4, 1). r_pref(r7, h3, 2).
r_pref(r8, h4, 1). r_pref(r8, h3, 2).

% Block A3
r_pref(r9, h5, 1). r_pref(r9, h6, 2).
r_pref(r10, h5, 1). r_pref(r10, h6, 2).
r_pref(r11, h6, 1). r_pref(r11, h5, 2).
r_pref(r12, h6, 1). r_pref(r12, h5, 2).

% Block B1
r_pref(r13, h7, 1). r_pref(r13, h8, 2). r_pref(r13, h9, 3).
r_pref(r14, h7, 1). r_pref(r14, h8, 2). r_pref(r14, h9, 3).
r_pref(r15, h8, 1). r_pref(r15, h7, 2). r_pref(r15, h9, 3).
r_pref(r16, h8, 1). r_pref(r16, h7, 2). r_pref(r16, h9, 3).
r_pref(r17, h7, 1). r_pref(r17, h8, 2). r_pref(r17, h9, 3).
r_pref(r18, h7, 1). r_pref(r18, h9, 2). r_pref(r18, h8, 3).
r_pref(r19, h8, 1). r_pref(r19, h9, 2). r_pref(r19, h7, 3).
r_pref(r20, h9, 1). r_pref(r20, h8, 2). r_pref(r20, h7, 3).

% Block B2
r_pref(r21, h10, 1). r_pref(r21, h11, 2). r_pref(r21, h12, 3).
r_pref(r22, h10, 1). r_pref(r22, h12, 2). r_pref(r22, h11, 3).
r_pref(r23, h11, 1). r_pref(r23, h10, 2). r_pref(r23, h12, 3).
r_pref(r24, h11, 1). r_pref(r24, h12, 2). r_pref(r24, h10, 3).
r_pref(r25, h10, 1). r_pref(r25, h11, 2). r_pref(r25, h12, 3).
r_pref(r26, h11, 1). r_pref(r26, h10, 2). r_pref(r26, h12, 3).
r_pref(r27, h12, 1). r_pref(r27, h11, 2). r_pref(r27, h10, 3).
r_pref(r28, h12, 1). r_pref(r28, h10, 2). r_pref(r28, h11, 3).

% Block B3
r_pref(r29, h13, 1). r_pref(r29, h14, 2). r_pref(r29, h15, 3).
r_pref(r30, h13, 1). r_pref(r30, h15, 2). r_pref(r30, h14, 3).
r_pref(r31, h14, 1). r_pref(r31, h13, 2). r_pref(r31, h15, 3).
r_pref(r32, h14, 1). r_pref(r32, h15, 2). r_pref(r32, h13, 3).
r_pref(r33, h13, 1). r_pref(r33, h14, 2). r_pref(r33, h15, 3).
r_pref(r34, h14, 1). r_pref(r34, h13, 2). r_pref(r34, h15, 3).
r_pref(r35, h15, 1). r_pref(r35, h14, 2). r_pref(r35, h13, 3).
r_pref(r36, h15, 1). r_pref(r36, h13, 2). r_pref(r36, h14, 3).

% Block A4
r_pref(r37, h16, 1). r_pref(r37, h17, 2).
r_pref(r38, h16, 1). r_pref(r38, h17, 2).
r_pref(r39, h17, 1). r_pref(r39, h16, 2).
r_pref(r40, h17, 1). r_pref(r40, h16, 2).

% ---- Hospital Preferences ----
% Block A1
h_pref(h1, r3, 1). h_pref(h1, r4, 2). h_pref(h1, r1, 3). h_pref(h1, r2, 4).
h_pref(h2, r1, 1). h_pref(h2, r2, 2). h_pref(h2, r3, 3). h_pref(h2, r4, 4).

% Block A2
h_pref(h3, r7, 1). h_pref(h3, r8, 2). h_pref(h3, r5, 3). h_pref(h3, r6, 4).
h_pref(h4, r5, 1). h_pref(h4, r6, 2). h_pref(h4, r7, 3). h_pref(h4, r8, 4).

% Block A3
h_pref(h5, r11, 1). h_pref(h5, r12, 2). h_pref(h5, r9, 3). h_pref(h5, r10, 4).
h_pref(h6, r9, 1). h_pref(h6, r10, 2). h_pref(h6, r11, 3). h_pref(h6, r12, 4).

% Block B1
h_pref(h7, r13, 1). h_pref(h7, r14, 2). h_pref(h7, r17, 3). h_pref(h7, r18, 4).
h_pref(h7, r15, 5). h_pref(h7, r16, 6). h_pref(h7, r19, 7). h_pref(h7, r20, 8).
h_pref(h8, r15, 1). h_pref(h8, r16, 2). h_pref(h8, r19, 3). h_pref(h8, r13, 4).
h_pref(h8, r14, 5). h_pref(h8, r17, 6). h_pref(h8, r18, 7). h_pref(h8, r20, 8).
h_pref(h9, r20, 1). h_pref(h9, r19, 2). h_pref(h9, r18, 3). h_pref(h9, r17, 4).
h_pref(h9, r16, 5). h_pref(h9, r15, 6). h_pref(h9, r14, 7). h_pref(h9, r13, 8).

% Block B2
h_pref(h10, r21, 1). h_pref(h10, r22, 2). h_pref(h10, r25, 3). h_pref(h10, r23, 4).
h_pref(h10, r24, 5). h_pref(h10, r26, 6). h_pref(h10, r27, 7). h_pref(h10, r28, 8).
h_pref(h11, r23, 1). h_pref(h11, r24, 2). h_pref(h11, r26, 3). h_pref(h11, r21, 4).
h_pref(h11, r22, 5). h_pref(h11, r25, 6). h_pref(h11, r27, 7). h_pref(h11, r28, 8).
h_pref(h12, r27, 1). h_pref(h12, r28, 2). h_pref(h12, r23, 3). h_pref(h12, r24, 4).
h_pref(h12, r21, 5). h_pref(h12, r22, 6). h_pref(h12, r25, 7). h_pref(h12, r26, 8).

% Block B3
h_pref(h13, r29, 1). h_pref(h13, r30, 2). h_pref(h13, r33, 3). h_pref(h13, r31, 4).
h_pref(h13, r32, 5). h_pref(h13, r34, 6). h_pref(h13, r35, 7). h_pref(h13, r36, 8).
h_pref(h14, r31, 1). h_pref(h14, r32, 2). h_pref(h14, r34, 3). h_pref(h14, r29, 4).
h_pref(h14, r30, 5). h_pref(h14, r33, 6). h_pref(h14, r35, 7). h_pref(h14, r36, 8).
h_pref(h15, r35, 1). h_pref(h15, r36, 2). h_pref(h15, r31, 3). h_pref(h15, r32, 4).
h_pref(h15, r29, 5). h_pref(h15, r30, 6). h_pref(h15, r33, 7). h_pref(h15, r34, 8).

% Block A4
h_pref(h16, r39, 1). h_pref(h16, r40, 2). h_pref(h16, r37, 3). h_pref(h16, r38, 4).
h_pref(h17, r37, 1). h_pref(h17, r38, 2). h_pref(h17, r39, 3). h_pref(h17, r40, 4).

% ---- Mutual Acceptability ----
acceptable(R, H) :- r_pref(R, H, _), h_pref(H, R, _).

% ---- Choice: Assign residents to hospitals ----
{ assigned(R, H) : acceptable(R, H) } 1 :- resident(R).

% ---- Capacity Constraint ----
:- hospital(H), capacity(H, Cap), Cap < #count { R : assigned(R, H) }.

% ---- Stability: No blocking pair ----
% A blocking pair (R, H) exists if:
% 1. R prefers H over current assignment (or is unmatched)
% 2. H would accept R (has free capacity OR prefers R over some current assignee)

% R prefers H over current assignment
r_prefers_over_current(R, H) :- assigned(R, H2), r_pref(R, H, P1), r_pref(R, H2, P2), P1 < P2.

% R is unmatched and H is acceptable
r_unmatched_prefers(R, H) :- resident(R), acceptable(R, H), not assigned(R, _).

% H has free capacity
h_has_capacity(H) :- hospital(H), capacity(H, Cap), #count { R : assigned(R, H) } < Cap.

% H prefers R over some current assignee
h_prefers_over_some(H, R) :- assigned(R2, H), h_pref(H, R, P1), h_pref(H, R2, P2), P1 < P2.

% Blocking pair definition
blocking_pair(R, H) :- acceptable(R, H), r_prefers_over_current(R, H), h_has_capacity(H).
blocking_pair(R, H) :- acceptable(R, H), r_prefers_over_current(R, H), h_prefers_over_some(H, R).
blocking_pair(R, H) :- acceptable(R, H), r_unmatched_prefers(R, H), h_has_capacity(H).
blocking_pair(R, H) :- acceptable(R, H), r_unmatched_prefers(R, H), h_prefers_over_some(H, R).

% Stability constraint: no blocking pairs allowed
:- blocking_pair(_, _).

% ---- Output ----
#show assigned/2.