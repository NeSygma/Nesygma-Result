% Residents
resident(r1). resident(r2). resident(r3). resident(r4). resident(r5). resident(r6). resident(r7). resident(r8). resident(r9). resident(r10). resident(r11). resident(r12). resident(r13). resident(r14). resident(r15). resident(r16). resident(r17). resident(r18). resident(r19). resident(r20). resident(r21). resident(r22). resident(r23). resident(r24). resident(r25). resident(r26). resident(r27). resident(r28). resident(r29). resident(r30). resident(r31). resident(r32). resident(r33). resident(r34). resident(r35). resident(r36). resident(r37). resident(r38). resident(r39). resident(r40).

% Hospitals
hospital(h1). hospital(h2). hospital(h3). hospital(h4). hospital(h5). hospital(h6). hospital(h7). hospital(h8). hospital(h9). hospital(h10). hospital(h11). hospital(h12). hospital(h13). hospital(h14). hospital(h15). hospital(h16). hospital(h17). hospital(h18). hospital(h19). hospital(h20).

% Capacities
cap(h1,2). cap(h2,2). cap(h3,2). cap(h4,2). cap(h5,2). cap(h6,2). cap(h7,4). cap(h8,3). cap(h9,1). cap(h10,3). cap(h11,3). cap(h12,2). cap(h13,3). cap(h14,3). cap(h15,2). cap(h16,2). cap(h17,2). cap(h18,0). cap(h19,0). cap(h20,0).

% Resident preferences (ordered)
resident_pref(r1,h1). resident_pref(r1,h2).
resident_pref(r2,h1). resident_pref(r2,h2).
resident_pref(r3,h2). resident_pref(r3,h1).
resident_pref(r4,h2). resident_pref(r4,h1).

resident_pref(r5,h3). resident_pref(r5,h4).
resident_pref(r6,h3). resident_pref(r6,h4).
resident_pref(r7,h4). resident_pref(r7,h3).
resident_pref(r8,h4). resident_pref(r8,h3).

resident_pref(r9,h5). resident_pref(r9,h6).
resident_pref(r10,h5). resident_pref(r10,h6).
resident_pref(r11,h6). resident_pref(r11,h5).
resident_pref(r12,h6). resident_pref(r12,h5).

resident_pref(r13,h7). resident_pref(r13,h8). resident_pref(r13,h9).
resident_pref(r14,h7). resident_pref(r14,h8). resident_pref(r14,h9).
resident_pref(r15,h8). resident_pref(r15,h7). resident_pref(r15,h9).
resident_pref(r16,h8). resident_pref(r16,h7). resident_pref(r16,h9).
resident_pref(r17,h7). resident_pref(r17,h8). resident_pref(r17,h9).
resident_pref(r18,h7). resident_pref(r18,h9). resident_pref(r18,h8).
resident_pref(r19,h8). resident_pref(r19,h9). resident_pref(r19,h7).
resident_pref(r20,h9). resident_pref(r20,h8). resident_pref(r20,h7).

resident_pref(r21,h10). resident_pref(r21,h11). resident_pref(r21,h12).
resident_pref(r22,h10). resident_pref(r22,h12). resident_pref(r22,h11).
resident_pref(r23,h11). resident_pref(r23,h10). resident_pref(r23,h12).
resident_pref(r24,h11). resident_pref(r24,h12). resident_pref(r24,h10).
resident_pref(r25,h10). resident_pref(r25,h11). resident_pref(r25,h12).
resident_pref(r26,h11). resident_pref(r26,h10). resident_pref(r26,h12).
resident_pref(r27,h12). resident_pref(r27,h11). resident_pref(r27,h10).
resident_pref(r28,h12). resident_pref(r28,h10). resident_pref(r28,h11).

resident_pref(r29,h13). resident_pref(r29,h14). resident_pref(r29,h15).
resident_pref(r30,h13). resident_pref(r30,h15). resident_pref(r30,h14).
resident_pref(r31,h14). resident_pref(r31,h13). resident_pref(r31,h15).
resident_pref(r32,h14). resident_pref(r32,h15). resident_pref(r32,h13).
resident_pref(r33,h13). resident_pref(r33,h14). resident_pref(r33,h15).
resident_pref(r34,h14). resident_pref(r34,h13). resident_pref(r34,h15).
resident_pref(r35,h15). resident_pref(r35,h14). resident_pref(r35,h13).
resident_pref(r36,h15). resident_pref(r36,h13). resident_pref(r36,h14).

