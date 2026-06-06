% --- Facts ---
qubit(q0). qubit(q1). qubit(q2). qubit(q3).

gate(h_q0). gate(h_q1). gate(x_q2).
gate(cnot_q0_q1). gate(cnot_q1_q2). gate(cnot_q0_q3).

% Qubits involved in each gate
qubits_of_gate(h_q0, q0).
qubits_of_gate(h_q1, q1).
qubits_of_gate(x_q2, q2).
qubits_of_gate(cnot_q0_q1, q0, q1).
qubits_of_gate(cnot_q1_q2, q1, q2).
qubits_of_gate(cnot_q0_q3, q0, q3).

% --- Time steps ---
max_time(3).
time(1..max_time).

% --- Choice rule: Schedule each gate to exactly one time step ---
1 { scheduled(G, T) : time(T) } 1 :- gate(G).

% --- Helper: Check if two gates share any qubit ---
share_qubit(G1, G2) :-
    scheduled(G1, T), scheduled(G2, T), G1 != G2,
    qubits_of_gate(G1, Q1, Q2),
    qubits_of_gate(G2, Q3, Q4),
    (Q1 = Q3 ; Q1 = Q4 ; Q2 = Q3 ; Q2 = Q4).

% --- Constraint: Gates sharing qubits cannot be scheduled at the same time ---
:- share_qubit(G1, G2).

% --- Objective: Minimize the maximum time step used ---
#minimize { T : time(T), scheduled(_, T) }.

% --- Output ---
circuit_depth(D) :- D = #max { T : time(T), scheduled(_, T) }.
gate_schedule(T, G) :- time(T), gate(G), scheduled(G, T).

% --- Show directives ---
#show circuit_depth/1.
#show gate_schedule/2.