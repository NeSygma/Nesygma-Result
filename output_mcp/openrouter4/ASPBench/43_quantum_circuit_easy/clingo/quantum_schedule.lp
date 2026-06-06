% Quantum Gate Scheduling Problem
% Instance Data

% Qubits
qubit(q0; q1; q2; q3).

% Gates
gate(h_q0; h_q1; x_q2; cnot_q0_q1; cnot_q1_q2; cnot_q0_q3).

% Gate-qubit mapping (which qubits a gate acts on)
acts_on(h_q0, q0).
acts_on(h_q1, q1).
acts_on(x_q2, q2).
acts_on(cnot_q0_q1, q0).
acts_on(cnot_q0_q1, q1).
acts_on(cnot_q1_q2, q1).
acts_on(cnot_q1_q2, q2).
acts_on(cnot_q0_q3, q0).
acts_on(cnot_q0_q3, q3).

% Time horizon (upper bound: at most 6 time steps for 6 gates)
time(1..6).

% 1. Each gate assigned to exactly one time step
{ assign(G, T) : time(T) } 1 :- gate(G).

% 2. No two gates share a qubit at the same time step
:- assign(G1, T), assign(G2, T), G1 != G2, acts_on(G1, Q), acts_on(G2, Q).

% 3. All gates must be scheduled (guaranteed by the choice rule)

% Compute circuit depth (maximum time step used)
depth(D) :- D = #max{ T : assign(G, T) }.

% Minimize circuit depth
#minimize { D : depth(D) }.

% Output predicates
#show assign/2.
#show depth/1.