% Domains
resident(r1; r2; r3; r4; r5; r6; r7; r8; r9; r10; r11; r12; r13; r14; r15; r16; r17; r18; r19; r20;
          r21; r22; r23; r24; r25; r26; r27; r28; r29; r30; r31; r32; r33; r34; r35; r36; r37; r38; r39; r40).

hospital(h1; h2; h3; h4; h5; h6; h7; h8; h9; h10; h11; h12; h13; h14; h15; h16; h17; h18; h19; h20).

% Capacities (h18, h19, h20 have no acceptable residents)
hospital(h1,2). hospital(h2,2). hospital(h3,2). hospital(h4,2). hospital(h5,2). hospital(h6,2).
hospital(h7,4). hospital(h8,3). hospital(h9,1).
hospital(h10,3). hospital(h11,3). hospital(h12,2).
hospital(h13,3). hospital(h14,3). hospital(h15,2).
hospital(h16,2). hospital(h17,2).
hospital(h18,1). hospital(h19,1). hospital(h20,1).

% Acceptable pairs (mutual)
% Block A1
acceptable(r1,h1). acceptable(r1,h2).
acceptable(r2,h1). acceptable(r2,h2).
acceptable(r3,h1). acceptable(r3,h2).
acceptable(r4,h1). acceptable(r4,h2).

% Block A2
acceptable(r5,h3). acceptable(r5,h4).
acceptable(r6,h3). acceptable(r6,h4).
acceptable(r7,h3). acceptable(r7,h4).
acceptable(r8,h3). acceptable(r8,h4).

% Block A3
acceptable(r9,h5). acceptable(r9,h6).
acceptable(r10,h5). acceptable(r10,h6).
acceptable(r11,h5). acceptable(r11,h6).
acceptable(r12,h5). acceptable(r12,h6).

% Block B1
acceptable(r13,h7). acceptable(r13,h8). acceptable(r13,h9).
acceptable(r14,h7). acceptable(r14,h8). acceptable(r14,h9).
acceptable(r15,h7). acceptable(r15,h8). acceptable(r15,h9).
acceptable(r16,h7). acceptable(r16,h8). acceptable(r16,h9).
acceptable(r17,h7). acceptable(r17,h8). acceptable(r17,h9).
acceptable(r18,h7). acceptable(r18,h8). acceptable(r18,h9).
acceptable(r19,h7). acceptable(r19,h8). acceptable(r19,h9).
acceptable(r20,h7). acceptable(r20,h8). acceptable(r20,h9).

% Block B2
acceptable(r21,h10). acceptable(r21,h11). acceptable(r21,h12).
acceptable(r22,h10). acceptable(r22,h11). acceptable(r22,h12).
acceptable(r23,h10). acceptable(r23,h11). acceptable(r23,h12).
acceptable(r24,h10). acceptable(r24,h11). acceptable(r24,h12).
acceptable(r25,h10). acceptable(r25,h11). acceptable(r25,h12).
acceptable(r26,h10). acceptable(r26,h11). acceptable(r26,h12).
acceptable(r27,h10). acceptable(r27,h11). acceptable(r27,h12).
acceptable(r28,h10). acceptable(r28,h11). acceptable(r28,h12).

% Block B3
acceptable(r29,h13). acceptable(r29,h14). acceptable(r29,h15).
acceptable(r30,h13). acceptable(r30,h14). acceptable(r30,h15).
acceptable(r31,h13). acceptable(r31,h14). acceptable(r31,h15).
acceptable(r32,h13). acceptable(r32,h14). acceptable(r32,h15).
acceptable(r33,h13). acceptable(r33,h14). acceptable(r33,h15).
acceptable(r34,h13). acceptable(r34,h14). acceptable(r34,h15).
acceptable(r35,h13). acceptable(r35,h14). acceptable(r35,h15).
acceptable(r36,h13). acceptable(r36,h14). acceptable(r36,h15).

% Block A4
acceptable(r37,h16). acceptable(r37,h17).
acceptable(r38,h16). acceptable(r38,h17).
acceptable(r39,h16). acceptable(r39,h17).
acceptable(r40,h16). acceptable(r40,h17).

