% --- Domain ---
time(1..4).
logical_qubit(q0; q1; q2; q3; q4; q5; q6; q7).
physical_qubit(q0; q1; q2; q3; q4; q5; q6; q7).

% Topology
adj(q0,q1). adj(q1,q2). adj(q2,q3).
adj(q4,q5). adj(q5,q6). adj(q6,q7).
adj(q0,q4). adj(q1,q5). adj(q2,q6). adj(q3,q7).
adj(Y,X) :- adj(X,Y).

% Gates
gate(h_q0, 1, q0).
gate(x_q1, 1, q1).
gate(cnot_q2_q3, 2, q2, q3).
gate(cnot_q4_q5, 2, q4, q5).
gate(cnot_q0_q2, 2, q0, q2).
gate(toffoli_q5_q7_q6, 3, q5, q7, q6).

% Dependencies
dependency(toffoli_q5_q7_q6, cnot_q4_q5).

% --- State ---
% pos(Lq, Pq, T)
% Initial positions
pos(Lq, Lq, 0) :- logical_qubit(Lq).

% --- Actions ---
{ execute(G, T) : gate(G, _, _) } :- time(T).
{ execute(G, T) : gate(G, _, _, _) } :- time(T).
{ execute(G, T) : gate(G, _, _, _, _) } :- time(T).
{ swap(P1, P2, T) : adj(P1, P2), P1 < P2 } :- time(T).

% Constraints
% 1. Each gate executed exactly once
:- gate(G, 1, _), not 1 { execute(G, T) : time(T) } 1.
:- gate(G, 2, _, _), not 1 { execute(G, T) : time(T) } 1.
:- gate(G, 3, _, _, _), not 1 { execute(G, T) : time(T) } 1.

% 2. Dependency
:- execute(G1, T1), execute(G2, T2), dependency(G1, G2), T1 <= T2.

% 3. Adjacency for gates
% Single qubit
:- execute(G, T), gate(G, 1, Lq), pos(Lq, Pq, T-1).
% CNOT (Lq1, Lq2)
:- execute(G, T), gate(G, 2, Lq1, Lq2), pos(Lq1, P1, T-1), pos(Lq2, P2, T-1), not adj(P1, P2).
% Toffoli (Lq1, Lq2, Lq3)
:- execute(G, T), gate(G, 3, Lq1, Lq2, Lq3), pos(Lq1, P1, T-1), pos(Lq2, P2, T-1), pos(Lq3, P3, T-1), not adj(P1, P3), not adj(P2, P3).

% 4. Qubit conflicts
used_p(P, T) :- execute(G, T), gate(G, 1, Lq), pos(Lq, P, T-1).
used_p(P, T) :- execute(G, T), gate(G, 2, Lq1, Lq2), pos(Lq1, P, T-1).
used_p(P, T) :- execute(G, T), gate(G, 2, Lq1, Lq2), pos(Lq2, P, T-1).
used_p(P, T) :- execute(G, T), gate(G, 3, Lq1, Lq2, Lq3), pos(Lq1, P, T-1).
used_p(P, T) :- execute(G, T), gate(G, 3, Lq1, Lq2, Lq3), pos(Lq2, P, T-1).
used_p(P, T) :- execute(G, T), gate(G, 3, Lq1, Lq2, Lq3), pos(Lq3, P, T-1).
used_p(P, T) :- swap(P1, P2, T), (P=P1; P=P2).
:- used_p(P, T), #count { 1 : used_p(P, T) } > 1.

% 5. State transition
moved(Lq, T) :- swap(P1, P2, T), pos(Lq, P, T-1), (P=P1; P=P2).
pos(Lq, P2, T) :- swap(P1, P2, T), pos(Lq, P1, T-1).
pos(Lq, P1, T) :- swap(P1, P2, T), pos(Lq, P2, T-1).
pos(Lq, P, T) :- pos(Lq, P, T-1), not moved(Lq, T), time(T).

% --- Optimization ---
depth(D) :- D = #max { T : execute(G, T) }.
#minimize { D : depth(D) }.
#minimize { 1, P1, P2, T : swap(P1, P2, T) }.

#show execute/2.
#show swap/3.
#show depth/1.