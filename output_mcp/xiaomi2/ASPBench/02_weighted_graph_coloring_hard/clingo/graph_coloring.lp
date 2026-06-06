% ============ DOMAINS ============
vertex(1..36).
color(1..5).

% ============ WEIGHTS ============
weight(V, 10) :- V = 1..5.
weight(V, 3) :- V = 6..15.
weight(V, 5) :- V = 16..25.
weight(V, 7) :- V = 26..36.

% ============ CHOICE: assign exactly one color per vertex ============
1 { color_of(V, C) : color(C) } 1 :- vertex(V).

% ============ EDGES (undirected, stored with A < B) ============

% --- Core Clique K5: vertices 1-5 ---
edge(1,2). edge(1,3). edge(1,4). edge(1,5).
edge(2,3). edge(2,4). edge(2,5).
edge(3,4). edge(3,5).
edge(4,5).

% --- Cluster A ring (6-15) ---
edge(6,7). edge(7,8). edge(8,9). edge(9,10). edge(10,11).
edge(11,12). edge(12,13). edge(13,14). edge(14,15). edge(6,15).

% --- Cluster A diagonal chords ---
edge(6,9). edge(7,10). edge(8,11). edge(9,12). edge(10,13).
edge(11,14). edge(12,15). edge(6,13). edge(7,14). edge(8,15).

% --- Cluster A to core ---
edge(1,6). edge(2,6). edge(2,9). edge(3,9). edge(3,12). edge(4,12). edge(4,15). edge(5,15).

% --- Cluster B horizontal (16-20 row1, 21-25 row2) ---
edge(16,17). edge(17,18). edge(18,19). edge(19,20).
edge(21,22). edge(22,23). edge(23,24). edge(24,25).

% --- Cluster B vertical ---
edge(16,21). edge(17,22). edge(18,23). edge(19,24). edge(20,25).

% --- Cluster B diagonal ---
edge(16,22). edge(17,23). edge(18,24). edge(19,25).

% --- Cluster B to core ---
edge(1,16). edge(5,20).

% --- Cluster B to Cluster A ---
edge(8,18). edge(13,23).

% --- Cluster C cycle (26-36) ---
edge(26,27). edge(27,28). edge(28,29). edge(29,30). edge(30,31).
edge(31,32). edge(32,33). edge(33,34). edge(34,35). edge(35,36). edge(26,36).

% --- Cluster C chords (3 apart) ---
edge(26,29). edge(27,30). edge(28,31). edge(29,32). edge(30,33).
edge(31,34). edge(32,35). edge(33,36). edge(26,34). edge(27,35). edge(28,36).

% --- Cluster C to core ---
edge(1,26). edge(5,26). edge(3,31).

% --- Cluster C to Cluster B ---
edge(19,28). edge(24,33).

% ============ CONSTRAINT 1: Proper coloring ============
:- edge(A, B), color_of(A, C), color_of(B, C).

% ============ CONSTRAINT 2: Weighted cost <= 850 ============
vcost(V, W*C) :- color_of(V, C), weight(V, W).
total_cost(S) :- S = #sum { K, V : vcost(V, K) }.
:- total_cost(S), S > 850.

% ============ OUTPUT ============
#show color_of/2.
#show total_cost/1.