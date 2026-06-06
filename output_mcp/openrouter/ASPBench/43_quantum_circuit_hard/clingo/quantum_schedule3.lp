% Qubit adjacency (undirected)
adj(q0,q1). adj(q1,q0).
adj(q1,q2). adj(q2,q1).
adj(q2,q3). adj(q3,q2).
adj(q4,q5). adj(q5,q4).
adj(q5,q6). adj(q6,q5).
adj(q6,q7). adj(q7,q6).
adj(q0,q4). adj(q4,q0).
adj(q1,q5). adj(q5,q1).
adj(q2,q6). adj(q6,q2).
adj(q3,q7). adj(q7,q3).

% Logical qubits
logical(l0). logical(l1). logical(l2). logical(l3). logical(l4). logical(l5). logical(l6). logical(l7).

% Initial placement at time 0
at(l0,q0,0). at(l1,q1,0). at(l2,q2,0). at(l3,q3,0).
at(l4,q4,0). at(l5,q5,0). at(l6,q6,0). at(l7,q7,0).

% Time horizon (allow up to 5 steps)
time(1..5).

% Mandatory gates
mandatory_gate(h_q0).
mandatory_gate(x_q1).
mandatory_gate(cnot_q2_q3).
mandatory_gate(cnot_q4_q5).
mandatory_gate(cnot_q0_q2).
mandatory_gate(toffoli_q5_q7_q6).

% Gate requirements (logical qubits involved)
% gate_req(Gate, Logical)
gate_req(h_q0, l0).
gate_req(x_q1, l1).
gate_req(cnot_q2_q3, l2). gate_req(cnot_q2_q3, l3).
gate_req(cnot_q4_q5, l4). gate_req(cnot_q4_q5, l5).
gate_req(cnot_q0_q2, l0). gate_req(cnot_q0_q2, l2).
gate_req(toffoli_q5_q7_q6, l5). gate_req(toffoli_q5_q7_q6, l7). gate_req(toffoli_q5_q7_q6, l6).

% Gate type classification
single(h_q0). single(x_q1).
cnot(cnot_q2_q3). cnot(cnot_q4_q5). cnot(cnot_q0_q2).
toffoli(toffoli_q5_q7_q6).

% Assign each mandatory gate to exactly one time step
1 { gate_at(G,T) : time(T) } 1 :- mandatory_gate(G).

% Dependency: toffoli must be strictly after cnot_q4_q5
:- gate_at(toffoli_q5_q7_q6,T1), gate_at(cnot_q4_q5,T2), T1 <= T2.

% Swaps: allow up to 2 swaps per time step (unordered adjacent pairs)
{ swap(P1,P2,T) : adj(P1,P2), P1 < P2 } 0..2 :- time(T).

% Location update (persistence and movement via swaps)
% Persistence when not involved in a swap at previous step
at(L,P,T) :- at(L,P,T-1), time(T), not swap(P,_,T-1), not swap(_,P,T-1).
% Move due to a swap (both directions)
at(L,P,T) :- swap(P,P2,T-1), at(L,P2,T-1), time(T).
at(L,P,T) :- swap(P2,P,T-1), at(L,P2,T-1), time(T).

% Each logical qubit occupies exactly one physical qubit at each time
:- at(L,P1,T), at(L,P2,T), P1 != P2.
% Each physical qubit holds exactly one logical qubit at each time
:- at(L1,P,T), at(L2,P,T), L1 != L2.

% Gate adjacency constraints
% CNOT requires its two qubits to be adjacent
:- gate_at(G,T), cnot(G), gate_req(G,L1), gate_req(G,L2), L1 != L2,
   at(L1,P1,T), at(L2,P2,T), not adj(P1,P2).
% Toffoli requires both controls adjacent to the target
:- gate_at(G,T), toffoli(G),
   gate_req(G,Ctrl1), gate_req(G,Ctrl2), gate_req(G,Tgt),
   Ctrl1 != Ctrl2, Ctrl1 != Tgt, Ctrl2 != Tgt,
   at(Ctrl1,PC1,T), at(Ctrl2,PC2,T), at(Tgt,PT,T),
   not adj(PC1,PT), not adj(PC2,PT).

% Conflict: no two gates may use same physical qubit at same time
:- #count{ G : gate_at(G,T), gate_req(G,L), at(L,P,T) } > 1.

% Compute number of swaps used
swaps_used(N) :- N = #count { P1,P2,T : swap(P1,P2,T) }.
% Compute circuit depth (max time step with any action)
action_time(T) :- gate_at(_,T).
action_time(T) :- swap(_,_,T).
depth(D) :- D = #max { T : action_time(T) }.

#minimize { D : depth(D) }.
#minimize { 1,T,P1,P2 : swap(P1,P2,T) }.

#show gate_at/2.
#show swap/3.
#show depth/1.
#show swaps_used/1.