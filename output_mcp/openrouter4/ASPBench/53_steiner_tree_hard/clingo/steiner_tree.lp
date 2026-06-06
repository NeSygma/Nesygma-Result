% --- DATA ---
vertex(0..11).
level(0..2).

% Vertex levels
vertex_level(0,2). vertex_level(1,2).
vertex_level(2,1). vertex_level(3,1). vertex_level(4,1). vertex_level(5,1).
vertex_level(6,0). vertex_level(7,0). vertex_level(8,0). vertex_level(9,0). vertex_level(10,0). vertex_level(11,0).

% Edges: edge(U, V, Weight, Type) with U < V
edge(0,2,5,fiber). edge(1,3,4,fiber). edge(2,3,3,fiber). edge(2,4,6,copper).
edge(2,6,2,copper). edge(3,5,2,fiber). edge(3,7,8,copper). edge(4,8,5,fiber).
edge(5,9,4,copper). edge(5,10,3,fiber). edge(6,7,1,copper). edge(9,10,7,fiber).
edge(10,11,2,copper).

% Resource costs
resource_cost(0,10). resource_cost(1,10). resource_cost(2,8). resource_cost(3,5).
resource_cost(4,7). resource_cost(5,6). resource_cost(6,2). resource_cost(7,2).
resource_cost(8,3). resource_cost(9,3). resource_cost(10,4). resource_cost(11,4).

% Terminals and groups
terminal(6). terminal(7). terminal(10). terminal(11).
terminal_group(6,a). terminal_group(7,a). terminal_group(10,b). terminal_group(11,b).

% --- GENERATION ---
% Choose which edges to include in the tree
{ selected(U, V, W, T) } :- edge(U, V, W, T).

% Vertices in the tree: terminals are always in the tree
in_tree(V) :- terminal(V).
% Vertices incident to selected edges are in the tree
in_tree(U) :- selected(U, V, _, _).
in_tree(V) :- selected(U, V, _, _).

% Steiner vertices are non-terminal vertices in the tree
steiner(V) :- in_tree(V), not terminal(V).

% --- CONSTRAINTS ---

% 1. Connectivity: All terminals must be mutually reachable via tree edges
% Symmetric version of selected edges for reachability
tree_edge(U, V, W, T) :- selected(U, V, W, T).
tree_edge(V, U, W, T) :- selected(U, V, W, T).

% Reachability in the tree
reaches(V, V) :- in_tree(V).
reaches(U, V) :- tree_edge(U, W, _, _), reaches(W, V).

% All terminals must be connected to each other
:- terminal(U), terminal(V), U != V, not reaches(U, V).

% 2. Acyclicity: Number of edges = Number of vertices in tree - 1
vertex_count(N) :- N = #count { V : in_tree(V) }.
edge_count(M) :- M = #count { U, V : selected(U, V, _, _) }.
:- vertex_count(N), edge_count(M), M != N - 1.

% 3. Hierarchy Constraint: Steiner vertex at level L cannot connect to vertex at level > L
:- selected(U, V, _, _), steiner(U), vertex_level(U, LU), vertex_level(V, LV), LV > LU.
:- selected(U, V, _, _), steiner(V), vertex_level(U, LU), vertex_level(V, LV), LU > LV.

% 4. Resource Budget: Sum of resource costs for Steiner vertices <= 20
total_steiner_cost(C) :- C = #sum { Cost, V : steiner(V), resource_cost(V, Cost) }.
:- total_steiner_cost(C), C > 20.

% 5. Edge Type Limit: At most 3 copper edges
copper_count(N) :- N = #count { U, V : selected(U, V, _, copper) }.
:- copper_count(N), N > 3.

% 6. Gateway Requirement: For each terminal group, at least one Steiner vertex connects directly to a terminal in that group
gateway(V, G) :- steiner(V), terminal_group(T, G), selected(V, T, _, _).
gateway(V, G) :- steiner(V), terminal_group(T, G), selected(T, V, _, _).

:- terminal_group(_, G), not gateway(_, G).

% 7. Gateway Connectivity: All gateways connected via path using only Steiner vertices
s_reaches(V, V) :- steiner(V).
s_reaches(U, V) :- tree_edge(U, W, _, _), steiner(W), s_reaches(W, V).

:- gateway(G1, _), gateway(G2, _), G1 != G2, not s_reaches(G1, G2).

% --- OBJECTIVE ---
% Minimize total edge weight
#minimize { Weight, U, V : selected(U, V, Weight, _) }.

% Compute total weight for output
total_weight(W) :- W = #sum { Weight, U, V : selected(U, V, Weight, _) }.

% --- OUTPUT ---
#show selected/4.
#show steiner/1.
#show gateway/2.
#show total_weight/1.
#show total_steiner_cost/1.
#show copper_count/1.