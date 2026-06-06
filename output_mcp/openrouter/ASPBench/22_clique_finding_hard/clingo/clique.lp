% Vertices
vertex(0..19).

% Types
type(0,alpha). type(1,alpha). type(2,alpha). type(3,alpha). type(4,beta). type(5,alpha). type(6,beta). type(7,beta). type(8,beta). type(9,delta). type(10,delta). type(11,beta). type(12,gamma). type(13,gamma). type(14,gamma). type(15,delta). type(16,delta). type(17,gamma). type(18,alpha). type(19,beta).

% Weights
weight(0,20). weight(1,20). weight(2,15). weight(3,20). weight(4,30). weight(5,15). weight(6,30). weight(7,30). weight(8,18). weight(9,10). weight(10,10). weight(11,12). weight(12,25). weight(13,25). weight(14,20). weight(15,5). weight(16,5). weight(17,19). weight(18,40). weight(19,40).

% Edges (undirected, both directions)
edge(0,1). edge(1,0).
edge(0,3). edge(3,0).
edge(0,4). edge(4,0).
edge(0,6). edge(6,0).
edge(0,7). edge(7,0).
edge(0,9). edge(9,0).
edge(0,10). edge(10,0).
edge(1,3). edge(3,1).
edge(1,4). edge(4,1).
edge(1,6). edge(6,1).
edge(1,7). edge(7,1).
edge(1,9). edge(9,1).
edge(2,5). edge(5,2).
edge(2,8). edge(8,2).
edge(2,11). edge(11,2).
edge(2,14). edge(14,2).
edge(2,17). edge(17,2).
edge(2,18). edge(18,2).
edge(3,4). edge(4,3).
edge(3,6). edge(6,3).
edge(3,7). edge(7,3).
edge(3,9). edge(9,3).
edge(4,6). edge(6,4).
edge(4,7). edge(7,4).
edge(4,9). edge(9,4).
edge(5,8). edge(8,5).
edge(5,11). edge(11,5).
edge(5,14). edge(14,5).
edge(5,17). edge(17,5).
edge(5,19). edge(19,5).
edge(6,7). edge(7,6).
edge(6,9). edge(9,6).
edge(7,9). edge(9,7).
edge(8,11). edge(11,8).
edge(8,14). edge(14,8).
edge(8,17). edge(17,8).
edge(11,14). edge(14,11).
edge(11,17). edge(17,11).
edge(12,13). edge(13,12).
edge(14,17). edge(17,14).
edge(15,16). edge(16,15).

% Domain for types
type_name(T) :- type(_,T).

% Choice of vertices in clique
{in_clique(V)} :- vertex(V).

% Clique property: every pair must be adjacent
:- in_clique(V), in_clique(W), V < W, not edge(V,W).

% Type diversity: at most 2 per type
:- type_name(T), #count{V : in_clique(V), type(V,T)} > 2.

% Weight limit
:- #sum{Wgt,V : in_clique(V), weight(V,Wgt)} > 100.

% Optimization: maximize size of clique
#maximize { 1,V : in_clique(V) }.

% Helper predicates for output
clique_size(N) :- N = #count{V : in_clique(V)}.
clique_total_weight(W) :- W = #sum{Wgt,V : in_clique(V), weight(V,Wgt)}.
type_count(T,N) :- type_name(T), N = #count{V : in_clique(V), type(V,T)}.
clique_edge(U,V) :- in_clique(U), in_clique(V), U < V, edge(U,V).

#show in_clique/1.
#show clique_size/1.
#show clique_total_weight/1.
#show type_count/2.
#show clique_edge/2.