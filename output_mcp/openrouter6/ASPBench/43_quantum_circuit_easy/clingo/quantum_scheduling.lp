% Quantum gate scheduling to minimize circuit depth

% --- Domain ---
qubit(q0). qubit(q1). qubit(q2). qubit(q3).

gate(h_q0). gate(h_q1). gate(x_q2). gate(cnot_q0_q1). gate(cnot_q1_q2). gate(cnot_q0_q3).

% Gate-qubit usage
gate_uses(h_q0, q0).
gate_uses(h_q1, q1).
gate_uses(x_q2, q2).
gate_uses(cnot_q0_q1, q0).
gate_uses(cnot_q0_q1, q1).
gate_uses(cnot_q1_q2, q1).
gate_uses(cnot_q1_q2, q2).
gate_uses(cnot_q0_q3, q0).
gate_uses(cnot_q0_q3, q3).

% Time steps (bound: we expect depth 3, but allow up to 6)
time(1..6).

% Decision: gate assigned to time
1 { gate_time(Gate, T) : time(T) } 1 :- gate(Gate).

% Constraint: gates sharing a qubit cannot execute at same time
:- gate_time(G1, T), gate_time(G2, T), G1 != G2, gate_uses(G1, Q), gate_uses(G2, Q).

% Compute maximum time used
max_time(T) :- time(T), not greater_time_exists(T).
greater_time_exists(T) :- time(T), time(T2), T2 > T, gate_time(_, T2).

% Objective: minimize circuit depth (maximum time)
#minimize { 1, T : max_time(T) }.

% Output
circuit_depth(D) :- max_time(D).
schedule(T, G) :- gate_time(G, T).

#show circuit_depth/1.
#show schedule/2.