resident_pref(r37,h16). resident_pref(r37,h17).
resident_pref(r38,h16). resident_pref(r38,h17).
resident_pref(r39,h17). resident_pref(r39,h16).
resident_pref(r40,h17). resident_pref(r40,h16).

% Hospital preferences (ordered)
hospital_pref(h1,r3). hospital_pref(h1,r4). hospital_pref(h1,r1). hospital_pref(h1,r2).
hospital_pref(h2,r1). hospital_pref(h2,r2). hospital_pref(h2,r3). hospital_pref(h2,r4).

hospital_pref(h3,r7). hospital_pref(h3,r8). hospital_pref(h3,r5). hospital_pref(h3,r6).
hospital_pref(h4,r5). hospital_pref(h4,r6). hospital_pref(h4,r7). hospital_pref(h4,r8).

hospital_pref(h5,r11). hospital_pref(h5,r12). hospital_pref(h5,r9). hospital_pref(h5,r10).
hospital_pref(h6,r9). hospital_pref(h6,r10). hospital_pref(h6,r11). hospital_pref(h6,r12).

hospital_pref(h7,r13). hospital_pref(h7,r14). hospital_pref(h7,r17). hospital_pref(h7,r18). hospital_pref(h7,r15). hospital_pref(h7,r16). hospital_pref(h7,r19). hospital_pref(h7,r20).
hospital_pref(h8,r15). hospital_pref(h8,r16). hospital_pref(h8,r19). hospital_pref(h8,r13). hospital_pref(h8,r14). hospital_pref(h8,r17). hospital_pref(h8,r18). hospital_pref(h8,r20).
hospital_pref(h9,r20). hospital_pref(h9,r19). hospital_pref(h9,r18). hospital_pref(h9,r17). hospital_pref(h9,r16). hospital_pref(h9,r15). hospital_pref(h9,r14). hospital_pref(h9,r13).

hospital_pref(h10,r21). hospital_pref(h10,r22). hospital_pref(h10,r25). hospital_pref(h10,r23). hospital_pref(h10,r24). hospital_pref(h10,r26). hospital_pref(h10,r27). hospital_pref(h10,r28).
hospital_pref(h11,r23). hospital_pref(h11,r24). hospital_pref(h11,r26). hospital_pref(h11,r21). hospital_pref(h11,r22). hospital_pref(h11,r25). hospital_pref(h11,r27). hospital_pref(h11,r28).
hospital_pref(h12,r27). hospital_pref(h12,r28). hospital_pref(h12,r23). hospital_pref(h12,r24). hospital_pref(h12,r21). hospital_pref(h12,r22). hospital_pref(h12,r25). hospital_pref(h12,r26).

hospital_pref(h13,r29). hospital_pref(h13,r30). hospital_pref(h13,r33). hospital_pref(h13,r31). hospital_pref(h13,r32). hospital_pref(h13,r34). hospital_pref(h13,r35). hospital_pref(h13,r36).
hospital_pref(h14,r31). hospital_pref(h14,r32). hospital_pref(h14,r34). hospital_pref(h14,r29). hospital_pref(h14,r30). hospital_pref(h14,r33). hospital_pref(h14,r35). hospital_pref(h14,r36).
hospital_pref(h15,r35). hospital_pref(h15,r36). hospital_pref(h15,r31). hospital_pref(h15,r32). hospital_pref(h15,r29). hospital_pref(h15,r30). hospital_pref(h15,r33). hospital_pref(h15,r34).

hospital_pref(h16,r39). hospital_pref(h16,r40). hospital_pref(h16,r37). hospital_pref(h16,r38).
hospital_pref(h17,r37). hospital_pref(h17,r38). hospital_pref(h17,r39). hospital_pref(h17,r40).

% No preferences for h18-h20 (they have no acceptable residents)

% Define mutual acceptability
acceptable(R,H) :- resident_pref(R,H), hospital_pref(H,R).

% Rank for residents
resident_rank(r1,h1,1). resident_rank(r1,h2,2).
resident_rank(r2,h1,1). resident_rank(r2,h2,2).
resident_rank(r3,h2,1). resident_rank(r3,h1,2).
resident_rank(r4,h2,1). resident_rank(r4,h1,2).

