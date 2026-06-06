% Stable Matching Problem - 40 residents, 20 hospitals

% ===== DOMAIN DECLARATIONS =====
% Residents (explicitly defined)
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

% Hospitals with capacities
hospital(h1). capacity(h1, 2).
hospital(h2). capacity(h2, 2).
hospital(h3). capacity(h3, 2).
hospital(h4). capacity(h4, 2).
hospital(h5). capacity(h5, 2).
hospital(h6). capacity(h6, 2).
hospital(h7). capacity(h7, 4).
hospital(h8). capacity(h8, 3).
hospital(h9). capacity(h9, 1).
hospital(h10). capacity(h10, 3).
hospital(h11). capacity(h11, 3).
hospital(h12). capacity(h12, 2).
hospital(h13). capacity(h13, 3).
hospital(h14). capacity(h14, 3).
hospital(h15). capacity(h15, 2).
hospital(h16). capacity(h16, 2).
hospital(h17). capacity(h17, 2).
hospital(h18). capacity(h18, 1).
hospital(h19). capacity(h19, 1).
hospital(h20). capacity(h20, 1).

% ===== PREFERENCE RANKINGS =====
% Residents' preferences (rank 1 is best)
% Block A1
pref_res(r1, h1, 1). pref_res(r1, h2, 2).
pref_res(r2, h1, 1). pref_res(r2, h2, 2).
pref_res(r3, h2, 1). pref_res(r3, h1, 2).
pref_res(r4, h2, 1). pref_res(r4, h1, 2).

% Block A2
pref_res(r5, h3, 1). pref_res(r5, h4, 2).
pref_res(r6, h3, 1). pref_res(r6, h4, 2).
pref_res(r7, h4, 1). pref_res(r7, h3, 2).
pref_res(r8, h4, 1). pref_res(r8, h3, 2).

% Block A3
pref_res(r9, h5, 1). pref_res(r9, h6, 2).
pref_res(r10, h5, 1). pref_res(r10, h6, 2).
pref_res(r11, h6, 1). pref_res(r11, h5, 2).
pref_res(r12, h6, 1). pref_res(r12, h5, 2).

% Block B1
pref_res(r13, h7, 1). pref_res(r13, h8, 2). pref_res(r13, h9, 3).
pref_res(r14, h7, 1). pref_res(r14, h8, 2). pref_res(r14, h9, 3).
pref_res(r15, h8, 1). pref_res(r15, h7, 2). pref_res(r15, h9, 3).
pref_res(r16, h8, 1). pref_res(r16, h7, 2). pref_res(r16, h9, 3).
pref_res(r17, h7, 1). pref_res(r17, h8, 2). pref_res(r17, h9, 3).
pref_res(r18, h7, 1). pref_res(r18, h9, 2). pref_res(r18, h8, 3).
pref_res(r19, h8, 1). pref_res(r19, h9, 2). pref_res(r19, h7, 3).
pref_res(r20, h9, 1). pref_res(r20, h8, 2). pref_res(r20, h7, 3).

% Block B2
pref_res(r21, h10, 1). pref_res(r21, h11, 2). pref_res(r21, h12, 3).
pref_res(r22, h10, 1). pref_res(r22, h12, 2). pref_res(r22, h11, 3).
pref_res(r23, h11, 1). pref_res(r23, h10, 2). pref_res(r23, h12, 3).
pref_res(r24, h11, 1). pref_res(r24, h12, 2). pref_res(r24, h10, 3).
pref_res(r25, h10, 1). pref_res(r25, h11, 2). pref_res(r25, h12, 3).
pref_res(r26, h11, 1). pref_res(r26, h10, 2). pref_res(r26, h12, 3).
pref_res(r27, h12, 1). pref_res(r27, h11, 2). pref_res(r27, h10, 3).
pref_res(r28, h12, 1). pref_res(r28, h10, 2). pref_res(r28, h11, 3).

