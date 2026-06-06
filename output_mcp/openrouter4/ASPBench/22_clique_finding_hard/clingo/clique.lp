% Define vertices
vertex(0..19).

% Vertex types
type(0, alpha). type(1, alpha). type(2, alpha). type(3, alpha). type(4, beta).
type(5, alpha). type(6, beta). type(7, beta). type(8, beta). type(9, delta).
type(10, delta). type(11, beta). type(12, gamma). type(13, gamma). type(14, gamma).
type(15, delta). type(16, delta). type(17, gamma). type(18, alpha). type(19, beta).

% Vertex weights
weight(0,20). weight(1,20). weight(2,15). weight(3,20). weight(4,30).
weight(5,15). weight(6,30). weight(7,30). weight(8,18). weight(9,10).
weight(10,10). weight(11,12). weight(12,25). weight(13,25). weight(14,20).
weight(15,5). weight(16,5). weight(17,19). weight(18,40). weight(19,40).

% Edges (undirected) - symmetric
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

% Make edges symmetric
edge(Y,X) :- edge(X,Y).

% Choose which vertices are in the clique
{ in_clique(V) : vertex(V) }.

% Clique property: any two vertices in the clique must have an edge
:- in_clique(U), in_clique(V), U < V, not edge(U,V).

% Type diversity constraint: at most 2 vertices of any single type in the clique
:- type(T), #count { V : in_clique(V), type(V,T) } > 2.

% Weight limit constraint: total weight must be <= 100
total_weight(S) :- S = #sum { W,V : in_clique(V), weight(V,W) }.
:- total_weight(S), S > 100.

% Maximize clique size
#maximize { 1,V : in_clique(V) }.

% Output
#show in_clique/1.
#show total_weight/1.