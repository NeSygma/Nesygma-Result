% Quantum Circuit Scheduling - Minimize Depth

% Define qubits
qubit(q0; q1; q2; q3).

% Define gates
gate(h_q0; h_q1; x_q2; cnot_q0_q1; cnot_q1_q2; cnot_q0_q3).

% Define which qubits each gate operates on
operates_on(h_q0, q0).
operates_on(h_q1, q1).
operates_on(x_q2, q2).
operates_on(cnot_q0_q1, q0).
operates_on(cnot_q0_q1, q1).
operates_on(cnot_q1_q2, q1).
operates_on(cnot_q1_q2, q2).
operates_on(cnot_q0_q3, q0).
operates_on(cnot_q0_q3, q3).

% Time steps - we need at most 6 (one per gate), but optimal is 3
time(1..6).

% Each gate must be scheduled at exactly one time step
1 { schedule(G, T) : time(T) } 1 :- gate(G).

% Two gates cannot execute at the same time if they share any qubit
:- schedule(G1, T), schedule(G2, T), G1 != G2,
   operates_on(G1, Q), operates_on(G2, Q).

% Define circuit depth as the maximum time step used
max_time_used(T) :- T = #max { T2 : schedule(_, T2) }.

% Minimize the circuit depth
#minimize { T : schedule(_, T) }.

% Show results
#show schedule/2.
#show max_time_used/1.