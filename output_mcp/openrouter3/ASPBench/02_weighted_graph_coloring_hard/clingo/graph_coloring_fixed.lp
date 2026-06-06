% Graph Coloring with Weighted Cost Constraint

% Define vertices
vertex(1..36).

% Define colors
color(1..5).

% Define weights for each vertex
weight(1,10). weight(2,10). weight(3,10). weight(4,10). weight(5,10).
weight(6,3). weight(7,3). weight(8,3). weight(9,3). weight(10,3).
weight(11,3). weight(12,3). weight(13,3). weight(14,3). weight(15,3).
weight(16,5). weight(17,5). weight(18,5). weight(19,5). weight(20,5).
weight(21,5). weight(22,5). weight(23,5). weight(24,5). weight(25,5).
weight(26,7). weight(27,7). weight(28,7). weight(29,7). weight(30,7).
weight(31,7). weight(32,7). weight(33,7). weight(34,7). weight(35,7). weight(36,7).

% Define edges (adjacency relationships)
% Core clique (K5): vertices 1-5 form a complete graph
edge(1,2). edge(1,3). edge(1,4). edge(1,5).
edge(2,3). edge(2,4). edge(2,5).
edge(3,4). edge(3,5).
edge(4,5).

% Cluster A: Ring structure (vertices 6-15)
edge(6,7). edge(7,8). edge(8,9). edge(9,10). edge(10,11).
edge(11,12). edge(12,13). edge(13,14). edge(14,15). edge(15,6).
% Diagonal chords
edge(6,9). edge(7,10). edge(8,11). edge(9,12). edge(10,13).
edge(11,14). edge(12,15). edge(13,6). edge(14,7). edge(15,8).
% Connections to core
edge(6,1). edge(6,2).
edge(9,2). edge(9,3).
edge(12,3). edge(12,4).
edge(15,4). edge(15,5).

% Cluster B: Grid structure (vertices 16-25)
% Horizontal edges
edge(16,17). edge(17,18). edge(18,19). edge(19,20).
edge(21,22). edge(22,23). edge(23,24). edge(24,25).
% Vertical edges
edge(16,21). edge(17,22). edge(18,23). edge(19,24). edge(20,25).
% Diagonal edges
edge(16,22). edge(17,23). edge(18,24). edge(19,25).
% Connections to core
edge(16,1). edge(20,5).
% Connections to Cluster A
edge(18,8). edge(23,13).

% Cluster C: 11-cycle with chords (vertices 26-36)
% Cycle edges
edge(26,27). edge(27,28). edge(28,29). edge(29,30). edge(30,31).
edge(31,32). edge(32,33). edge(33,34). edge(34,35). edge(35,36). edge(36,26).
% Chord edges (3 steps apart)
edge(26,29). edge(27,30). edge(28,31). edge(29,32). edge(30,33).
edge(31,34). edge(32,35). edge(33,36). edge(34,26). edge(35,27). edge(36,28).
% Connections to core
edge(26,1). edge(26,5). edge(31,3).
% Connections to Cluster B
edge(28,19). edge(33,24).

% Make edges symmetric (undirected graph)
edge(X,Y) :- edge(Y,X).

% Each vertex gets exactly one color
1 { colored(V, C) : color(C) } 1 :- vertex(V).

% No two adjacent vertices can have the same color
:- colored(V1, C), colored(V2, C), edge(V1, V2).

% All 5 colors must be used (due to K5 core)
% Since vertices 1-5 form a K5, they must all have different colors
% So we just need to ensure all colors are used somewhere
used_color(C) :- colored(V, C), vertex(V).
:- not used_color(1), not used_color(2), not used_color(3), not used_color(4), not used_color(5).

% Calculate weighted cost
% For each vertex, multiply its color by its weight
vertex_cost(V, Cost) :- colored(V, C), weight(V, W), Cost = C * W.
weighted_cost(Sum) :- Sum = #sum { Cost : vertex_cost(V, Cost) }.

% Cost must be ≤ 850
:- weighted_cost(Sum), Sum > 850.

% Show the coloring and cost
#show colored/2.
#show weighted_cost/1.