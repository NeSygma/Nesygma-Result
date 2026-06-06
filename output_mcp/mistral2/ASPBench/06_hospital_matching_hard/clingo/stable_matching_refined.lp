% Declarations
resident(r1..r40).
hospital(h1..h20).

% Hospital capacities
capacity(h1, 2). capacity(h2, 2). capacity(h3, 2). capacity(h4, 2). capacity(h5, 2). capacity(h6, 2).
capacity(h7, 4). capacity(h8, 3). capacity(h9, 1).
capacity(h10, 3). capacity(h11, 3). capacity(h12, 2).
capacity(h13, 3). capacity(h14, 3). capacity(h15, 2).
capacity(h16, 2). capacity(h17, 2).
capacity(h18, 1). capacity(h19, 1). capacity(h20, 1).

% Resident preferences (only acceptable hospitals listed, in order of preference)
% Block A1 (r1-r4)
prefers_hospital(r1, h1, h2).
prefers_hospital(r2, h1, h2).
prefers_hospital(r3, h2, h1).
prefers_hospital(r4, h2, h1).

% Block A2 (r5-r8)
prefers_hospital(r5, h3, h4).
prefers_hospital(r6, h3, h4).
prefers_hospital(r7, h4, h3).
prefers_hospital(r8, h4, h3).

% Block A3 (r9-r12)
prefers_hospital(r9, h5, h6).
prefers_hospital(r10, h5, h6).
prefers_hospital(r11, h6, h5).
prefers_hospital(r12, h6, h5).

% Block B1 (r13-r20)
prefers_hospital(r13, h7, h8). prefers_hospital(r13, h8, h9).
prefers_hospital(r14, h7, h8). prefers_hospital(r14, h8, h9).
prefers_hospital(r15, h8, h7). prefers_hospital(r15, h7, h9).
prefers_hospital(r16, h8, h7). prefers_hospital(r16, h7, h9).
prefers_hospital(r17, h7, h8). prefers_hospital(r17, h8, h9).
prefers_hospital(r18, h7, h9). prefers_hospital(r18, h9, h8).
prefers_hospital(r19, h8, h9). prefers_hospital(r19, h9, h7).
prefers_hospital(r20, h9, h8). prefers_hospital(r20, h8, h7).

% Block B2 (r21-r28)
prefers_hospital(r21, h10, h11). prefers_hospital(r21, h11, h12).
prefers_hospital(r22, h10, h12). prefers_hospital(r22, h12, h11).
prefers_hospital(r23, h11, h10). prefers_hospital(r23, h10, h12).
prefers_hospital(r24, h11, h12). prefers_hospital(r24, h12, h10).
prefers_hospital(r25, h10, h11). prefers_hospital(r25, h11, h12).
prefers_hospital(r26, h11, h10). prefers_hospital(r26, h10, h12).
prefers_hospital(r27, h12, h11). prefers_hospital(r27, h11, h10).
prefers_hospital(r28, h12, h10). prefers_hospital(r28, h10, h11).

% Block B3 (r29-r36)
prefers_hospital(r29, h13, h14). prefers_hospital(r29, h14, h15).
prefers_hospital(r30, h13, h15). prefers_hospital(r30, h15, h14).
prefers_hospital(r31, h14, h13). prefers_hospital(r31, h13, h15).
prefers_hospital(r32, h14, h15). prefers_hospital(r32, h15, h13).
prefers_hospital(r33, h13, h14). prefers_hospital(r33, h14, h15).
prefers_hospital(r34, h14, h13). prefers_hospital(r34, h13, h15).
prefers_hospital(r35, h15, h14). prefers_hospital(r35, h14, h13).
prefers_hospital(r36, h15, h13). prefers_hospital(r36, h13, h14).

% Block A4 (r37-r40)
prefers_hospital(r37, h16, h17).
prefers_hospital(r38, h16, h17).
prefers_hospital(r39, h17, h16).
prefers_hospital(r40, h17, h16).

% Hospital preferences (only acceptable residents listed, in order of preference)
% Block A1
prefers_resident(h1, r3, r4). prefers_resident(h1, r4, r1). prefers_resident(h1, r1, r2).
prefers_resident(h2, r1, r2). prefers_resident(h2, r2, r3). prefers_resident(h2, r3, r4).

