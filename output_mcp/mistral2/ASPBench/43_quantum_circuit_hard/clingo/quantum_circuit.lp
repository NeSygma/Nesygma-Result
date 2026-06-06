% --- Basic Facts ---
qubit(q0). qubit(q1). qubit(q2). qubit(q3).
qubit(q4). qubit(q5). qubit(q6). qubit(q7).

% Adjacency (2x4 grid)
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

% Gates
gate(h_q0). gate(x_q1). gate(cnot_q2_q3). gate(cnot_q4_q5).
gate(cnot_q0_q2). gate(toffoli_q5_q7_q6).

% Single-qubit gates
single_qubit(h_q0, q0).
single_qubit(x_q1, q1).

% Two-qubit gates
control(cnot_q2_q3, q2). target(cnot_q2_q3, q3).
control(cnot_q4_q5, q4). target(cnot_q4_q5, q5).
control(cnot_q0_q2, q0). target(cnot_q0_q2, q2).

% Toffoli gate (three-qubit)
control(toffoli_q5_q7_q6, q5). control(toffoli_q5_q7_q6, q7).
target(toffoli_q5_q7_q6, q6).

% Gate dependencies
dependency(toffoli_q5_q7_q6, cnot_q4_q5).

% --- Time Horizon ---
time(0..10). % Start with 10 time steps; refine if needed.

% --- Initial Qubit Mapping ---
mapped(Q, Q, 0) :- qubit(Q).

% --- SWAP Gates ---
{swap(Q1, Q2, T) : adjacent(Q1, Q2)} 1 :- time(T), T > 0.

% Update mapping after SWAP
mapped(Q2, LQ, T+1) :- swap(Q1, Q2, T), mapped(Q1, LQ, T), time(T).
mapped(Q1, LQ, T+1) :- swap(Q1, Q2, T), mapped(Q2, LQ, T), time(T).
mapped(Q, LQ, T+1) :- mapped(Q, LQ, T), not swap(Q, _, T), time(T).

% --- Gate Scheduling ---
{scheduled(G, T) : time(T)} 1 :- gate(G).

% --- No Qubit Conflicts ---
% Single-qubit gates: no conflict if only one gate uses the qubit
:- scheduled(G, T), single_qubit(G, Q), {scheduled(G2, T) : single_qubit(G2, Q)} > 1.

% Multi-qubit gates: no conflict if any qubit is used by more than one gate
:- scheduled(G, T), control(G, Q), {scheduled(G2, T) : control(G2, Q)} > 1.
:- scheduled(G, T), target(G, Q), {scheduled(G2, T) : target(G2, Q)} > 1.

% --- Adjacency for Multi-Qubit Gates ---
% For two-qubit gates
:- scheduled(G, T), control(G, Q1), target(G, Q2), not adjacent(Q1, Q2),
   mapped(Q1, LQ1, T), mapped(Q2, LQ2, T).

% For Toffoli gate (three-qubit)
:- scheduled(toffoli_q5_q7_q6, T),
   not adjacent(MappedQ5, MappedQ6),
   not adjacent(MappedQ7, MappedQ6),
   mapped(Q5, q5, T), mapped(Q6, q6, T), mapped(Q7, q7, T),
   mapped(MappedQ5, q5, T), mapped(MappedQ6, q6, T), mapped(MappedQ7, q7, T).

% --- Dependency Ordering ---
:- scheduled(G2, T2), scheduled(G1, T1), dependency(G1, G2), T2 <= T1.

% --- Objective ---
% Minimize circuit depth
circuit_depth(T) :- time(T), {scheduled(_, T)} > 0.

% Minimize SWAP gates
swaps_used(N) :- N = #count {Q1, Q2, T : swap(Q1, Q2, T)}.

% --- Show Directives ---
#show scheduled/2.
#show swap/3.
#show circuit_depth/1.
#show swaps_used/1.