% --- Data ---
vertex(0..19).

type(0, alpha). type(1, alpha). type(2, alpha). type(3, alpha). type(4, beta).
type(5, alpha). type(6, beta). type(7, beta). type(8, beta). type(9, delta).
type(10, delta). type(11, beta). type(12, gamma). type(13, gamma). type(14, gamma).
type(15, delta). type(16, delta). type(17, gamma). type(18, alpha). type(19, beta).

weight(0, 20). weight(1, 20). weight(2, 15). weight(3, 20). weight(4, 30).
weight(5, 15). weight(6, 30). weight(7, 30). weight(8, 18). weight(9, 10).
weight(10, 10). weight(11, 12). weight(12, 25). weight(13, 25). weight(14, 20).
weight(15, 5). weight(16, 5). weight(17, 19). weight(18, 40). weight(19, 40).

edge_raw(0,1). edge_raw(0,3). edge_raw(0,4). edge_raw(0,6). edge_raw(0,7). edge_raw(0,9). edge_raw(0,10).
edge_raw(1,3). edge_raw(1,4). edge_raw(1,6). edge_raw(1,7). edge_raw(1,9).
edge_raw(2,5). edge_raw(2,8). edge_raw(2,11). edge_raw(2,14). edge_raw(2,17). edge_raw(2,18).
edge_raw(3,4). edge_raw(3,6). edge_raw(3,7). edge_raw(3,9).
edge_raw(4,6). edge_raw(4,7). edge_raw(4,9).
edge_raw(5,8). edge_raw(5,11). edge_raw(5,14). edge_raw(5,17). edge_raw(5,19).
edge_raw(6,7). edge_raw(6,9).
edge_raw(7,9).
edge_raw(8,11). edge_raw(8,14). edge_raw(8,17).
edge_raw(11,14). edge_raw(11,17).
edge_raw(12,13).
edge_raw(14,17).
edge_raw(15,16).

edge(U, V) :- edge_raw(U, V).
edge(V, U) :- edge_raw(U, V).

% --- Logic ---
{ in_clique(V) } :- vertex(V).

% Clique constraint
:- in_clique(U), in_clique(V), U < V, not edge(U, V).

% Type diversity constraint
:- type(_, T), #count { V : in_clique(V), type(V, T) } > 2.

% Weight limit constraint
:- #sum { W, V : in_clique(V), weight(V, W) } > 100.

% Objective
#maximize { 1, V : in_clique(V) }.

% --- Output ---
clique_size(S) :- S = #count { V : in_clique(V) }.
clique_total_weight(W) :- W = #sum { Wt, V : in_clique(V), weight(V, Wt) }.
clique_type_distribution(T, C) :- type(_, T), C = #count { V : in_clique(V), type(V, T) }, C > 0.
clique_edges(U, V) :- in_clique(U), in_clique(V), U < V, edge(U, V).

#show in_clique/1.
#show clique_size/1.
#show clique_total_weight/1.
#show clique_type_distribution/2.
#show clique_edges/2.