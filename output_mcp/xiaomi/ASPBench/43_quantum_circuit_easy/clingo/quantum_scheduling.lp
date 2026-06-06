% ==============================
% Quantum Gate Scheduling Problem
% ==============================

% --- Domain: Qubits ---
qubit(q0). qubit(q1). qubit(q2). qubit(q3).

% --- Domain: Gates ---
gate(h_q0).
gate(h_q1).
gate(x_q2).
gate(cnot_q0_q1).
gate(cnot_q1_q2).
gate(cnot_q0_q3).

% --- Gate-Qubit Usage ---
% Single-qubit gates
uses_qubit(h_q0, q0).
uses_qubit(h_q1, q1).
uses_qubit(x_q2, q2).

% CNOT gates use both control and target qubits
uses_qubit(cnot_q0_q1, q0).
uses_qubit(cnot_q0_q1, q1).
uses_qubit(cnot_q1_q2, q1).
uses_qubit(cnot_q1_q2, q2).
uses_qubit(cnot_q0_q3, q0).
uses_qubit(cnot_q0_q3, q3).

% --- Time Horizon ---
% Upper bound: worst case is all gates sequential (6 steps)
% We'll use a reasonable upper bound
time(1..6).

% --- Conflict Detection ---
% Two gates conflict if they share any qubit
conflict(G1, G2) :- gate(G1), gate(G2), G1 != G2, 
                     uses_qubit(G1, Q), uses_qubit(G2, Q).

% --- Decision: Schedule each gate at exactly one time step ---
1 { scheduled(G, T) : time(T) } 1 :- gate(G).

% --- Constraint: Conflicting gates cannot be at the same time ---
:- conflict(G1, G2), scheduled(G1, T), scheduled(G2, T).

% --- Compute maximum time step used ---
max_time(T) :- scheduled(_, T), time(T).
max_time_val(M) :- M = #max { T : max_time(T) }.

% --- Minimize circuit depth ---
#minimize { M : max_time_val(M) }.

% --- Output predicates ---
gate_at_time(T, G) :- scheduled(G, T).
circuit_depth(M) :- max_time_val(M).

#show gate_at_time/2.
#show circuit_depth/1.