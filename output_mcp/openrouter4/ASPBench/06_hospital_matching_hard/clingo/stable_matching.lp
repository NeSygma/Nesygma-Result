%%% DOMAIN DEFINITIONS %%%
resident(r1;r2;r3;r4;r5;r6;r7;r8;r9;r10;r11;r12;r13;r14;r15;r16;r17;r18;r19;r20).
resident(r21;r22;r23;r24;r25;r26;r27;r28;r29;r30;r31;r32;r33;r34;r35;r36;r37;r38;r39;r40).

hospital(h1;h2;h3;h4;h5;h6;h7;h8;h9;h10;h11;h12;h13;h14;h15;h16;h17;h18;h19;h20).

capacity(h1,2). capacity(h2,2). capacity(h3,2). capacity(h4,2). capacity(h5,2). capacity(h6,2).
capacity(h7,4). capacity(h8,3). capacity(h9,1).
capacity(h10,3). capacity(h11,3). capacity(h12,2).
capacity(h13,3). capacity(h14,3). capacity(h15,2).
capacity(h16,2). capacity(h17,2).
capacity(h18,1). capacity(h19,1). capacity(h20,1).

%%% RESIDENT PREFERENCES %%%
% Block A1
pref_resident(r1,h1,1). pref_resident(r1,h2,2).
pref_resident(r2,h1,1). pref_resident(r2,h2,2).
pref_resident(r3,h2,1). pref_resident(r3,h1,2).
pref_resident(r4,h2,1). pref_resident(r4,h1,2).

% Block A2
pref_resident(r5,h3,1). pref_resident(r5,h4,2).
pref_resident(r6,h3,1). pref_resident(r6,h4,2).
pref_resident(r7,h4,1). pref_resident(r7,h3,2).
pref_resident(r8,h4,1). pref_resident(r8,h3,2).

% Block A3
pref_resident(r9,h5,1). pref_resident(r9,h6,2).
pref_resident(r10,h5,1). pref_resident(r10,h6,2).
pref_resident(r11,h6,1). pref_resident(r11,h5,2).
pref_resident(r12,h6,1). pref_resident(r12,h5,2).

% Block B1
pref_resident(r13,h7,1). pref_resident(r13,h8,2). pref_resident(r13,h9,3).
pref_resident(r14,h7,1). pref_resident(r14,h8,2). pref_resident(r14,h9,3).
pref_resident(r15,h8,1). pref_resident(r15,h7,2). pref_resident(r15,h9,3).
pref_resident(r16,h8,1). pref_resident(r16,h7,2). pref_resident(r16,h9,3).
pref_resident(r17,h7,1). pref_resident(r17,h8,2). pref_resident(r17,h9,3).
pref_resident(r18,h7,1). pref_resident(r18,h9,2). pref_resident(r18,h8,3).
pref_resident(r19,h8,1). pref_resident(r19,h9,2). pref_resident(r19,h7,3).
pref_resident(r20,h9,1). pref_resident(r20,h8,2). pref_resident(r20,h7,3).

% Block B2
pref_resident(r21,h10,1). pref_resident(r21,h11,2). pref_resident(r21,h12,3).
pref_resident(r22,h10,1). pref_resident(r22,h12,2). pref_resident(r22,h11,3).
pref_resident(r23,h11,1). pref_resident(r23,h10,2). pref_resident(r23,h12,3).
pref_resident(r24,h11,1). pref_resident(r24,h12,2). pref_resident(r24,h10,3).
pref_resident(r25,h10,1). pref_resident(r25,h11,2). pref_resident(r25,h12,3).
pref_resident(r26,h11,1). pref_resident(r26,h10,2). pref_resident(r26,h12,3).
pref_resident(r27,h12,1). pref_resident(r27,h11,2). pref_resident(r27,h10,3).
pref_resident(r28,h12,1). pref_resident(r28,h10,2). pref_resident(r28,h11,3).

% Block B3
pref_resident(r29,h13,1). pref_resident(r29,h14,2). pref_resident(r29,h15,3).
pref_resident(r30,h13,1). pref_resident(r30,h15,2). pref_resident(r30,h14,3).
pref_resident(r31,h14,1). pref_resident(r31,h13,2). pref_resident(r31,h15,3).
pref_resident(r32,h14,1). pref_resident(r32,h15,2). pref_resident(r32,h13,3).
pref_resident(r33,h13,1). pref_resident(r33,h14,2). pref_resident(r33,h15,3).
pref_resident(r34,h14,1). pref_resident(r34,h13,2). pref_resident(r34,h15,3).
pref_resident(r35,h15,1). pref_resident(r35,h14,2). pref_resident(r35,h13,3).
pref_resident(r36,h15,1). pref_resident(r36,h13,2). pref_resident(r36,h14,3).

% Block A4
pref_resident(r37,h16,1). pref_resident(r37,h17,2).
pref_resident(r38,h16,1). pref_resident(r38,h17,2).
pref_resident(r39,h17,1). pref_resident(r39,h16,2).
pref_resident(r40,h17,1). pref_resident(r40,h16,2).

%%% HOSPITAL PREFERENCES %%%
% Block A1
pref_hospital(h1,r3,1). pref_hospital(h1,r4,2). pref_hospital(h1,r1,3). pref_hospital(h1,r2,4).
pref_hospital(h2,r1,1). pref_hospital(h2,r2,2). pref_hospital(h2,r3,3). pref_hospital(h2,r4,4).