% Block A2
prefers_resident(h3, r7, r8). prefers_resident(h3, r8, r5). prefers_resident(h3, r5, r6).
prefers_resident(h4, r5, r6). prefers_resident(h4, r6, r7). prefers_resident(h4, r7, r8).

% Block A3
prefers_resident(h5, r11, r12). prefers_resident(h5, r12, r9). prefers_resident(h5, r9, r10).
prefers_resident(h6, r9, r10). prefers_resident(h6, r10, r11). prefers_resident(h6, r11, r12).

% Block B1
prefers_resident(h7, r13, r14). prefers_resident(h7, r14, r17). prefers_resident(h7, r17, r18). prefers_resident(h7, r18, r15). prefers_resident(h7, r15, r16). prefers_resident(h7, r16, r19). prefers_resident(h7, r19, r20).
prefers_resident(h8, r15, r16). prefers_resident(h8, r16, r19). prefers_resident(h8, r19, r13). prefers_resident(h8, r13, r14). prefers_resident(h8, r14, r17). prefers_resident(h8, r17, r18). prefers_resident(h8, r18, r20).
prefers_resident(h9, r20, r19). prefers_resident(h9, r19, r18). prefers_resident(h9, r18, r17). prefers_resident(h9, r17, r16). prefers_resident(h9, r16, r15). prefers_resident(h9, r15, r14). prefers_resident(h9, r14, r13).

% Block B2
prefers_resident(h10, r21, r22). prefers_resident(h10, r22, r25). prefers_resident(h10, r25, r23). prefers_resident(h10, r23, r24). prefers_resident(h10, r24, r26). prefers_resident(h10, r26, r27). prefers_resident(h10, r27, r28).
prefers_resident(h11, r23, r24). prefers_resident(h11, r24, r26). prefers_resident(h11, r26, r21). prefers_resident(h11, r21, r22). prefers_resident(h11, r22, r25). prefers_resident(h11, r25, r27). prefers_resident(h11, r27, r28).
prefers_resident(h12, r27, r28). prefers_resident(h12, r28, r23). prefers_resident(h12, r23, r24). prefers_resident(h12, r24, r21). prefers_resident(h12, r21, r22). prefers_resident(h12, r22, r25). prefers_resident(h12, r25, r26).

% Block B3
prefers_resident(h13, r29, r30). prefers_resident(h13, r30, r33). prefers_resident(h13, r33, r31). prefers_resident(h13, r31, r32). prefers_resident(h13, r32, r34). prefers_resident(h13, r34, r35). prefers_resident(h13, r35, r36).
prefers_resident(h14, r31, r32). prefers_resident(h14, r32, r34). prefers_resident(h14, r34, r29). prefers_resident(h14, r29, r30). prefers_resident(h14, r30, r33). prefers_resident(h14, r33, r35). prefers_resident(h14, r35, r36).
prefers_resident(h15, r35, r36). prefers_resident(h15, r36, r31). prefers_resident(h15, r31, r32). prefers_resident(h15, r32, r29). prefers_resident(h15, r29, r30). prefers_resident(h15, r30, r33). prefers_resident(h15, r33, r34).

% Block A4
prefers_resident(h16, r39, r40). prefers_resident(h16, r40, r37). prefers_resident(h16, r37, r38).
prefers_resident(h17, r37, r38). prefers_resident(h17, r38, r39). prefers_resident(h17, r39, r40).

% Mutual acceptability (only pairs where both find each other acceptable)
% Block A1
acceptable(r1, h1). acceptable(r1, h2).
acceptable(r2, h1). acceptable(r2, h2).
acceptable(r3, h1). acceptable(r3, h2).
acceptable(r4, h1). acceptable(r4, h2).

% Block A2
acceptable(r5, h3). acceptable(r5, h4).
acceptable(r6, h3). acceptable(r6, h4).
acceptable(r7, h3). acceptable(r7, h4).
acceptable(r8, h3). acceptable(r8, h4).

% Block A3
acceptable(r9, h5). acceptable(r9, h6).
acceptable(r10, h5). acceptable(r10, h6).
acceptable(r11, h5). acceptable(r11, h6).
acceptable(r12, h5). acceptable(r12, h6).

