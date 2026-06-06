% Stable Matching Problem: 40 residents, 20 hospitals
% Find all stable matchings

% ========== DOMAINS ==========
resident(r1..r40).
hospital(h1..h20).

% ========== CAPACITIES ==========
capacity(h1, 2). capacity(h2, 2). capacity(h3, 2). capacity(h4, 2).
capacity(h5, 2). capacity(h6, 2). capacity(h7, 4). capacity(h8, 3).
capacity(h9, 1). capacity(h10, 3). capacity(h11, 3). capacity(h12, 2).
capacity(h13, 3). capacity(h14, 3). capacity(h15, 2). capacity(h16, 2).
capacity(h17, 2). capacity(h18, 1). capacity(h19, 1). capacity(h20, 1).

% ========== RESIDENT PREFERENCES ==========
% Block A1 (r1-r4)
resident_pref_rank(r1, h1, 1). resident_pref_rank(r1, h2, 2).
resident_pref_rank(r2, h1, 1). resident_pref_rank(r2, h2, 2).
resident_pref_rank(r3, h2, 1). resident_pref_rank(r3, h1, 2).
resident_pref_rank(r4, h2, 1). resident_pref_rank(r4, h1, 2).

% Block A2 (r5-r8)
resident_pref_rank(r5, h3, 1). resident_pref_rank(r5, h4, 2).
resident_pref_rank(r6, h3, 1). resident_pref_rank(r6, h4, 2).
resident_pref_rank(r7, h4, 1). resident_pref_rank(r7, h3, 2).
resident_pref_rank(r8, h4, 1). resident_pref_rank(r8, h3, 2).

% Block A3 (r9-r12)
resident_pref_rank(r9, h5, 1). resident_pref_rank(r9, h6, 2).
resident_pref_rank(r10, h5, 1). resident_pref_rank(r10, h6, 2).
resident_pref_rank(r11, h6, 1). resident_pref_rank(r11, h5, 2).
resident_pref_rank(r12, h6, 1). resident_pref_rank(r12, h5, 2).

% Block B1 (r13-r20)
resident_pref_rank(r13, h7, 1). resident_pref_rank(r13, h8, 2). resident_pref_rank(r13, h9, 3).
resident_pref_rank(r14, h7, 1). resident_pref_rank(r14, h8, 2). resident_pref_rank(r14, h9, 3).
resident_pref_rank(r15, h8, 1). resident_pref_rank(r15, h7, 2). resident_pref_rank(r15, h9, 3).
resident_pref_rank(r16, h8, 1). resident_pref_rank(r16, h7, 2). resident_pref_rank(r16, h9, 3).
resident_pref_rank(r17, h7, 1). resident_pref_rank(r17, h8, 2). resident_pref_rank(r17, h9, 3).
resident_pref_rank(r18, h7, 1). resident_pref_rank(r18, h9, 2). resident_pref_rank(r18, h8, 3).
resident_pref_rank(r19, h8, 1). resident_pref_rank(r19, h9, 2). resident_pref_rank(r19, h7, 3).
resident_pref_rank(r20, h9, 1). resident_pref_rank(r20, h8, 2). resident_pref_rank(r20, h7, 3).

% Block B2 (r21-r28)
resident_pref_rank(r21, h10, 1). resident_pref_rank(r21, h11, 2). resident_pref_rank(r21, h12, 3).
resident_pref_rank(r22, h10, 1). resident_pref_rank(r22, h12, 2). resident_pref_rank(r22, h11, 3).
resident_pref_rank(r23, h11, 1). resident_pref_rank(r23, h10, 2). resident_pref_rank(r23, h12, 3).
resident_pref_rank(r24, h11, 1). resident_pref_rank(r24, h12, 2). resident_pref_rank(r24, h10, 3).
resident_pref_rank(r25, h10, 1). resident_pref_rank(r25, h11, 2). resident_pref_rank(r25, h12, 3).
resident_pref_rank(r26, h11, 1). resident_pref_rank(r26, h10, 2). resident_pref_rank(r26, h12, 3).
resident_pref_rank(r27, h12, 1). resident_pref_rank(r27, h11, 2). resident_pref_rank(r27, h10, 3).
resident_pref_rank(r28, h12, 1). resident_pref_rank(r28, h10, 2). resident_pref_rank(r28, h11, 3).

