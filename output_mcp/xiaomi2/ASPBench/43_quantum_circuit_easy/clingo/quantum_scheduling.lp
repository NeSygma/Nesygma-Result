% Quantum Gate Scheduling Problem
% Minimize circuit depth while respecting qubit constraints

% ============ DOMAINS ============
% Qubits
qubit(q0). qubit(q1). qubit(q2). qubit(q3).

% Gates
gate(h_q0). gate(h_q1). gate(x_q2).
gate(cnot_q0_q1). gate(cnot_q1_q2). gate(cnot_q0_q3).

% Time steps (upper bound - will be minimized)
time(1..6).

% ============ GATE-QUBIT MAPPING ============
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

% ============ SCHEDULING ============
% Each gate is scheduled at exactly one time step
1 { scheduled(G, T) : time(T) } 1 :- gate(G).

% ============ CONSTRAINTS ============
% Two gates cannot execute at the same time if they share any qubit
:- scheduled(G1, T), scheduled(G2, T), G1 != G2, uses_qubit(G1, Q), uses_qubit(G2, Q).

% ============ OUTPUT ============
% Define the makespan (maximum time step used)
makespan(M) :- M = #max { T : scheduled(_, T) }.

% Minimize the circuit depth
#minimize { M : makespan(M) }.

% ============ SHOW ============
#show scheduled/2.
#show makespan/1.