% Block B1
acceptable(r13, h7). acceptable(r13, h8). acceptable(r13, h9).
acceptable(r14, h7). acceptable(r14, h8). acceptable(r14, h9).
acceptable(r15, h7). acceptable(r15, h8). acceptable(r15, h9).
acceptable(r16, h7). acceptable(r16, h8). acceptable(r16, h9).
acceptable(r17, h7). acceptable(r17, h8). acceptable(r17, h9).
acceptable(r18, h7). acceptable(r18, h8). acceptable(r18, h9).
acceptable(r19, h7). acceptable(r19, h8). acceptable(r19, h9).
acceptable(r20, h7). acceptable(r20, h8). acceptable(r20, h9).

% Block B2
acceptable(r21, h10). acceptable(r21, h11). acceptable(r21, h12).
acceptable(r22, h10). acceptable(r22, h11). acceptable(r22, h12).
acceptable(r23, h10). acceptable(r23, h11). acceptable(r23, h12).
acceptable(r24, h10). acceptable(r24, h11). acceptable(r24, h12).
acceptable(r25, h10). acceptable(r25, h11). acceptable(r25, h12).
acceptable(r26, h10). acceptable(r26, h11). acceptable(r26, h12).
acceptable(r27, h10). acceptable(r27, h11). acceptable(r27, h12).
acceptable(r28, h10). acceptable(r28, h11). acceptable(r28, h12).

% Block B3
acceptable(r29, h13). acceptable(r29, h14). acceptable(r29, h15).
acceptable(r30, h13). acceptable(r30, h14). acceptable(r30, h15).
acceptable(r31, h13). acceptable(r31, h14). acceptable(r31, h15).
acceptable(r32, h13). acceptable(r32, h14). acceptable(r32, h15).
acceptable(r33, h13). acceptable(r33, h14). acceptable(r33, h15).
acceptable(r34, h13). acceptable(r34, h14). acceptable(r34, h15).
acceptable(r35, h13). acceptable(r35, h14). acceptable(r35, h15).
acceptable(r36, h13). acceptable(r36, h14). acceptable(r36, h15).

% Block A4
acceptable(r37, h16). acceptable(r37, h17).
acceptable(r38, h16). acceptable(r38, h17).
acceptable(r39, h16). acceptable(r39, h17).
acceptable(r40, h16). acceptable(r40, h17).

% Choice rule: Assign residents to hospitals
{ assigned(R, H) : hospital(H) } 1 :- resident(R).

% Constraints
% 1. Capacity constraint
:- capacity(H, C), #count{R: assigned(R, H)} > C.

% 2. Mutual acceptability constraint
:- assigned(R, H), not acceptable(R, H).

% 3. Stability constraint: No blocking pair (R, H)
% A blocking pair (R, H) exists if:
%   - R is unmatched or prefers H over their current assignment
%   - H has free capacity or prefers R over at least one current assignee

% Helper: Current assignment of R
current_assignment(R, H) :- assigned(R, H).

% Helper: R prefers H1 over H2
resident_prefers(R, H1, H2) :- prefers_hospital(R, H1, H2).

% Helper: H prefers R1 over R2
hospital_prefers(H, R1, R2) :- prefers_resident(H, R1, R2).

% Check for blocking pairs
% Case 1: R is unmatched and H has free capacity or prefers R over someone
blocking_pair(R, H) :-
    resident(R),
    hospital(H),
    not assigned(R, _),
    capacity(H, C),
    #count{R2: assigned(R2, H)} < C.

blocking_pair(R, H) :-
    resident(R),
    hospital(H),
    not assigned(R, _),
    capacity(H, C),
    #count{R2: assigned(R2, H)} = C,
    hospital_prefers(H, R, R2),
    assigned(R2, H).

% Case 2: R is matched to H' but prefers H over H', and H has free capacity or prefers R over someone
blocking_pair(R, H) :-
    resident(R),
    hospital(H),
    hospital(H2),
    assigned(R, H2),
    resident_prefers(R, H, H2),
    capacity(H, C),
    #count{R2: assigned(R2, H)} < C.

blocking_pair(R, H) :-
    resident(R),
    hospital(H),
    hospital(H2),
    assigned(R, H2),
    resident_prefers(R, H, H2),
    capacity(H, C),
    #count{R2: assigned(R2, H)} = C,
    hospital_prefers(H, R, R2),
    assigned(R2, H).

% Eliminate all assignments that allow a blocking pair
:- blocking_pair(R, H).

% Output
#show assigned/2.