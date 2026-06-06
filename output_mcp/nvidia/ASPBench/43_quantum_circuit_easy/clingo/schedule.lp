% Define time steps
time(1). time(2). time(3). time(4). time(5).

% Define gates
gate(h_q0). gate(h_q1). gate(x_q2). gate(cnot_q0_q1). gate(cnot_q1_q2). gate(cnot_q0_q3).

% Exactly one time per gate
1 { scheduled(G,T) : time(T) } 1 :- gate(G).

% Conflict relation
conflict(h_q0, cnot_q0_q1).
conflict(h_q0, cnot_q0_q3).
conflict(h_q1, cnot_q0_q1).
conflict(h_q1, cnot_q1_q2).
conflict(x_q2, cnot_q1_q2).
conflict(cnot_q0_q1, cnot_q0_q3).
conflict(cnot_q0_q1, cnot_q1_q2).

% No conflicting gates at the same time
:- scheduled(G1,T), scheduled(G2,T), conflict(G1,G2).

% Define used_time
used_time(T) :- scheduled(G,T).

% Contiguity constraints (no gaps)
:- used_time(2), not used_time(1).
:- used_time(3), not used_time(2).
:- used_time(4), not used_time(3).
:- used_time(5), not used_time(4).

% Define depth as the maximum used_time
depth(D) :- used_time(D), #max { D2 : used_time(D2) } = D.

% Minimize the maximum time step (circuit depth)
#minimize { D : depth(D) }.

% Show the results
#show depth/1.
#show scheduled/2.