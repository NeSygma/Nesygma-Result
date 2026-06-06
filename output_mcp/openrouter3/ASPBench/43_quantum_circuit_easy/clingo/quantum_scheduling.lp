% Quantum Gate Scheduling Problem

% Domain declarations
qubit(q0). qubit(q1). qubit(q2). qubit(q3).

gate(h_q0). gate(h_q1). gate(x_q2).
gate(cnot_q0_q1). gate(cnot_q1_q2). gate(cnot_q0_q3).

% Qubit usage for each gate
uses(h_q0, q0).
uses(h_q1, q1).
uses(x_q2, q2).
uses(cnot_q0_q1, q0). uses(cnot_q0_q1, q1).
uses(cnot_q1_q2, q1). uses(cnot_q1_q2, q2).
uses(cnot_q0_q3, q0). uses(cnot_q0_q3, q3).

% Time domain - we'll try up to 5 time steps (should be enough for optimal depth 3)
time(1..5).

% Choice rule: each gate scheduled at exactly one time
1 { scheduled(G, T) : time(T) } 1 :- gate(G).

% Constraint: no two gates sharing a qubit can execute at same time
:- scheduled(G1, T), scheduled(G2, T), G1 != G2, uses(G1, Q), uses(G2, Q).

% Calculate circuit depth (maximum time step used)
circuit_depth(D) :- D = #max { T : scheduled(_, T) }.

% Minimize circuit depth
#minimize { D : circuit_depth(D) }.

% Helper for output: gate_at_time(T, G)
gate_at_time(T, G) :- scheduled(G, T).

% Show relevant information
#show circuit_depth/1.
#show gate_at_time/2.