resident_rank(r5,h3,1). resident_rank(r5,h4,2).
resident_rank(r6,h3,1). resident_rank(r6,h4,2).
resident_rank(r7,h4,1). resident_rank(r7,h3,2).
resident_rank(r8,h4,1). resident_rank(r8,h3,2).

resident_rank(r9,h5,1). resident_rank(r9,h6,2).
resident_rank(r10,h5,1). resident_rank(r10,h6,2).
resident_rank(r11,h6,1). resident_rank(r11,h5,2).
resident_rank(r12,h6,1). resident_rank(r12,h5,2).

resident_rank(r13,h7,1). resident_rank(r13,h8,2). resident_rank(r13,h9,3).
resident_rank(r14,h7,1). resident_rank(r14,h8,2). resident_rank(r14,h9,3).
resident_rank(r15,h8,1). resident_rank(r15,h7,2). resident_rank(r15,h9,3).
resident_rank(r16,h8,1). resident_rank(r16,h7,2). resident_rank(r16,h9,3).
resident_rank(r17,h7,1). resident_rank(r17,h8,2). resident_rank(r17,h9,3).
resident_rank(r18,h7,1). resident_rank(r18,h9,2). resident_rank(r18,h8,3).
resident_rank(r19,h8,1). resident_rank(r19,h9,2). resident_rank(r19,h7,3).
resident_rank(r20,h9,1). resident_rank(r20,h8,2). resident_rank(r20,h7,3).

resident_rank(r21,h10,1). resident_rank(r21,h11,2). resident_rank(r21,h12,3).
resident_rank(r22,h10,1). resident_rank(r22,h12,2). resident_rank(r22,h11,3).
resident_rank(r23,h11,1). resident_rank(r23,h10,2). resident_rank(r23,h12,3).
resident_rank(r24,h11,1). resident_rank(r24,h12,2). resident_rank(r24,h10,3).
resident_rank(r25,h10,1). resident_rank(r25,h11,2). resident_rank(r25,h12,3).
resident_rank(r26,h11,1). resident_rank(r26,h10,2). resident_rank(r26,h12,3).
resident_rank(r27,h12,1). resident_rank(r27,h11,2). resident_rank(r27,h10,3).
resident_rank(r28,h12,1). resident_rank(r28,h10,2). resident_rank(r28,h11,3).

resident_rank(r29,h13,1). resident_rank(r29,h14,2). resident_rank(r29,h15,3).
resident_rank(r30,h13,1). resident_rank(r30,h15,2). resident_rank(r30,h14,3).
resident_rank(r31,h14,1). resident_rank(r31,h13,2). resident_rank(r31,h15,3).
resident_rank(r32,h14,1). resident_rank(r32,h15,2). resident_rank(r32,h13,3).
resident_rank(r33,h13,1). resident_rank(r33,h14,2). resident_rank(r33,h15,3).
resident_rank(r34,h14,1). resident_rank(r34,h13,2). resident_rank(r34,h15,3).
resident_rank(r35,h15,1). resident_rank(r35,h14,2). resident_rank(r35,h13,3).
resident_rank(r36,h15,1). resident_rank(r36,h13,2). resident_rank(r36,h14,3).

resident_rank(r37,h16,1). resident_rank(r37,h17,2).
resident_rank(r38,h16,1). resident_rank(r38,h17,2).
resident_rank(r39,h17,1). resident_rank(r39,h16,2).
resident_rank(r40,h17,1). resident_rank(r40,h16,2).

% Rank for hospitals
hospital_rank(h1,r3,1). hospital_rank(h1,r4,2). hospital_rank(h1,r1,3). hospital_rank(h1,r2,4).
hospital_rank(h2,r1,1). hospital_rank(h2,r2,2). hospital_rank(h2,r3,3). hospital_rank(h2,r4,4).

hospital_rank(h3,r7,1). hospital_rank(h3,r8,2). hospital_rank(h3,r5,3). hospital_rank(h3,r6,4).
hospital_rank(h4,r5,1). hospital_rank(h4,r6,2). hospital_rank(h4,r7,3). hospital_rank(h4,r8,4).

hospital_rank(h5,r11,1). hospital_rank(h5,r12,2). hospital_rank(h5,r9,3). hospital_rank(h5,r10,4).
hospital_rank(h6,r9,1). hospital_rank(h6,r10,2). hospital_rank(h6,r11,3). hospital_rank(h6,r12,4).

