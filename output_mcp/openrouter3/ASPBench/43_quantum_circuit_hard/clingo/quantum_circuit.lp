% Quantum Circuit Scheduling with Topology Constraints

% ==================== DOMAIN DEFINITIONS ====================
% Qubits
qubit(q0). qubit(q1). qubit(q2). qubit(q3).
qubit(q4). qubit(q5). qubit(q6). qubit(q7).

% Time horizon (we'll start with a reasonable bound)
time(1..10).

% ==================== TOPOLOGY DEFINITIONS ====================
% Adjacency in 2x4 grid
adjacent(q0, q1). adjacent(q1, q0).
adjacent(q1, q2). adjacent(q2, q1).
adjacent(q2, q3). adjacent(q3, q2).

adjacent(q4, q5). adjacent(q5, q4).
adjacent(q5, q6). adjacent(q6, q5).
adjacent(q6, q7). adjacent(q7, q6).

adjacent(q0, q4). adjacent(q4, q0).
adjacent(q1, q5). adjacent(q5, q1).
adjacent(q2, q6). adjacent(q6, q2).
adjacent(q3, q7). adjacent(q7, q3).

% ==================== GATE DEFINITIONS ====================
% Gate types and their qubit requirements
gate_type(h_q0, single, q0).
gate_type(x_q1, single, q1).
gate_type(cnot_q2_q3, cnot, q2, q3).
gate_type(cnot_q4_q5, cnot, q4, q5).
gate_type(cnot_q0_q2, cnot, q0, q2).
gate_type(toffoli_q5_q7_q6, toffoli, q5, q7, q6).

% Gate dependencies
depends(toffoli_q5_q7_q6, cnot_q4_q5).

% ==================== SCHEDULING VARIABLES ====================
% Time when each gate is executed
1 { gate_time(G, T) : time(T) } 1 :- gate_type(G, _, _).

% SWAP operations between adjacent qubits at each time
{ swap(Q1, Q2, T) : adjacent(Q1, Q2), time(T) } :- time(T).

% ==================== TOPOLOGY CONSTRAINTS ====================
% Single-qubit gates can be executed on any qubit
:- gate_time(G, T), gate_type(G, single, Q), not qubit(Q).

% CNOT gates require control and target to be adjacent
:- gate_time(G, T), gate_type(G, cnot, C, Tgt),
   not adjacent(C, Tgt).

% Toffoli gates require both controls adjacent to target
:- gate_time(G, T), gate_type(G, toffoli, C1, C2, Tgt),
   not adjacent(C1, Tgt), not adjacent(C2, Tgt).

% ==================== DEPENDENCY CONSTRAINTS ====================
% Gate dependencies must be respected
:- gate_time(G1, T1), gate_time(G2, T2), depends(G1, G2), T1 <= T2.

% ==================== QUBIT CONFLICT CONSTRAINTS ====================
% At each time step, each qubit can be used by at most one gate
% For single-qubit gates
:- gate_time(G1, T), gate_time(G2, T), G1 != G2,
   gate_type(G1, single, Q), gate_type(G2, single, Q).

% For CNOT gates (control or target qubits)
:- gate_time(G1, T), gate_time(G2, T), G1 != G2,
   gate_type(G1, cnot, C1, T1), gate_type(G2, cnot, C2, T2),
   (C1 = C2; C1 = T2; T1 = C2; T1 = T2).

% For Toffoli gates (controls and target)
:- gate_time(G1, T), gate_time(G2, T), G1 != G2,
   gate_type(G1, toffoli, C1a, C1b, T1), gate_type(G2, toffoli, C2a, C2b, T2),
   (C1a = C2a; C1a = C2b; C1a = T2; C1b = C2a; C1b = C2b; C1b = T2; T1 = C2a; T1 = C2b; T1 = T2).

% Mixed gate conflicts (single vs CNOT, etc.)
:- gate_time(G1, T), gate_time(G2, T), G1 != G2,
   gate_type(G1, single, Q),
   (gate_type(G2, cnot, Q, _); gate_type(G2, cnot, _, Q);
    gate_type(G2, toffoli, Q, _, _); gate_type(G2, toffoli, _, Q, _);
    gate_type(G2, toffoli, _, _, Q)).

% ==================== SWAP OPERATIONS ====================
% SWAP operations also consume qubits at their time
:- swap(Q1, Q2, T), gate_time(G, T),
   (gate_type(G, single, Q1); gate_type(G, single, Q2);
    gate_type(G, cnot, Q1, _); gate_type(G, cnot, _, Q1);
    gate_type(G, cnot, Q2, _); gate_type(G, cnot, _, Q2);
    gate_type(G, toffoli, Q1, _, _); gate_type(G, toffoli, _, Q1, _);
    gate_type(G, toffoli, _, _, Q1);
    gate_type(G, toffoli, Q2, _, _); gate_type(G, toffoli, _, Q2, _);
    gate_type(G, toffoli, _, _, Q2)).

% SWAPs cannot conflict with each other
:- swap(Q1, Q2, T), swap(Q3, Q4, T), (Q1 = Q3; Q1 = Q4; Q2 = Q3; Q2 = Q4), (Q1, Q2) != (Q3, Q4).

% ==================== OPTIMIZATION ====================
% Circuit depth is the maximum time step used
circuit_depth(D) :- D = #max{ T : gate_time(_, T) }.

% Count SWAP operations
swaps_used(S) :- S = #count{ Q1, Q2, T : swap(Q1, Q2, T) }.

% ==================== OUTPUT ====================
#show gate_time/2.
#show swap/3.
#show circuit_depth/1.
#show swaps_used/1.

% Optimization: minimize depth first, then swaps
#minimize { 1@1, D : circuit_depth(D) }.
#minimize { 1@2, S : swaps_used(S) }.