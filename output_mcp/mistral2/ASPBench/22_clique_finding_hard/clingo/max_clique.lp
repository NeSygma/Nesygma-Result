% --- Declare the domain ---
vertex(0..19).
type(alpha; beta; gamma; delta).

% --- Vertex properties ---
weight(0,20). type_of(0,alpha).
weight(1,20). type_of(1,alpha).
weight(2,15). type_of(2,alpha).
weight(3,20). type_of(3,alpha).
weight(4,30). type_of(4,beta).
weight(5,15). type_of(5,alpha).
weight(6,30). type_of(6,beta).
weight(7,30). type_of(7,beta).
weight(8,18). type_of(8,beta).
weight(9,10). type_of(9,delta).
weight(10,10). type_of(10,delta).
weight(11,12). type_of(11,beta).
weight(12,25). type_of(12,gamma).
weight(13,25). type_of(13,gamma).
weight(14,20). type_of(14,gamma).
weight(15,5). type_of(15,delta).
weight(16,5). type_of(16,delta).
weight(17,19). type_of(17,gamma).
weight(18,40). type_of(18,alpha).
weight(19,40). type_of(19,beta).

% --- Edges (undirected) ---
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

% --- Clique choice rule ---
{ in_clique(V) : vertex(V) }.

% --- Clique property: all pairs in the clique must be connected by an edge ---
:- in_clique(U), in_clique(V), U < V, not edge(U, V).

% --- Type diversity: at most 2 vertices of each type in the clique ---
type_count(T, N) :- N = #count{ V : in_clique(V), type_of(V, T) }, type(T).
:- type_count(T, N), N > 2.

% --- Weight limit: total weight of the clique <= 100 ---
clique_total_weight(W) :- W = #sum{ Wt : in_clique(V), weight(V, Wt) }.
:- clique_total_weight(W), W > 100.

% --- Objective: maximize the size of the clique ---
#maximize { 1@1 : in_clique(V) }.

% --- Derive clique edges ---
clique_edge(U, V) :- in_clique(U), in_clique(V), edge(U, V), U < V.

% --- Derive clique size ---
clique_size(N) :- N = #count{ V : in_clique(V) }.

% --- Derive type distribution ---
type_in_clique(T, N) :- N = #count{ V : in_clique(V), type_of(V, T) }, type(T).

% --- Show the required outputs ---
#show in_clique/1.
#show clique_size/1.
#show clique_edge/2.
#show clique_total_weight/1.
#show type_in_clique/2.