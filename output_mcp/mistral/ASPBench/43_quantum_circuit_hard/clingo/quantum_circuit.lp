%% Basic definitions
% Qubits
qubit(q0; q1; q2; q3; q4; q5; q6; q7).

% Topology: 2x4 grid adjacency (undirected)
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

% Gate definitions
% Single-qubit gates
gate(h_q0). gate_type(h_q0, single). gate_qubit(h_q0, q0).
gate(x_q1). gate_type(x_q1, single). gate_qubit(x_q1, q1).

% Two-qubit gates
gate(cnot_q2_q3). gate_type(cnot_q2_q3, double).
    gate_qubit(cnot_q2_q3, q2). gate_qubit(cnot_q2_q3, q3).
    control(cnot_q2_q3, q2). target(cnot_q2_q3, q3).

gate(cnot_q4_q5). gate_type(cnot_q4_q5, double).
    gate_qubit(cnot_q4_q5, q4). gate_qubit(cnot_q4_q5, q5).
    control(cnot_q4_q5, q4). target(cnot_q4_q5, q5).

gate(cnot_q0_q2). gate_type(cnot_q0_q2, double).
    gate_qubit(cnot_q0_q2, q0). gate_qubit(cnot_q0_q2, q2).
    control(cnot_q0_q2, q0). target(cnot_q0_q2, q2).

% Three-qubit gates
gate(toffoli_q5_q7_q6). gate_type(toffoli_q5_q7_q6, triple).
    gate_qubit(toffoli_q5_q7_q6, q5). gate_qubit(toffoli_q5_q7_q6, q7). gate_qubit(toffoli_q5_q7_q6, q6).
    control(toffoli_q5_q7_q6, q5). control(toffoli_q5_q7_q6, q7). target(toffoli_q5_q7_q6, q6).

% Gate dependencies
% toffoli_q5_q7_q6 must be scheduled strictly after cnot_q4_q5
depends_after(toffoli_q5_q7_q6, cnot_q4_q5).

% Time horizon (we'll search for minimal depth)
time(1..10).

% Initial positions: logical qubits start at their physical locations
% position(LogicalQubit, PhysicalQubit, Time)

% Choice rule: assign each gate to a time step
{ scheduled(G, T) : time(T) } 1 :- gate(G).

% SWAP operations can be inserted between adjacent qubits
{ swap(Q1, Q2, T) : adjacent(Q1, Q2), time(T) }.

% Frame axioms for qubit positions
% At time 1, each logical qubit is at its initial physical location
position(Q, Q, 1) :- qubit(Q).

% Position persists unless swapped
position(Q, P, T+1) :- position(Q, P, T), time(T+1), not swapped_at_qubit(Q, P, T).

% SWAP changes positions of two qubits
swapped_at_qubit(Q1, P, T) :- swap(Q1, Q2, T), position(Q1, P, T), position(Q2, P2, T), adjacent(P, P2).
swapped_at_qubit(Q2, P2, T) :- swap(Q1, Q2, T), position(Q1, P, T), position(Q2, P2, T), adjacent(P, P2).

% Update positions after swap
position(Q1, P2, T+1) :- swapped_at_qubit(Q1, P, T), position(Q1, P, T), swap(Q1, Q2, T), position(Q2, P2, T), time(T+1).
position(Q2, P, T+1) :- swapped_at_qubit(Q2, P2, T), position(Q2, P2, T), swap(Q1, Q2, T), position(Q1, P, T), time(T+1).

% Constraint: No qubit conflict at any time step
% A physical qubit can be used by at most one gate at each time
:- scheduled(G, T), gate_qubit(G, Q), time(T),
   scheduled(G2, T), G != G2, gate_qubit(G2, Q).

% Constraint: Multi-qubit gates require adjacent qubits at schedule time
:- scheduled(G, T), gate_type(G, double), time(T),
   not adjacent_qubits_for_gate(G, T).
adjacent_qubits_for_gate(G, T) :-
    scheduled(G, T), gate_type(G, double),
    gate_qubit(G, Q1), gate_qubit(G, Q2),
    position(Q1, P1, T), position(Q2, P2, T), adjacent(P1, P2).

% Special constraint for Toffoli: both controls must be adjacent to target
:- scheduled(toffoli_q5_q7_q6, T), time(T),
   not toffoli_adjacent(T).

toffoli_adjacent(T) :-
    position(q5, P5, T), position(q7, P7, T), position(q6, P6, T),
    adjacent(P5, P6), adjacent(P7, P6).

% Dependency constraint: if G1 depends on G2, G1 must be scheduled after G2
:- depends_after(G1, G2), scheduled(G1, T1), scheduled(G2, T2), T1 <= T2.

% Count SWAPs
swap_count(S) :- S = #count { Q1, Q2, T : swap(Q1, Q2, T) }.

% Show directives
#show scheduled/2.
#show swap/3.
#show swap_count/1.

% Additional show for debugging
#show position/3.