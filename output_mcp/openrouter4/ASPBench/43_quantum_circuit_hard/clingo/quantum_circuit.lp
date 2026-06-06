% --- Quantum Circuit Compilation on 2x4 Grid ---

#const max_depth = 5.

% Positions
pos(0..7).

% Logical qubits
lq(0..7).

% Topology adjacency (2x4 grid)
adj(0,1). adj(1,0). adj(1,2). adj(2,1). adj(2,3). adj(3,2).
adj(4,5). adj(5,4). adj(5,6). adj(6,5). adj(6,7). adj(7,6).
adj(0,4). adj(4,0). adj(1,5). adj(5,1). adj(2,6). adj(6,2). adj(3,7). adj(7,3).

% Time steps
time(1..max_depth).

% Gate names
gate_name("h_q0"; "x_q1"; "cnot_q2_q3"; "cnot_q4_q5"; "cnot_q0_q2"; "toffoli_q5_q7_q6").

% Gate types
single("h_q0"; "x_q1").
cnot("cnot_q2_q3"; "cnot_q4_q5"; "cnot_q0_q2").
toffoli("toffoli_q5_q7_q6").

% Qubits per gate
qubit_of("h_q0", 0).
qubit_of("x_q1", 1).
qubit_of("cnot_q2_q3", 2; 3).
qubit_of("cnot_q4_q5", 4; 5).
qubit_of("cnot_q0_q2", 0; 2).
qubit_of("toffoli_q5_q7_q6", 5; 7; 6).

% CNOT pairs (control, target)
cnot_pair("cnot_q2_q3", 2, 3).
cnot_pair("cnot_q4_q5", 4, 5).
cnot_pair("cnot_q0_q2", 0, 2).

% Toffoli triple (control1, control2, target)
toffoli_triple("toffoli_q5_q7_q6", 5, 7, 6).

% Dependency: toffoli must be after cnot_q4_q5
depends("toffoli_q5_q7_q6", "cnot_q4_q5").

% --- Initial mapping: each logical qubit starts at its corresponding physical position ---
map(L, L, 1) :- lq(L).

% --- SWAP operations ---
% SWAP can be inserted between any adjacent physical qubits at any time step
{ swap(P1, P2, T) : adj(P1, P2), P1 < P2 } :- time(T).

% A physical qubit can be in at most one SWAP per time step
:- swap(P1, P2, T), swap(P1, P3, T), P2 != P3.
:- swap(P1, P2, T), swap(P3, P2, T), P1 != P3.

% Effect of SWAP: at the next time step, logical qubits at P1 and P2 are swapped
map(L, P2, T+1) :- swap(P1, P2, T), map(L, P1, T), time(T), T < max_depth.
map(L, P1, T+1) :- swap(P1, P2, T), map(L, P2, T), time(T), T < max_depth.

% Qubits not involved in any SWAP keep their position
involved(P, T) :- swap(P, _, T).
involved(P, T) :- swap(_, P, T).
map(L, P, T+1) :- map(L, P, T), time(T), T < max_depth, not involved(P, T).

% --- Gate scheduling ---
% Each gate scheduled exactly once
1 { schedule(G, T) : time(T) } 1 :- gate_name(G).

% Dependency constraint: toffoli after cnot_q4_q5
:- schedule("toffoli_q5_q7_q6", T1), schedule("cnot_q4_q5", T2), T1 <= T2.

% --- Adjacency constraints for multi-qubit gates ---
% CNOT: both qubits must be physically adjacent at execution time
:- schedule(G, T), cnot(G), cnot_pair(G, L1, L2),
   map(L1, P1, T), map(L2, P2, T), not adj(P1, P2).

% Toffoli: both controls must be adjacent to target at execution time
:- schedule(G, T), toffoli(G), toffoli_triple(G, L1, L2, L3),
   map(L1, P1, T), map(L2, P2, T), map(L3, P3, T), not adj(P1, P3).
:- schedule(G, T), toffoli(G), toffoli_triple(G, L1, L2, L3),
   map(L1, P1, T), map(L2, P2, T), map(L3, P3, T), not adj(P2, P3).

% --- Physical qubit usage by gates ---
used_by_gate(P, G, T) :- schedule(G, T), single(G), qubit_of(G, L), map(L, P, T).
used_by_gate(P1, G, T) :- schedule(G, T), cnot(G), cnot_pair(G, L1, L2), map(L1, P1, T), map(L2, P2, T).
used_by_gate(P2, G, T) :- schedule(G, T), cnot(G), cnot_pair(G, L1, L2), map(L1, P1, T), map(L2, P2, T).
used_by_gate(P1, G, T) :- schedule(G, T), toffoli(G), toffoli_triple(G, L1, L2, L3), map(L1, P1, T), map(L2, P2, T), map(L3, P3, T).
used_by_gate(P2, G, T) :- schedule(G, T), toffoli(G), toffoli_triple(G, L1, L2, L3), map(L1, P1, T), map(L2, P2, T), map(L3, P3, T).
used_by_gate(P3, G, T) :- schedule(G, T), toffoli(G), toffoli_triple(G, L1, L2, L3), map(L1, P1, T), map(L2, P2, T), map(L3, P3, T).

% Physical qubit used by SWAP
used_by_swap(P, T) :- swap(P, _, T).
used_by_swap(P, T) :- swap(_, P, T).

% --- No qubit conflicts ---
% Two different gates cannot use the same physical qubit at the same time
:- schedule(G1, T), schedule(G2, T), G1 != G2,
   used_by_gate(P, G1, T), used_by_gate(P, G2, T).

% A gate and a SWAP cannot use the same physical qubit at the same time
:- used_by_gate(P, G, T), used_by_swap(P, T).

% --- Objective ---
% Minimize depth (max time step used)
max_depth_used(D) :- D = #max{ T : schedule(G, T) }.
% Minimize number of SWAPs
total_swaps(N) :- N = #count{ P1, P2, T : swap(P1, P2, T) }.

#minimize { D@2 : max_depth_used(D) }.
#minimize { N@1 : total_swaps(N) }.

% --- Output ---
circuit_depth(D) :- max_depth_used(D).
swaps_used(N) :- total_swaps(N).
gate_schedule(T, G) :- schedule(G, T).
swap_schedule(T, P1, P2) :- swap(P1, P2, T).

#show circuit_depth/1.
#show swaps_used/1.
#show gate_schedule/2.
#show swap_schedule/3.