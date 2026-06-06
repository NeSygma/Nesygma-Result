% Vertices with type and weight
vertex(0..19).

type(0, alpha). weight(0, 20).
type(1, alpha). weight(1, 20).
type(2, alpha). weight(2, 15).
type(3, alpha). weight(3, 20).
type(4, beta).  weight(4, 30).
type(5, alpha). weight(5, 15).
type(6, beta).  weight(6, 30).
type(7, beta).  weight(7, 30).
type(8, beta).  weight(8, 18).
type(9, delta). weight(9, 10).
type(10, delta). weight(10, 10).
type(11, beta). weight(11, 12).
type(12, gamma). weight(12, 25).
type(13, gamma). weight(13, 25).
type(14, gamma). weight(14, 20).
type(15, delta). weight(15, 5).
type(16, delta). weight(16, 5).
type(17, gamma). weight(17, 19).
type(18, alpha). weight(18, 40).
type(19, beta). weight(19, 40).

% Edges (undirected - store both directions)
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
edge(U, V) :- edge(V, U).

% Type names for diversity constraint
typename(alpha). typename(beta). typename(gamma). typename(delta).

% Choice: select vertices into the clique
{ in_clique(V) } :- vertex(V).

% Clique property: every pair of selected vertices must be connected
:- in_clique(U), in_clique(V), U < V, not edge(U, V).

% Type diversity: at most 2 vertices of any type
:- typename(T), #count{ V : in_clique(V), type(V, T) } > 2.

% Weight limit: total weight <= 100
total_weight(S) :- S = #sum{ W, V : in_clique(V), weight(V, W) }.
:- total_weight(S), S > 100.

% Maximize clique size
clique_size(N) :- N = #count{ V : in_clique(V) }.
#maximize { N : clique_size(N) }.

% Output
#show in_clique/1.
#show clique_size/1.
#show total_weight/1.