% Block B3 (r29-r36)
resident_pref_rank(r29, h13, 1). resident_pref_rank(r29, h14, 2). resident_pref_rank(r29, h15, 3).
resident_pref_rank(r30, h13, 1). resident_pref_rank(r30, h15, 2). resident_pref_rank(r30, h14, 3).
resident_pref_rank(r31, h14, 1). resident_pref_rank(r31, h13, 2). resident_pref_rank(r31, h15, 3).
resident_pref_rank(r32, h14, 1). resident_pref_rank(r32, h15, 2). resident_pref_rank(r32, h13, 3).
resident_pref_rank(r33, h13, 1). resident_pref_rank(r33, h14, 2). resident_pref_rank(r33, h15, 3).
resident_pref_rank(r34, h14, 1). resident_pref_rank(r34, h13, 2). resident_pref_rank(r34, h15, 3).
resident_pref_rank(r35, h15, 1). resident_pref_rank(r35, h14, 2). resident_pref_rank(r35, h13, 3).
resident_pref_rank(r36, h15, 1). resident_pref_rank(r36, h13, 2). resident_pref_rank(r36, h14, 3).

% Block A4 (r37-r40)
resident_pref_rank(r37, h16, 1). resident_pref_rank(r37, h17, 2).
resident_pref_rank(r38, h16, 1). resident_pref_rank(r38, h17, 2).
resident_pref_rank(r39, h17, 1). resident_pref_rank(r39, h16, 2).
resident_pref_rank(r40, h17, 1). resident_pref_rank(r40, h16, 2).

% ========== HOSPITAL PREFERENCES ==========
% Block A1
hospital_pref_rank(h1, r3, 1). hospital_pref_rank(h1, r4, 2). hospital_pref_rank(h1, r1, 3). hospital_pref_rank(h1, r2, 4).
hospital_pref_rank(h2, r1, 1). hospital_pref_rank(h2, r2, 2). hospital_pref_rank(h2, r3, 3). hospital_pref_rank(h2, r4, 4).

% Block A2
hospital_pref_rank(h3, r7, 1). hospital_pref_rank(h3, r8, 2). hospital_pref_rank(h3, r5, 3). hospital_pref_rank(h3, r6, 4).
hospital_pref_rank(h4, r5, 1). hospital_pref_rank(h4, r6, 2). hospital_pref_rank(h4, r7, 3). hospital_pref_rank(h4, r8, 4).

% Block A3
hospital_pref_rank(h5, r11, 1). hospital_pref_rank(h5, r12, 2). hospital_pref_rank(h5, r9, 3). hospital_pref_rank(h5, r10, 4).
hospital_pref_rank(h6, r9, 1). hospital_pref_rank(h6, r10, 2). hospital_pref_rank(h6, r11, 3). hospital_pref_rank(h6, r12, 4).

% Block B1
hospital_pref_rank(h7, r13, 1). hospital_pref_rank(h7, r14, 2). hospital_pref_rank(h7, r17, 3). hospital_pref_rank(h7, r18, 4).
hospital_pref_rank(h7, r15, 5). hospital_pref_rank(h7, r16, 6). hospital_pref_rank(h7, r19, 7). hospital_pref_rank(h7, r20, 8).
hospital_pref_rank(h8, r15, 1). hospital_pref_rank(h8, r16, 2). hospital_pref_rank(h8, r19, 3). hospital_pref_rank(h8, r13, 4).
hospital_pref_rank(h8, r14, 5). hospital_pref_rank(h8, r17, 6). hospital_pref_rank(h8, r18, 7). hospital_pref_rank(h8, r20, 8).
hospital_pref_rank(h9, r20, 1). hospital_pref_rank(h9, r19, 2). hospital_pref_rank(h9, r18, 3). hospital_pref_rank(h9, r17, 4).
hospital_pref_rank(h9, r16, 5). hospital_pref_rank(h9, r15, 6). hospital_pref_rank(h9, r14, 7). hospital_pref_rank(h9, r13, 8).

% Block B2
hospital_pref_rank(h10, r21, 1). hospital_pref_rank(h10, r22, 2). hospital_pref_rank(h10, r25, 3). hospital_pref_rank(h10, r23, 4).
hospital_pref_rank(h10, r24, 5). hospital_pref_rank(h10, r26, 6). hospital_pref_rank(h10, r27, 7). hospital_pref_rank(h10, r28, 8).
hospital_pref_rank(h11, r23, 1). hospital_pref_rank(h11, r24, 2). hospital_pref_rank(h11, r26, 3). hospital_pref_rank(h11, r21, 4).
hospital_pref_rank(h11, r22, 5). hospital_pref_rank(h11, r25, 6). hospital_pref_rank(h11, r27, 7). hospital_pref_rank(h11, r28, 8).
hospital_pref_rank(h12, r27, 1). hospital_pref_rank(h12, r28, 2). hospital_pref_rank(h12, r23, 3). hospital_pref_rank(h12, r24, 4).
hospital_pref_rank(h12, r21, 5). hospital_pref_rank(h12, r22, 6). hospital_pref_rank(h12, r25, 7). hospital_pref_rank(h12, r26, 8).

