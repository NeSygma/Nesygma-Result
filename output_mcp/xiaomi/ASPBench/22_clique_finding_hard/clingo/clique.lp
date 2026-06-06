% ============ DOMAIN ============
vertex(0..19).

% Vertex types
type(0, alpha). type(1, alpha). type(2, alpha). type(3, alpha). type(5, alpha). type(18, alpha).
type(4, beta). type(6, beta). type(7, beta). type(8, beta). type(11, beta). type(19, beta).
type(9, delta). type(10, delta). type(15, delta). type(16, delta).
type(12, gamma). type(13, gamma). type(14, gamma). type(17, gamma).

% Vertex weights
weight(0, 20). weight(1, 20). weight(2, 15). weight(3, 20). weight(4, 30).
weight(5, 15). weight(6, 30). weight(7, 30). weight(8, 18). weight(9, 10).
weight(10, 10). weight(11, 12). weight(12, 25). weight(13, 25). weight(14, 20).
weight(15, 5). weight(16, 5). weight(17, 19). weight(18, 40). weight(19, 40).

% Edges (undirected, stored with smaller vertex first)
edge(0,1). edge(0,3). edge(0,4). edge(0,6). edge(0,7). edge(0,9). edge(0,10).
edge(1,3). edge(1,4). edge(1,6). edge(1,7). edge(1,9).
edge(2,5). edge(2,8). edge(2,11). edge(2,14). edge(2,17). edge(2,18).
edge(3,4). edge(3,6). edge(3,7). edge(3,9).
edge(4,6). edge(4,7). edge(4,9).
edge(5,8). edge(5,11). edge(5,14). edge(5,17). edge(5,19).
edge(6,7). edge(6,9).
edge(7,9).
edge(8,11). edge(8,14). edge(8,17).
edge(11,14). edge(11,17).
edge(12,13).
edge(14,17).
edge(15,16).

% Make edge symmetric for lookup
edge_sym(V1, V2) :- edge(V1, V2).
edge_sym(V1, V2) :- edge(V2, V1).

% ============ CHOICE: SELECT CLIQUE ============
{ in_clique(V) } :- vertex(V).

% ============ CONSTRAINT 1: CLIQUE PROPERTY ============
% Every pair of vertices in the clique must have an edge
:- in_clique(V1), in_clique(V2), V1 < V2, not edge(V1, V2).

% ============ CONSTRAINT 2: TYPE DIVERSITY ============
% Count vertices of each type in the clique
type_count(T, N) :- type_name(T), N = #count{V : in_clique(V), type(V, T)}.
:- type_count(T, N), N > 2.

% Type names
type_name(alpha). type_name(beta). type_name(gamma). type_name(delta).

% ============ CONSTRAINT 3: WEIGHT LIMIT ============
total_weight(W) :- W = #sum{Wt, V : in_clique(V), weight(V, Wt)}.
:- total_weight(W), W > 100.

% ============ OBJECTIVE: MAXIMIZE CLIQUE SIZE ============
clique_size(N) :- N = #count{V : in_clique(V)}.
#maximize { N : clique_size(N) }.

% ============ OUTPUT ============
#show in_clique/1.
#show clique_size/1.
#show total_weight/1.