% Resident preferences (strict order)
% Block A1
prefers_hospital(r1,h1,h2).
prefers_hospital(r2,h1,h2).
prefers_hospital(r3,h2,h1).
prefers_hospital(r4,h2,h1).

% Block A2
prefers_hospital(r5,h3,h4).
prefers_hospital(r6,h3,h4).
prefers_hospital(r7,h4,h3).
prefers_hospital(r8,h4,h3).

% Block A3
prefers_hospital(r9,h5,h6).
prefers_hospital(r10,h5,h6).
prefers_hospital(r11,h6,h5).
prefers_hospital(r12,h6,h5).

% Block B1
prefers_hospital(r13,h7,h8). prefers_hospital(r13,h8,h9).
prefers_hospital(r14,h7,h8). prefers_hospital(r14,h8,h9).
prefers_hospital(r15,h8,h7). prefers_hospital(r15,h7,h9).
prefers_hospital(r16,h8,h7). prefers_hospital(r16,h7,h9).
prefers_hospital(r17,h7,h8). prefers_hospital(r17,h8,h9).
prefers_hospital(r18,h7,h9). prefers_hospital(r18,h9,h8).
prefers_hospital(r19,h8,h9). prefers_hospital(r19,h9,h7).
prefers_hospital(r20,h9,h8). prefers_hospital(r20,h8,h7).

% Block B2
prefers_hospital(r21,h10,h11). prefers_hospital(r21,h11,h12).
prefers_hospital(r22,h10,h12). prefers_hospital(r22,h12,h11).
prefers_hospital(r23,h11,h10). prefers_hospital(r23,h10,h12).
prefers_hospital(r24,h11,h12). prefers_hospital(r24,h12,h10).
prefers_hospital(r25,h10,h11). prefers_hospital(r25,h11,h12).
prefers_hospital(r26,h11,h10). prefers_hospital(r26,h10,h12).
prefers_hospital(r27,h12,h11). prefers_hospital(r27,h11,h10).
prefers_hospital(r28,h12,h10). prefers_hospital(r28,h10,h11).

% Block B3
prefers_hospital(r29,h13,h14). prefers_hospital(r29,h14,h15).
prefers_hospital(r30,h13,h15). prefers_hospital(r30,h15,h14).
prefers_hospital(r31,h14,h13). prefers_hospital(r31,h13,h15).
prefers_hospital(r32,h14,h15). prefers_hospital(r32,h15,h13).
prefers_hospital(r33,h13,h14). prefers_hospital(r33,h14,h15).
prefers_hospital(r34,h14,h13). prefers_hospital(r34,h13,h15).
prefers_hospital(r35,h15,h14). prefers_hospital(r35,h14,h13).
prefers_hospital(r36,h15,h13). prefers_hospital(r36,h13,h14).

% Block A4
prefers_hospital(r37,h16,h17).
prefers_hospital(r38,h16,h17).
prefers_hospital(r39,h17,h16).
prefers_hospital(r40,h17,h16).

% Hospital preferences (strict order)
% Block A1
hospital_prefers(h1,r3,r4). hospital_prefers(h1,r4,r1). hospital_prefers(h1,r1,r2).
hospital_prefers(h2,r1,r2). hospital_prefers(h2,r2,r3). hospital_prefers(h2,r3,r4).

% Block A2
hospital_prefers(h3,r7,r8). hospital_prefers(h3,r8,r5). hospital_prefers(h3,r5,r6).
hospital_prefers(h4,r5,r6). hospital_prefers(h4,r6,r7). hospital_prefers(h4,r7,r8).

% Block A3
hospital_prefers(h5,r11,r12). hospital_prefers(h5,r12,r9). hospital_prefers(h5,r9,r10).
hospital_prefers(h6,r9,r10). hospital_prefers(h6,r10,r11). hospital_prefers(h6,r11,r12).

% Block B1
hospital_prefers(h7,r13,r14). hospital_prefers(h7,r14,r17). hospital_prefers(h7,r17,r18).
hospital_prefers(h7,r18,r15). hospital_prefers(h7,r15,r16). hospital_prefers(h7,r16,r19).
hospital_prefers(h7,r19,r20).

