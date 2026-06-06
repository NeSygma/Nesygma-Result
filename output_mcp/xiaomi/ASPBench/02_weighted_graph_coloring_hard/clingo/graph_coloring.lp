% ============================================
% Graph Coloring with Weighted Cost Constraint
% ============================================

% ---- Domain: Vertices ----
vertex(1..36).

% ---- Domain: Colors ----
color(1..5).

% ---- Weights ----
weight(V, 10) :- V = 1..5.
weight(V, 3) :- V = 6..15.
weight(V, 5) :- V = 16..25.
weight(V, 7) :- V = 26..36.

% ---- Core Clique (K5): vertices 1-5, all pairs connected ----
edge(1,2). edge(1,3). edge(1,4). edge(1,5).
edge(2,3). edge(2,4). edge(2,5).
edge(3,4). edge(3,5).
edge(4,5).

% ---- Cluster A (vertices 6-15): Ring structure ----
edge(6,7). edge(7,8). edge(8,9). edge(9,10). edge(10,11).
edge(11,12). edge(12,13). edge(13,14). edge(14,15). edge(15,6).

% Cluster A: Diagonal chords
edge(6,9). edge(7,10). edge(8,11). edge(9,12). edge(10,13).
edge(11,14). edge(12,15). edge(13,6). edge(14,7). edge(15,8).

% Cluster A: Connections to core
edge(6,1). edge(6,2).
edge(9,2). edge(9,3).
edge(12,3). edge(12,4).
edge(15,4). edge(15,5).

% ---- Cluster B (vertices 16-25): Grid structure ----
% Horizontal edges (row 1)
edge(16,17). edge(17,18). edge(18,19). edge(19,20).
% Horizontal edges (row 2)
edge(21,22). edge(22,23). edge(23,24). edge(24,25).
% Vertical edges
edge(16,21). edge(17,22). edge(18,23). edge(19,24). edge(20,25).
% Diagonal edges
edge(16,22). edge(17,23). edge(18,24). edge(19,25).

% Cluster B: Connections to core
edge(16,1).
edge(20,5).

% Cluster B: Connections to Cluster A
edge(18,8).
edge(23,13).

% ---- Cluster C (vertices 26-36): 11-cycle with chords ----
% Cycle edges
edge(26,27). edge(27,28). edge(28,29). edge(29,30). edge(30,31).
edge(31,32). edge(32,33). edge(33,34). edge(34,35). edge(35,36). edge(36,26).

% Chord edges (3 steps apart)
edge(26,29). edge(27,30). edge(28,31). edge(29,32). edge(30,33).
edge(31,34). edge(32,35). edge(33,36). edge(34,26). edge(35,27). edge(36,28).

% Cluster C: Connections to core
edge(26,1). edge(26,5).
edge(31,3).

% Cluster C: Connections to Cluster B
edge(28,19).
edge(33,24).

% ---- Symmetric adjacency (undirected graph) ----
adjacent(V1, V2) :- edge(V1, V2).
adjacent(V1, V2) :- edge(V2, V1).

% ---- Choice: Assign exactly one color to each vertex ----
1 { colored(V, C) : color(C) } 1 :- vertex(V).

% ---- Constraint 1: No two adjacent vertices share the same color ----
:- adjacent(V1, V2), colored(V1, C), colored(V2, C).

% ---- Constraint 3: All 5 colors must be used (due to K5 core) ----
% The K5 clique (vertices 1-5) forces all 5 colors to be used
% since they are all mutually adjacent. This is automatically enforced
% by the adjacency constraint above.

% ---- Constraint 5: Weighted cost must be <= 850 ----
weighted_cost(S) :- S = #sum { W*C, V : colored(V, C), weight(V, W) }.
:- weighted_cost(S), S > 850.

% ---- Show the coloring ----
#show colored/2.
#show weighted_cost/1.