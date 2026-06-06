%%% DOMAIN DECLARATIONS %%%

% Residents
resident(r1; r2; r3; r4; r5; r6; r7; r8; r9; r10; r11; r12; r13; r14; r15; r16; r17; r18; r19; r20; r21; r22; r23; r24; r25; r26; r27; r28; r29; r30; r31; r32; r33; r34; r35; r36; r37; r38; r39; r40).

% Hospitals
hospital(h1; h2; h3; h4; h5; h6; h7; h8; h9; h10; h11; h12; h13; h14; h15; h16; h17; h18; h19; h20).

% Hospital capacities
capacity(h1, 2).
capacity(h2, 2).
capacity(h3, 2).
capacity(h4, 2).
capacity(h5, 2).
capacity(h6, 2).
capacity(h7, 4).
capacity(h8, 3).
capacity(h9, 1).
capacity(h10, 3).
capacity(h11, 3).
capacity(h12, 2).
capacity(h13, 3).
capacity(h14, 3).
capacity(h15, 2).
capacity(h16, 2).
capacity(h17, 2).
capacity(h18, 1).
capacity(h19, 1).
capacity(h20, 1).

%%% PREFERENCE DECLARATIONS %%%

% Resident preferences: pref_res(Resident, Hospital, Rank) where lower rank = more preferred

% Block A1 (r1-r4)
pref_res(r1, h1, 1). pref_res(r1, h2, 2).
pref_res(r2, h1, 1). pref_res(r2, h2, 2).
pref_res(r3, h2, 1). pref_res(r3, h1, 2).
pref_res(r4, h2, 1). pref_res(r4, h1, 2).

% Block A2 (r5-r8)
pref_res(r5, h3, 1). pref_res(r5, h4, 2).
pref_res(r6, h3, 1). pref_res(r6, h4, 2).
pref_res(r7, h4, 1). pref_res(r7, h3, 2).
pref_res(r8, h4, 1). pref_res(r8, h3, 2).

% Block A3 (r9-r12)
pref_res(r9, h5, 1). pref_res(r9, h6, 2).
pref_res(r10, h5, 1). pref_res(r10, h6, 2).
pref_res(r11, h6, 1). pref_res(r11, h5, 2).
pref_res(r12, h6, 1). pref_res(r12, h5, 2).

% Block B1 (r13-r20)
pref_res(r13, h7, 1). pref_res(r13, h8, 2). pref_res(r13, h9, 3).
pref_res(r14, h7, 1). pref_res(r14, h8, 2). pref_res(r14, h9, 3).
pref_res(r15, h8, 1). pref_res(r15, h7, 2). pref_res(r15, h9, 3).
pref_res(r16, h8, 1). pref_res(r16, h7, 2). pref_res(r16, h9, 3).
pref_res(r17, h7, 1). pref_res(r17, h8, 2). pref_res(r17, h9, 3).
pref_res(r18, h7, 1). pref_res(r18, h9, 2). pref_res(r18, h8, 3).
pref_res(r19, h8, 1). pref_res(r19, h9, 2). pref_res(r19, h7, 3).
pref_res(r20, h9, 1). pref_res(r20, h8, 2). pref_res(r20, h7, 3).

% Block B2 (r21-r28)
pref_res(r21, h10, 1). pref_res(r21, h11, 2). pref_res(r21, h12, 3).
pref_res(r22, h10, 1). pref_res(r22, h12, 2). pref_res(r22, h11, 3).
pref_res(r23, h11, 1). pref_res(r23, h10, 2). pref_res(r23, h12, 3).
pref_res(r24, h11, 1). pref_res(r24, h12, 2). pref_res(r24, h10, 3).
pref_res(r25, h10, 1). pref_res(r25, h11, 2). pref_res(r25, h12, 3).
pref_res(r26, h11, 1). pref_res(r26, h10, 2). pref_res(r26, h12, 3).
pref_res(r27, h12, 1). pref_res(r27, h11, 2). pref_res(r27, h10, 3).
pref_res(r28, h12, 1). pref_res(r28, h10, 2). pref_res(r28, h11, 3).