hospital_rank(h7,r13,1). hospital_rank(h7,r14,2). hospital_rank(h7,r17,3). hospital_rank(h7,r18,4). hospital_rank(h7,r15,5). hospital_rank(h7,r16,6). hospital_rank(h7,r19,7). hospital_rank(h7,r20,8).
hospital_rank(h8,r15,1). hospital_rank(h8,r16,2). hospital_rank(h8,r19,3). hospital_rank(h8,r13,4). hospital_rank(h8,r14,5). hospital_rank(h8,r17,6). hospital_rank(h8,r18,7). hospital_rank(h8,r20,8).
hospital_rank(h9,r20,1). hospital_rank(h9,r19,2). hospital_rank(h9,r18,3). hospital_rank(h9,r17,4). hospital_rank(h9,r16,5). hospital_rank(h9,r15,6). hospital_rank(h9,r14,7). hospital_rank(h9,r13,8).

hospital_rank(h10,r21,1). hospital_rank(h10,r22,2). hospital_rank(h10,r25,3). hospital_rank(h10,r23,4). hospital_rank(h10,r24,5). hospital_rank(h10,r26,6). hospital_rank(h10,r27,7). hospital_rank(h10,r28,8).
hospital_rank(h11,r23,1). hospital_rank(h11,r24,2). hospital_rank(h11,r26,3). hospital_rank(h11,r21,4). hospital_rank(h11,r22,5). hospital_rank(h11,r25,6). hospital_rank(h11,r27,7). hospital_rank(h11,r28,8).
hospital_rank(h12,r27,1). hospital_rank(h12,r28,2). hospital_rank(h12,r23,3). hospital_rank(h12,r24,4). hospital_rank(h12,r21,5). hospital_rank(h12,r22,6). hospital_rank(h12,r25,7). hospital_rank(h12,r26,8).

hospital_rank(h13,r29,1). hospital_rank(h13,r30,2). hospital_rank(h13,r33,3). hospital_rank(h13,r31,4). hospital_rank(h13,r32,5). hospital_rank(h13,r34,6). hospital_rank(h13,r35,7). hospital_rank(h13,r36,8).
hospital_rank(h14,r31,1). hospital_rank(h14,r32,2). hospital_rank(h14,r34,3). hospital_rank(h14,r29,4). hospital_rank(h14,r30,5). hospital_rank(h14,r33,6). hospital_rank(h14,r35,7). hospital_rank(h14,r36,8).
hospital_rank(h15,r35,1). hospital_rank(h15,r36,2). hospital_rank(h15,r31,3). hospital_rank(h15,r32,4). hospital_rank(h15,r29,5). hospital_rank(h15,r30,6). hospital_rank(h15,r33,7). hospital_rank(h15,r34,8).

hospital_rank(h16,r39,1). hospital_rank(h16,r40,2). hospital_rank(h16,r37,3). hospital_rank(h16,r38,4).
hospital_rank(h17,r37,1). hospital_rank(h17,r38,2). hospital_rank(h17,r39,3). hospital_rank(h17,r40,4).

% Choice: each resident assigned to exactly one acceptable hospital
1 { assign(R,H) : acceptable(R,H) } 1 :- resident(R).

% Capacity constraint
:- cap(H,Cap), #count{R : assign(R,H)} > Cap.

% Preference helpers
resident_prefers(R,H1,H2) :- resident_rank(R,H1,RK1), resident_rank(R,H2,RK2), RK1 < RK2.

hospital_prefers(H,R1,R2) :- hospital_rank(H,R1,RK1), hospital_rank(H,R2,RK2), RK1 < RK2.

% Resident's current assignment
assigned_hospital(R,H) :- assign(R,H).

% Resident prefers some other hospital over current
resident_prefers_over_assigned(R,H) :- assign(R,HC), resident_prefers(R,H,HC).

% Hospital has free slot
hospital_has_free_slot(H) :- cap(H,Cap), #count{R : assign(R,H)} < Cap.

% Hospital prefers resident over at least one current assignee
hospital_prefers_over_some(R,H) :- assign(R2,H), hospital_prefers(H,R,R2).

% Blocking pair constraints
:- resident_prefers_over_assigned(R,H), hospital_has_free_slot(H).
:- resident_prefers_over_assigned(R,H), hospital_prefers_over_some(R,H).

% Show assignments
#show assign/2.