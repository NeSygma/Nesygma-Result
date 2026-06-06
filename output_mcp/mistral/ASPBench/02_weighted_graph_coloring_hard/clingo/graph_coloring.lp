% Declare colors
color(1..5).

% Declare vertices
vertex(1..36).

% Declare weights
weight(1,10). weight(2,10). weight(3,10). weight(4,10). weight(5,10).
weight(6,3). weight(7,3). weight(8,3). weight(9,3). weight(10,3).
weight(11,3). weight(12,3). weight(13,3). weight(14,3). weight(15,3).
weight(16,5). weight(17,5). weight(18,5). weight(19,5). weight(20,5).
weight(21,5). weight(22,5). weight(23,5). weight(24,5). weight(25,5).
weight(26,7). weight(27,7). weight(28,7). weight(29,7). weight(30,7).
weight(31,7). weight(32,7). weight(33,7). weight(34,7). weight(35,7).
weight(36,7).

% Core clique (K5): all pairs connected
edge(1,2). edge(1,3). edge(1,4). edge(1,5).
edge(2,3). edge(2,4). edge(2,5).
edge(3,4). edge(3,5).
edge(4,5).

% Cluster A: vertices 6-15
% Ring structure
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

% Cluster B: vertices 16-25 (2x5 grid)
% Horizontal edges
edge(16,17). edge(17,18). edge(18,19). edge(19,20).
edge(21,22). edge(22,23). edge(23,24). edge(24,25).
% Vertical edges
edge(16,21). edge(17,22). edge(18,23). edge(19,24). edge(20,25).
% Diagonal edges
edge(16,22). edge(17,23). edge(18,24). edge(19,25).
% Connections to core
edge(16,1).
edge(20,5).
% Connections to Cluster A
edge(18,8).
edge(23,13).

% Cluster C: vertices 26-36 (11-cycle with chords)
% Cycle edges
edge(26,27). edge(27,28). edge(28,29). edge(29,30). edge(30,31).
edge(31,32). edge(32,33). edge(33,34). edge(34,35). edge(35,36). edge(36,26).
% Chords (3 steps apart)
edge(26,29). edge(27,30). edge(28,31). edge(29,32). edge(30,33).
edge(31,34). edge(32,35). edge(33,36). edge(34,26). edge(35,27). edge(36,28).
% Connections to core
edge(26,1). edge(26,5).
edge(31,3).
% Connections to Cluster B
edge(28,19).
edge(33,24).

% Assign exactly one color to each vertex
{ coloring(V, C) : color(C) } = 1 :- vertex(V).

% No two adjacent vertices can have the same color
:- edge(V1, V2), coloring(V1, C), coloring(V2, C).

% Track which colors are used
used_color(C) :- coloring(V, C).

% Ensure all 5 colors are used
:- color(C), not used_color(C).

% Calculate weighted cost: sum over all vertices of (color(v) * weight(v))
weighted_cost(Cost) :- Cost = #sum { C*W, V : vertex(V), coloring(V, C), weight(V, W) }.

% Cost must be <= 850
:- weighted_cost(Cost), Cost > 850.

% Show the coloring
#show coloring/2.