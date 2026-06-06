% ============================================
% Quantum Circuit Compilation with Topology
% ============================================

% ---- Domain: Qubits ----
qubit(q0). qubit(q1). qubit(q2). qubit(q3).
qubit(q4). qubit(q5). qubit(q6). qubit(q7).

% ---- Topology: 2x4 Grid Adjacency ----
adjacent(q0, q1). adjacent(q1, q2). adjacent(q2, q3).
adjacent(q4, q5). adjacent(q5, q6). adjacent(q6, q7).
adjacent(q0, q4). adjacent(q1, q5). adjacent(q2, q6). adjacent(q3, q7).
adjacent(Q2, Q1) :- adjacent(Q1, Q2).

% ---- Gates ----
gate(h_q0).
gate(x_q1).
gate(cnot_q2_q3).
gate(cnot_q4_q5).
gate(cnot_q0_q2).
gate(toffoli_q5_q7_q6).

% Gate types and qubit assignments
single_qubit_gate(h_q0, q0).
single_qubit_gate(x_q1, q1).

cnot_gate(cnot_q2_q3, q2, q3).
cnot_gate(cnot_q4_q5, q4, q5).
cnot_gate(cnot_q0_q2, q0, q2).

toffoli_gate(toffoli_q5_q7_q6, q5, q7, q6).

% Which qubits does each gate use?
uses_qubit(G, Q) :- single_qubit_gate(G, Q).
uses_qubit(G, Q) :- cnot_gate(G, Q, _).
uses_qubit(G, Q) :- cnot_gate(G, _, Q).
uses_qubit(G, Q) :- toffoli_gate(G, Q, _, _).
uses_qubit(G, Q) :- toffoli_gate(G, _, Q, _).
uses_qubit(G, Q) :- toffoli_gate(G, _, _, Q).

% ---- Dependencies ----
depends(toffoli_q5_q7_q6, cnot_q4_q5).

% ---- Time Horizon ----
time(0..6).

% ---- Schedule: Each gate at exactly one time step (1-indexed) ----
1 { scheduled(G, T) : time(T), T > 0 } 1 :- gate(G).

% ---- SWAP gates: between adjacent qubits at each time step ----
{ swap(Q1, Q2, T) : adjacent(Q1, Q2), Q1 < Q2 } :- time(T), T > 0.

% ---- Logical-to-physical mapping ----
% At time 0, logical qubit Q is at physical position Q
at(Q, Q, 0) :- qubit(Q).

% After a SWAP at time T, positions are exchanged for time T
% If swap(P1,P2) at time T, then whatever was at P1 goes to P2 and vice versa
at(Q1, P2, T) :- swap(P1, P2, T), at(Q1, P1, T-1), time(T), T > 0.
at(Q2, P1, T) :- swap(P1, P2, T), at(Q2, P2, T-1), time(T), T > 0.

% Persistence: position stays if no swap involving that position at this time
at(Q, P, T) :- at(Q, P, T-1), time(T), T > 0,
                not swap(P, _, T-1), not swap(_, P, T-1).

% ---- Qubit usage tracking ----
qubit_used(Q, T) :- scheduled(G, T), uses_qubit(G, Q).

% ---- Constraint: No qubit conflicts ----
:- time(T), T > 0, qubit(Q), 2 { scheduled(G, T) : uses_qubit(G, Q) }.

% ---- Topology Constraint for Multi-qubit Gates (with SWAP support) ----
% CNOT gates require adjacent qubits considering current physical positions
:- cnot_gate(G, C, Target), scheduled(G, T),
   at(C, PC, T-1), at(Target, PT, T-1),
   not adjacent(PC, PT).

% Toffoli gates require both controls adjacent to target
:- toffoli_gate(G, C1, C2, Target), scheduled(G, T),
   at(C1, P1, T-1), at(Target, PT, T-1),
   not adjacent(P1, PT).
:- toffoli_gate(G, C1, C2, Target), scheduled(G, T),
   at(C2, P2, T-1), at(Target, PT, T-1),
   not adjacent(P2, PT).

% ---- Dependency Ordering ----
:- depends(G1, G2), scheduled(G1, T1), scheduled(G2, T2), T1 <= T2.

% ---- Count SWAPs ----
swap_count(N) :- N = #count{Q1, Q2, T : swap(Q1, Q2, T)}.

% ---- Circuit Depth: latest time step used ----
used_time(T) :- scheduled(_, T).
circuit_depth(D) :- D = #max{T : used_time(T)}.

% ---- Optimization ----
#minimize { D : circuit_depth(D) }.
#minimize { N : swap_count(N) }.

% ---- Output ----
#show scheduled/2.
#show swap/3.
#show circuit_depth/1.
#show swap_count/1.