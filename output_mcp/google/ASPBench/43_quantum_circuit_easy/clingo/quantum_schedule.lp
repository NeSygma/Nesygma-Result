% --- Data ---
gate_name(h_q0). gate_name(h_q1). gate_name(x_q2). 
gate_name(cnot_q0_q1). gate_name(cnot_q1_q2). gate_name(cnot_q0_q3).

gate(h_q0, q0).
gate(h_q1, q1).
gate(x_q2, q2).
gate(cnot_q0_q1, q0). gate(cnot_q0_q1, q1).
gate(cnot_q1_q2, q1). gate(cnot_q1_q2, q2).
gate(cnot_q0_q3, q0). gate(cnot_q0_q3, q3).

% --- Constraints ---
time(1..6).

% Each gate must be scheduled at exactly one time step
1 { scheduled(G, T) : time(T) } 1 :- gate_name(G).

% Two gates cannot execute at the same time if they share any qubit
:- scheduled(G1, T), scheduled(G2, T), G1 != G2, gate(G1, Q), gate(G2, Q).

% --- Objective ---
% Minimize the maximum time step used
depth(D) :- D = #max { T : scheduled(G, T) }.
#minimize { D : depth(D) }.

% --- Output ---
#show scheduled/2.
#show depth/1.