hospital_prefers(h8,r15,r16). hospital_prefers(h8,r16,r19). hospital_prefers(h8,r19,r13).
hospital_prefers(h8,r13,r14). hospital_prefers(h8,r14,r17). hospital_prefers(h8,r17,r18).
hospital_prefers(h8,r18,r20).

hospital_prefers(h9,r20,r19). hospital_prefers(h9,r19,r18). hospital_prefers(h9,r18,r17).
hospital_prefers(h9,r17,r16). hospital_prefers(h9,r16,r15). hospital_prefers(h9,r15,r14).
hospital_prefers(h9,r14,r13).

% Block B2
hospital_prefers(h10,r21,r22). hospital_prefers(h10,r22,r25). hospital_prefers(h10,r25,r23).
hospital_prefers(h10,r23,r24). hospital_prefers(h10,r24,r26). hospital_prefers(h10,r26,r27).
hospital_prefers(h10,r27,r28).

hospital_prefers(h11,r23,r24). hospital_prefers(h11,r24,r26). hospital_prefers(h11,r26,r21).
hospital_prefers(h11,r21,r22). hospital_prefers(h11,r22,r25). hospital_prefers(h11,r25,r27).
hospital_prefers(h11,r27,r28).

hospital_prefers(h12,r27,r28). hospital_prefers(h12,r28,r23). hospital_prefers(h12,r23,r24).
hospital_prefers(h12,r24,r21). hospital_prefers(h12,r21,r22). hospital_prefers(h12,r22,r25).
hospital_prefers(h12,r25,r26).

% Block B3
hospital_prefers(h13,r29,r30). hospital_prefers(h13,r30,r33). hospital_prefers(h13,r33,r31).
hospital_prefers(h13,r31,r32). hospital_prefers(h13,r32,r34). hospital_prefers(h13,r34,r35).
hospital_prefers(h13,r35,r36).

hospital_prefers(h14,r31,r32). hospital_prefers(h14,r32,r34). hospital_prefers(h14,r34,r29).
hospital_prefers(h14,r29,r30). hospital_prefers(h14,r30,r33). hospital_prefers(h14,r33,r35).
hospital_prefers(h14,r35,r36).

hospital_prefers(h15,r35,r36). hospital_prefers(h15,r36,r31). hospital_prefers(h15,r31,r32).
hospital_prefers(h15,r32,r29). hospital_prefers(h15,r29,r30). hospital_prefers(h15,r30,r33).
hospital_prefers(h15,r33,r34).

% Block A4
hospital_prefers(h16,r39,r40). hospital_prefers(h16,r40,r37). hospital_prefers(h16,r37,r38).
hospital_prefers(h17,r37,r38). hospital_prefers(h17,r38,r39). hospital_prefers(h17,r39,r40).

% Choice rule for matching
{ matched(R, H) : hospital(H, _) } :- resident(R).

% Hospital capacity constraints
:- hospital(H, Cap), #count { R : matched(R, H) } > Cap.

% Only acceptable pairs can be matched
:- matched(R, H), not acceptable(R, H).

% Helper predicates
unmatched(R) :- resident(R), not matched(R, _).
free_capacity(H) :- hospital(H, Cap), #count { R : matched(R, H) } < Cap.

% Blocking pair check:
% A blocking pair (R, H) exists if:
% 1. R is unmatched OR R prefers H over their current match
% 2. H has free capacity OR H prefers R over at least one current assignee

% Case 1: R is unmatched and H has free capacity
:- unmatched(R), free_capacity(H), acceptable(R, H).

% Case 2: R is unmatched and H prefers R over some current assignee
:- unmatched(R), matched(R_cur, H), acceptable(R, H), hospital_prefers(H, R, R_cur).

% Case 3: R prefers H over current match and H has free capacity
:- matched(R, H_cur), prefers_hospital(R, H, H_cur), free_capacity(H), acceptable(R, H).

% Case 4: R prefers H over current match and H prefers R over some current assignee
:- matched(R, H_cur), prefers_hospital(R, H, H_cur), matched(R_cur2, H), hospital_prefers(H, R, R_cur2), acceptable(R, H).

% Show the stable matchings
#show matched/2.