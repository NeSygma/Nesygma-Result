% Quantum Circuit Scheduling with Topology Constraints

% ========== DOMAINS ==========
% Physical qubits (0-7 correspond to q0-q7)
physical(0..7).

% Logical qubits (0-7 correspond to q0-q7)
logical(0..7).

% Time steps (we'll try depth 3 first)
time(1..3).

% ========== TOPOLOGY ==========
% Adjacency in 2x4 grid
adjacent(0,1). adjacent(1,2). adjacent(2,3).
adjacent(4,5). adjacent(5,6). adjacent(6,7).
adjacent(0,4). adjacent(1,5). adjacent(2,6). adjacent(3,7).
adjacent(P2,P1) :- adjacent(P1,P2).

% ========== GATES ==========
% Gate definitions with logical qubits
% Single-qubit gates
gate(h_q0, single, 0).
gate(x_q1, single, 1).

% CNOT gates: gate(control, target)
cnot(cnot_q2_q3, 2, 3).
cnot(cnot_q4_q5, 4, 5).
cnot(cnot_q0_q2, 0, 2).

% Toffoli gate: gate(control1, control2, target)
toffoli(toffoli_q5_q7_q6, 5, 7, 6).

% Dependencies: toffoli must be after cnot_q4_q5
dependency(toffoli_q5_q7_q6, cnot_q4_q5).

% ========== INITIAL MAPPING ==========
% Initially, logical qubit L is on physical qubit L
mapped(L, L, 1) :- logical(L).

% ========== ACTIONS ==========
% Execute gate G at time T
{ executed(G, T) : time(T) } 1 :- gate(G, _, _).
{ executed(G, T) : time(T) } 1 :- cnot(G, _, _).
{ executed(G, T) : time(T) } 1 :- toffoli(G, _, _, _).

% Swap adjacent physical qubits at time T
{ swap(P1, P2, T) : adjacent(P1,P2), time(T) }.

% ========== MAPPING TRANSITION ==========
% After swap, logical qubits exchange physical positions
mapped(L, P2, T+1) :- swap(P1, P2, T), mapped(L, P1, T), time(T), time(T+1).
mapped(L, P1, T+1) :- swap(P1, P2, T), mapped(L, P2, T), time(T), time(T+1).

% Logical qubits not involved in swap stay in place
mapped(L, P, T+1) :- mapped(L, P, T), time(T), time(T+1),
                     not involved_in_swap(P, T).

% Helper: physical qubit P is involved in swap at time T
involved_in_swap(P, T) :- swap(P, _, T).
involved_in_swap(P, T) :- swap(_, P, T).

% ========== GATE EXECUTION CONSTRAINTS ==========
% For single-qubit gates
used_phys_single(G, P, T) :- executed(G, T), gate(G, single, L), mapped(L, P, T).

% For CNOT gates
used_phys_cnot(G, Pc, Pt, T) :- executed(G, T), cnot(G, Lc, Lt),
                                mapped(Lc, Pc, T), mapped(Lt, Pt, T).

% For Toffoli gates
used_phys_toffoli(G, Pc1, Pc2, Pt, T) :- executed(G, T), toffoli(G, Lc1, Lc2, Lt),
                                         mapped(Lc1, Pc1, T), mapped(Lc2, Pc2, T), mapped(Lt, Pt, T).

% CNOT adjacency constraint: control and target must be adjacent
:- executed(G, T), cnot(G, Lc, Lt),
   mapped(Lc, Pc, T), mapped(Lt, Pt, T), not adjacent(Pc, Pt).

% Toffoli adjacency constraint: both controls must be adjacent to target
% We need to check both controls separately
:- executed(G, T), toffoli(G, Lc1, Lc2, Lt),
   mapped(Lc1, Pc1, T), mapped(Lt, Pt, T), not adjacent(Pc1, Pt).
:- executed(G, T), toffoli(G, Lc1, Lc2, Lt),
   mapped(Lc2, Pc2, T), mapped(Lt, Pt, T), not adjacent(Pc2, Pt).

% ========== CONFLICT AVOIDANCE ==========
% No physical qubit can be used by multiple gates at same time
% Single-qubit gates
:- used_phys_single(G1, P, T), used_phys_single(G2, P, T), G1 != G2.

% CNOT gates
:- used_phys_cnot(G1, P, _, T), used_phys_cnot(G2, P, _, T), G1 != G2.
:- used_phys_cnot(G1, _, P, T), used_phys_cnot(G2, _, P, T), G1 != G2.

% Toffoli gates
:- used_phys_toffoli(G1, P, _, _, T), used_phys_toffoli(G2, P, _, _, T), G1 != G2.
:- used_phys_toffoli(G1, _, P, _, T), used_phys_toffoli(G2, _, P, _, T), G1 != G2.
:- used_phys_toffoli(G1, _, _, P, T), used_phys_toffoli(G2, _, _, P, T), G1 != G2.

% Single-qubit vs CNOT conflicts
:- used_phys_single(G1, P, T), used_phys_cnot(G2, P, _, T).
:- used_phys_single(G1, P, T), used_phys_cnot(G2, _, P, T).

% Single-qubit vs Toffoli conflicts
:- used_phys_single(G1, P, T), used_phys_toffoli(G2, P, _, _, T).
:- used_phys_single(G1, P, T), used_phys_toffoli(G2, _, P, _, T).
:- used_phys_single(G1, P, T), used_phys_toffoli(G2, _, _, P, T).

% CNOT vs Toffoli conflicts
:- used_phys_cnot(G1, P, _, T), used_phys_toffoli(G2, P, _, _, T).
:- used_phys_cnot(G1, _, P, T), used_phys_toffoli(G2, P, _, _, T).
:- used_phys_cnot(G1, _, P, T), used_phys_toffoli(G2, _, P, _, T).
:- used_phys_cnot(G1, _, P, T), used_phys_toffoli(G2, _, _, P, T).

% No physical qubit can be used by both gate and swap at same time
used_by_swap(P, T) :- swap(P, _, T).
used_by_swap(P, T) :- swap(_, P, T).
:- used_phys_single(_, P, T), used_by_swap(P, T).
:- used_phys_cnot(_, P, _, T), used_by_swap(P, T).
:- used_phys_cnot(_, _, P, T), used_by_swap(P, T).
:- used_phys_toffoli(_, P, _, _, T), used_by_swap(P, T).
:- used_phys_toffoli(_, _, P, _, T), used_by_swap(P, T).
:- used_phys_toffoli(_, _, _, P, T), used_by_swap(P, T).

% No overlapping swaps
:- swap(P1, P2, T), swap(P1, P3, T), P2 != P3.
:- swap(P1, P2, T), swap(P3, P2, T), P1 != P3.

% ========== DEPENDENCIES ==========
% Enforce dependency ordering
:- executed(G2, T2), dependency(G2, G1), executed(G1, T1), T2 <= T1.

% ========== OBJECTIVES ==========
% Makespan (circuit depth)
makespan(M) :- M = #max{ T : executed(_, T) }.

% Swap count
swap_count(S) :- S = #count{ P1, P2, T : swap(P1, P2, T) }.

% ========== OUTPUT ==========
circuit_depth(M) :- makespan(M).
swaps_used(S) :- swap_count(S).

% Gate schedule: for each time step, list gates executed
gate_at(T, G) :- executed(G, T).

% ========== OPTIMIZATION ==========
% Primary: minimize depth, Secondary: minimize swaps
#minimize { 1@1, M : makespan(M) }.
#minimize { 1@2, S : swap_count(S) }.

% ========== SHOW DIRECTIVES ==========
#show circuit_depth/1.
#show swaps_used/1.
#show gate_at/2.