% Block A2
pref_hospital(h3,r7,1). pref_hospital(h3,r8,2). pref_hospital(h3,r5,3). pref_hospital(h3,r6,4).
pref_hospital(h4,r5,1). pref_hospital(h4,r6,2). pref_hospital(h4,r7,3). pref_hospital(h4,r8,4).

% Block A3
pref_hospital(h5,r11,1). pref_hospital(h5,r12,2). pref_hospital(h5,r9,3). pref_hospital(h5,r10,4).
pref_hospital(h6,r9,1). pref_hospital(h6,r10,2). pref_hospital(h6,r11,3). pref_hospital(h6,r12,4).

% Block B1
pref_hospital(h7,r13,1). pref_hospital(h7,r14,2). pref_hospital(h7,r17,3). pref_hospital(h7,r18,4).
pref_hospital(h7,r15,5). pref_hospital(h7,r16,6). pref_hospital(h7,r19,7). pref_hospital(h7,r20,8).

pref_hospital(h8,r15,1). pref_hospital(h8,r16,2). pref_hospital(h8,r19,3). pref_hospital(h8,r13,4).
pref_hospital(h8,r14,5). pref_hospital(h8,r17,6). pref_hospital(h8,r18,7). pref_hospital(h8,r20,8).

pref_hospital(h9,r20,1). pref_hospital(h9,r19,2). pref_hospital(h9,r18,3). pref_hospital(h9,r17,4).
pref_hospital(h9,r16,5). pref_hospital(h9,r15,6). pref_hospital(h9,r14,7). pref_hospital(h9,r13,8).

% Block B2
pref_hospital(h10,r21,1). pref_hospital(h10,r22,2). pref_hospital(h10,r25,3). pref_hospital(h10,r23,4).
pref_hospital(h10,r24,5). pref_hospital(h10,r26,6). pref_hospital(h10,r27,7). pref_hospital(h10,r28,8).

pref_hospital(h11,r23,1). pref_hospital(h11,r24,2). pref_hospital(h11,r26,3). pref_hospital(h11,r21,4).
pref_hospital(h11,r22,5). pref_hospital(h11,r25,6). pref_hospital(h11,r27,7). pref_hospital(h11,r28,8).

pref_hospital(h12,r27,1). pref_hospital(h12,r28,2). pref_hospital(h12,r23,3). pref_hospital(h12,r24,4).
pref_hospital(h12,r21,5). pref_hospital(h12,r22,6). pref_hospital(h12,r25,7). pref_hospital(h12,r26,8).

% Block B3
pref_hospital(h13,r29,1). pref_hospital(h13,r30,2). pref_hospital(h13,r33,3). pref_hospital(h13,r31,4).
pref_hospital(h13,r32,5). pref_hospital(h13,r34,6). pref_hospital(h13,r35,7). pref_hospital(h13,r36,8).

pref_hospital(h14,r31,1). pref_hospital(h14,r32,2). pref_hospital(h14,r34,3). pref_hospital(h14,r29,4).
pref_hospital(h14,r30,5). pref_hospital(h14,r33,6). pref_hospital(h14,r35,7). pref_hospital(h14,r36,8).

pref_hospital(h15,r35,1). pref_hospital(h15,r36,2). pref_hospital(h15,r31,3). pref_hospital(h15,r32,4).
pref_hospital(h15,r29,5). pref_hospital(h15,r30,6). pref_hospital(h15,r33,7). pref_hospital(h15,r34,8).

% Block A4
pref_hospital(h16,r39,1). pref_hospital(h16,r40,2). pref_hospital(h16,r37,3). pref_hospital(h16,r38,4).
pref_hospital(h17,r37,1). pref_hospital(h17,r38,2). pref_hospital(h17,r39,3). pref_hospital(h17,r40,4).

%%% MUTUAL ACCEPTABILITY %%%
acceptable(R, H) :- pref_resident(R, H, _), pref_hospital(H, R, _).

%%% MATCHING CHOICES: each resident can be matched to at most one acceptable hospital %%%
{ match(R, H) } :- acceptable(R, H).

% Each resident matched to at most one hospital
:- resident(R), #count{H : match(R, H)} > 1.

%%% CAPACITY CONSTRAINTS %%%
% Count assigned residents per hospital
assigned_count(H, N) :- hospital(H), N = #count{R : match(R, H)}.

% Enforce capacity
:- hospital(H), capacity(H, C), assigned_count(H, N), N > C.

%%% STABILITY AUXILIARIES %%%

% Currently unmatched resident
unmatched(R) :- resident(R), not match(R, _).

% Hospital has free capacity (not full)
free_cap(H) :- hospital(H), capacity(H, C), assigned_count(H, N), N < C.

% Resident R prefers hospital H over their current assignment Hc
r_prefers(R, H) :- match(R, Hc), pref_resident(R, H, Pr), pref_resident(R, Hc, Pc), Pr < Pc.

% Hospital H prefers resident R over at least one current assignee Rc
h_prefers(R, H) :- match(Rc, H), pref_hospital(H, R, Pr), pref_hospital(H, Rc, Pc), Pr < Pc.

% Blocking pair: (R, H) where R is not matched to H
blocking(R, H) :- acceptable(R, H), not match(R, H),
                  (unmatched(R) ; r_prefers(R, H)),
                  (free_cap(H) ; h_prefers(R, H)).

%%% FORBID BLOCKING PAIRS %%%
:- blocking(R, H).

%%% OUTPUT ALL MATCHINGS %%%
#show match/2.