% Block B3 (r29-r36)
pref_res(r29, h13, 1). pref_res(r29, h14, 2). pref_res(r29, h15, 3).
pref_res(r30, h13, 1). pref_res(r30, h15, 2). pref_res(r30, h14, 3).
pref_res(r31, h14, 1). pref_res(r31, h13, 2). pref_res(r31, h15, 3).
pref_res(r32, h14, 1). pref_res(r32, h15, 2). pref_res(r32, h13, 3).
pref_res(r33, h13, 1). pref_res(r33, h14, 2). pref_res(r33, h15, 3).
pref_res(r34, h14, 1). pref_res(r34, h13, 2). pref_res(r34, h15, 3).
pref_res(r35, h15, 1). pref_res(r35, h14, 2). pref_res(r35, h13, 3).
pref_res(r36, h15, 1). pref_res(r36, h13, 2). pref_res(r36, h14, 3).

% Block A4 (r37-r40)
pref_res(r37, h16, 1). pref_res(r37, h17, 2).
pref_res(r38, h16, 1). pref_res(r38, h17, 2).
pref_res(r39, h17, 1). pref_res(r39, h16, 2).
pref_res(r40, h17, 1). pref_res(r40, h16, 2).

% Hospital preferences: pref_hosp(Hospital, Resident, Rank) where lower rank = more preferred

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

%%% ACCEPTABLE PAIRS %%%

% A pair (r, h) is acceptable if both have each other in their preference lists
acceptable(R, H) :- pref_res(R, H, _), pref_hosp(H, R, _).

%%% CHOICE RULES: GENERATE MATCHINGS %%%

% Each resident can be matched to at most one hospital (among acceptable ones)
{ matched(R, H) : acceptable(R, H) } 1 :- resident(R).

% Each hospital can be matched to at most its capacity of residents
{ matched(R, H) : acceptable(R, H) } :- hospital(H), capacity(H, Cap), Cap > 0.

% Hospitals with capacity 0 or no acceptable residents get no one
:- matched(R, H), hospital(H), capacity(H, Cap), Cap = 0.
:- matched(R, H), not acceptable(R, H).

%%% CAPACITY CONSTRAINT %%%

% Hospital capacity constraint
:- hospital(H), capacity(H, Cap), #count{ R : matched(R, H) } > Cap.

%%% STABILITY CONSTRAINTS %%%

% A blocking pair is (R, H) where:
% 1. R is not matched to H
% 2. R prefers H over their current match (or R is unmatched)
% 3. H would accept R (either has free capacity or prefers R over at least one current assignee)

% Helper: R is unmatched
unmatched(R) :- resident(R), not matched(R, _).

% Helper: R prefers H1 over H2
prefers(R, H1, H2) :- pref_res(R, H1, Rank1), pref_res(R, H2, Rank2), Rank1 < Rank2.

% Helper: H prefers R1 over R2
prefers_h(H, R1, R2) :- pref_hosp(H, R1, Rank1), pref_hosp(H, R2, Rank2), Rank1 < Rank2.

% Helper: H has free capacity (counting current matches)
h_free_capacity(H) :- hospital(H), capacity(H, Cap), #count{ R : matched(R, H) } < Cap.

% Helper: H prefers R over at least one current assignee
h_prefers_over_current(H, R) :- matched(R2, H), prefers_h(H, R, R2).

% Blocking pair condition
blocking(R, H) :-
    acceptable(R, H),
    not matched(R, H),
    ( unmatched(R) ; matched(R, H_cur), prefers(R, H, H_cur) ),
    ( h_free_capacity(H) ; h_prefers_over_current(H, R) ).

% No blocking pairs allowed
:- blocking(R, H).

%%% OUTPUT %%%

#show matched/2.