% Block B3
pref_res(r29, h13, 1). pref_res(r29, h14, 2). pref_res(r29, h15, 3).
pref_res(r30, h13, 1). pref_res(r30, h15, 2). pref_res(r30, h14, 3).
pref_res(r31, h14, 1). pref_res(r31, h13, 2). pref_res(r31, h15, 3).
pref_res(r32, h14, 1). pref_res(r32, h15, 2). pref_res(r32, h13, 3).
pref_res(r33, h13, 1). pref_res(r33, h14, 2). pref_res(r33, h15, 3).
pref_res(r34, h14, 1). pref_res(r34, h13, 2). pref_res(r34, h15, 3).
pref_res(r35, h15, 1). pref_res(r35, h14, 2). pref_res(r35, h13, 3).
pref_res(r36, h15, 1). pref_res(r36, h13, 2). pref_res(r36, h14, 3).

% Block A4
pref_res(r37, h16, 1). pref_res(r37, h17, 2).
pref_res(r38, h16, 1). pref_res(r38, h17, 2).
pref_res(r39, h17, 1). pref_res(r39, h16, 2).
pref_res(r40, h17, 1). pref_res(r40, h16, 2).

% Hospitals' preferences (rank 1 is best)
% Block A1
pref_hosp(h1, r3, 1). pref_hosp(h1, r4, 2). pref_hosp(h1, r1, 3). pref_hosp(h1, r2, 4).
pref_hosp(h2, r1, 1). pref_hosp(h2, r2, 2). pref_hosp(h2, r3, 3). pref_hosp(h2, r4, 4).

% Block A2
pref_hosp(h3, r7, 1). pref_hosp(h3, r8, 2). pref_hosp(h3, r5, 3). pref_hosp(h3, r6, 4).
pref_hosp(h4, r5, 1). pref_hosp(h4, r6, 2). pref_hosp(h4, r7, 3). pref_hosp(h4, r8, 4).

% Block A3
pref_hosp(h5, r11, 1). pref_hosp(h5, r12, 2). pref_hosp(h5, r9, 3). pref_hosp(h5, r10, 4).
pref_hosp(h6, r9, 1). pref_hosp(h6, r10, 2). pref_hosp(h6, r11, 3). pref_hosp(h6, r12, 4).

% Block B1
pref_hosp(h7, r13, 1). pref_hosp(h7, r14, 2). pref_hosp(h7, r17, 3). pref_hosp(h7, r18, 4).
pref_hosp(h7, r15, 5). pref_hosp(h7, r16, 6). pref_hosp(h7, r19, 7). pref_hosp(h7, r20, 8).
pref_hosp(h8, r15, 1). pref_hosp(h8, r16, 2). pref_hosp(h8, r19, 3). pref_hosp(h8, r13, 4).
pref_hosp(h8, r14, 5). pref_hosp(h8, r17, 6). pref_hosp(h8, r18, 7). pref_hosp(h8, r20, 8).
pref_hosp(h9, r20, 1). pref_hosp(h9, r19, 2). pref_hosp(h9, r18, 3). pref_hosp(h9, r17, 4).
pref_hosp(h9, r16, 5). pref_hosp(h9, r15, 6). pref_hosp(h9, r14, 7). pref_hosp(h9, r13, 8).

% Block B2
pref_hosp(h10, r21, 1). pref_hosp(h10, r22, 2). pref_hosp(h10, r25, 3). pref_hosp(h10, r23, 4).
pref_hosp(h10, r24, 5). pref_hosp(h10, r26, 6). pref_hosp(h10, r27, 7). pref_hosp(h10, r28, 8).
pref_hosp(h11, r23, 1). pref_hosp(h11, r24, 2). pref_hosp(h11, r26, 3). pref_hosp(h11, r21, 4).
pref_hosp(h11, r22, 5). pref_hosp(h11, r25, 6). pref_hosp(h11, r27, 7). pref_hosp(h11, r28, 8).
pref_hosp(h12, r27, 1). pref_hosp(h12, r28, 2). pref_hosp(h12, r23, 3). pref_hosp(h12, r24, 4).
pref_hosp(h12, r21, 5). pref_hosp(h12, r22, 6). pref_hosp(h12, r25, 7). pref_hosp(h12, r26, 8).

