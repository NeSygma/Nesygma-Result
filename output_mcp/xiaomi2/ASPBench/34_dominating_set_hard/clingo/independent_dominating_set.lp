% Vertices
vertex(1..18).

% Edges (undirected, so we store both directions)
edge(1,2). edge(1,4). edge(1,5). edge(2,4). edge(2,5).
edge(3,4). edge(3,9). edge(4,5). edge(4,18).
edge(6,7). edge(6,9). edge(6,10). edge(7,9). edge(8,9).
edge(8,14). edge(9,10). edge(11,12). edge(11,14).
edge(12,14). edge(13,14). edge(13,17). edge(15,16).
edge(15,17). edge(16,17). edge(17,18).

% Symmetric edges
edge(X,Y) :- edge(Y,X).

% Vertex types
type(1,c). type(5,c). type(10,c). type(15,c).
type(2,s). type(6,s). type(7,s). type(11,s). type(12,s). type(16,s).
type(3,r). type(8,r). type(13,r). type(18,r).

% Vertex costs
cost(4,2). cost(9,2).
cost(14,3). cost(17,3).
cost(1,5). cost(2,5). cost(3,5). cost(5,5). cost(6,5). cost(7,5). cost(8,5).
cost(10,8). cost(11,8). cost(12,8). cost(13,8). cost(15,8). cost(16,8). cost(18,8).

% Choice: select each vertex into the dominating set or not
{ in_set(V) } :- vertex(V).

% Constraint 1: Independent set - no two adjacent vertices can both be in the set
:- in_set(V1), in_set(V2), edge(V1, V2), V1 < V2.

% Count neighbors in the dominating set for each vertex
neighbor_count(V, N) :- vertex(V), N = #count{ U : edge(V, U), in_set(U) }.

% Constraint 2 & 3: Critical and Standard vertices must be dominated (at least 1 neighbor in set, or in set themselves)
:- vertex(V), type(V, c), not in_set(V), neighbor_count(V, 0).
:- vertex(V), type(V, s), not in_set(V), neighbor_count(V, 0).

% Constraint 4: Resilient vertices need at least 2 neighbors in set (or be in set themselves)
:- vertex(V), type(V, r), not in_set(V), neighbor_count(V, N), N < 2.

% Minimize total cost
total_cost(S) :- S = #sum{ C, V : in_set(V), cost(V, C) }.
#minimize { C, V : in_set(V), cost(V, C) }.

#show in_set/1.
#show total_cost/1.