% Block B3
hospital_pref_rank(h13, r29, 1). hospital_pref_rank(h13, r30, 2). hospital_pref_rank(h13, r33, 3). hospital_pref_rank(h13, r31, 4).
hospital_pref_rank(h13, r32, 5). hospital_pref_rank(h13, r34, 6). hospital_pref_rank(h13, r35, 7). hospital_pref_rank(h13, r36, 8).
hospital_pref_rank(h14, r31, 1). hospital_pref_rank(h14, r32, 2). hospital_pref_rank(h14, r34, 3). hospital_pref_rank(h14, r29, 4).
hospital_pref_rank(h14, r30, 5). hospital_pref_rank(h14, r33, 6). hospital_pref_rank(h14, r35, 7). hospital_pref_rank(h14, r36, 8).
hospital_pref_rank(h15, r35, 1). hospital_pref_rank(h15, r36, 2). hospital_pref_rank(h15, r31, 3). hospital_pref_rank(h15, r32, 4).
hospital_pref_rank(h15, r29, 5). hospital_pref_rank(h15, r30, 6). hospital_pref_rank(h15, r33, 7). hospital_pref_rank(h15, r34, 8).

% Block A4
hospital_pref_rank(h16, r39, 1). hospital_pref_rank(h16, r40, 2). hospital_pref_rank(h16, r37, 3). hospital_pref_rank(h16, r38, 4).
hospital_pref_rank(h17, r37, 1). hospital_pref_rank(h17, r38, 2). hospital_pref_rank(h17, r39, 3). hospital_pref_rank(h17, r40, 4).

% Hospitals h18, h19, h20 have no acceptable residents (no preferences listed)

% ========== ACCEPTABLE PAIRS ==========
% A pair (R, H) is acceptable if both appear in each other's preference lists
acceptable(R, H) :- resident_pref_rank(R, H, _), hospital_pref_rank(H, R, _).

% ========== ASSIGNMENT ==========
% Each resident is assigned to at most one hospital
1 { assign(R, H) : acceptable(R, H) } 1 :- resident(R).

% Each hospital is assigned at most its capacity
:- assign(R, H), #count{ R2 : assign(R2, H) } > capacity(H).

% ========== HELPER PREDICATES FOR STABILITY ==========
% Resident's current assignment
resident_assigned(R, H) :- assign(R, H).

% Resident is unmatched
resident_unmatched(R) :- resident(R), not resident_assigned(R, _).

% Resident prefers H over current assignment Hcur
resident_prefers_over(R, H, Hcur) :- resident_pref_rank(R, H, R1), resident_pref_rank(R, Hcur, R2), R1 < R2.

% Hospital has free capacity
hospital_has_free_capacity(H) :- hospital(H), #count{ R : assign(R, H) } < capacity(H).

% Hospital prefers R over current assignee Rcur
hospital_prefers_over(H, R, Rcur) :- hospital_pref_rank(H, R, R1), hospital_pref_rank(H, Rcur, R2), R1 < R2.

% ========== STABILITY CONSTRAINTS ==========
% Resident prefers H over current assignment (or is unmatched)
resident_better_unmatched(R, H) :- acceptable(R, H), not assign(R, H), resident_unmatched(R).
resident_better_over_current(R, H, Hcur) :- acceptable(R, H), not assign(R, H), resident_assigned(R, Hcur), H != Hcur, resident_prefers_over(R, H, Hcur).

% Hospital would accept R
hospital_accepts_free(H, R) :- acceptable(R, H), hospital_has_free_capacity(H).
hospital_accepts_over_current(H, R, Rcur) :- acceptable(R, H), not hospital_has_free_capacity(H), assign(Rcur, H), hospital_prefers_over(H, R, Rcur).

% No blocking pairs
:- resident_better_unmatched(R, H), hospital_accepts_free(H, R).
:- resident_better_over_current(R, H, Hcur), hospital_accepts_over_current(H, R, Rcur).

% ========== OUTPUT ==========
% Show assignments for each stable matching
#show assign/2.

% Count the number of stable matchings (will be shown in solver output)
#show matching_count/1.
matching_count(N) :- N = #count{ M : model_id(M) }.
model_id(1) :- assign(r1, _).  % This will be true in every model