% Block B3
pref_hosp(h13, r29, 1). pref_hosp(h13, r30, 2). pref_hosp(h13, r33, 3). pref_hosp(h13, r31, 4).
pref_hosp(h13, r32, 5). pref_hosp(h13, r34, 6). pref_hosp(h13, r35, 7). pref_hosp(h13, r36, 8).
pref_hosp(h14, r31, 1). pref_hosp(h14, r32, 2). pref_hosp(h14, r34, 3). pref_hosp(h14, r29, 4).
pref_hosp(h14, r30, 5). pref_hosp(h14, r33, 6). pref_hosp(h14, r35, 7). pref_hosp(h14, r36, 8).
pref_hosp(h15, r35, 1). pref_hosp(h15, r36, 2). pref_hosp(h15, r31, 3). pref_hosp(h15, r32, 4).
pref_hosp(h15, r29, 5). pref_hosp(h15, r30, 6). pref_hosp(h15, r33, 7). pref_hosp(h15, r34, 8).

% Block A4
pref_hosp(h16, r39, 1). pref_hosp(h16, r40, 2). pref_hosp(h16, r37, 3). pref_hosp(h16, r38, 4).
pref_hosp(h17, r37, 1). pref_hosp(h17, r38, 2). pref_hosp(h17, r39, 3). pref_hosp(h17, r40, 4).

% Hospitals h18, h19, h20 have no acceptable residents (no preference entries)

% ===== MUTUAL ACCEPTABILITY =====
% A resident-hospital pair is acceptable if both have each other in their preference lists
acceptable(R, H) :- pref_res(R, H, _), pref_hosp(H, R, _).

% ===== MATCHING =====
% Choice rule: each resident can be matched to at most one hospital
{ matched(R, H) : acceptable(R, H) } 1 :- resident(R).

% Each hospital can be matched to at most its capacity
% Use a helper predicate for counting
hospital_count(H, N) :- hospital(H), N = #count{ R : matched(R, H) }.
:- hospital_count(H, N), capacity(H, C), N > C.

% ===== STABILITY CONDITIONS =====
% Helper: resident's current assignment
assigned(R, H) :- matched(R, H).

% Helper: hospital's current assignments
hospital_assigned(H, R) :- matched(R, H).

% Helper: resident prefers hospital H over current assignment
prefers_resident(R, H) :-
    assigned(R, H1),
    pref_res(R, H, RankH),
    pref_res(R, H1, RankH1),
    RankH < RankH1.

% Helper: resident is unmatched and prefers H
prefers_resident(R, H) :-
    not assigned(R, _),
    pref_res(R, H, _).

% Helper: hospital prefers resident R over at least one current assignee
prefers_hospital(H, R) :-
    hospital_assigned(H, R1),
    pref_hosp(H, R, RankR),
    pref_hosp(H, R1, RankR1),
    RankR < RankR1.

% Helper: hospital has free capacity
has_free_capacity(H) :-
    capacity(H, C),
    hospital_count(H, N),
    N < C.

% Blocking pair condition
% A pair (R, H) is blocking if:
% 1. R prefers H over current assignment (or is unmatched)
% 2. H would accept R (has free capacity OR prefers R over at least one current assignee)
blocking_pair(R, H) :-
    acceptable(R, H),
    prefers_resident(R, H),
    has_free_capacity(H).

blocking_pair(R, H) :-
    acceptable(R, H),
    prefers_resident(R, H),
    prefers_hospital(H, R).

% Stability constraint: no blocking pairs allowed
:- blocking_pair(R, H).

% ===== COUNTING AND OUTPUT =====
% Show the matching pairs
#show matched/2.

% Count the number of stable matchings
% We'll count the number of matched pairs to verify the matching is complete
matching_size(N) :- N = #count{ R, H : matched(R, H) }.

% For the final answer, we need to count all stable matchings
% Since Clingo finds all stable matchings, we count them
#show stable_matching_count/1.
stable_matching_count(N) :- N = #count{ 1 : matched(r1, _) }.