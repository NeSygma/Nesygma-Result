% Graph with 18 vertices
vertex(1..18).

% Undirected edges (as given)
edge(1,2). edge(1,4). edge(1,5).
edge(2,4). edge(2,5).
edge(3,4). edge(3,9).
edge(4,5). edge(4,18).
edge(6,7). edge(6,9). edge(6,10).
edge(7,9).
edge(8,9). edge(8,14).
edge(9,10).
edge(11,12). edge(11,14).
edge(12,14).
edge(13,14). edge(13,17).
edge(15,16). edge(15,17).
edge(16,17).
edge(17,18).

% Make adjacency symmetric
adjacent(V1, V2) :- edge(V1, V2).
adjacent(V1, V2) :- edge(V2, V1).

% Vertex types
type(1, c). type(5, c). type(10, c). type(15, c).
type(2, s). type(6, s). type(7, s). type(11, s). type(12, s). type(16, s).
type(3, r). type(8, r). type(13, r). type(18, r).

% Domination requirement per vertex
% Resilient vertices need 2 adjacent dominating vertices
req(V, 2) :- type(V, r).
% All other vertices (critical, standard, untyped) need at least 1
req(V, 1) :- vertex(V), not type(V, r).

% Costs
cost(4,2). cost(9,2).
cost(14,3). cost(17,3).
cost(1,5). cost(2,5). cost(3,5). cost(5,5). cost(6,5). cost(7,5). cost(8,5).
cost(10,8). cost(11,8). cost(12,8). cost(13,8). cost(15,8). cost(16,8). cost(18,8).

% --- Choice: select vertices for dominating set ---
{ in_set(V) : vertex(V) }.

% --- Constraint 1: Independent set (no two adjacent vertices both selected) ---
:- in_set(V1), in_set(V2), adjacent(V1, V2), V1 < V2.

% --- Domination constraints ---
% Count how many dominating vertices are adjacent to each vertex
adj_dominators(V, N) :- N = #count { U : in_set(U), adjacent(V, U) }, vertex(V).

% Each vertex not in the set must have enough adjacent dominating vertices
:- vertex(V), not in_set(V), adj_dominators(V, C), req(V, R), C < R.

% --- Objective: minimize total cost ---
total_cost(S) :- S = #sum { C, V : in_set(V), cost(V, C) }.
#minimize { C, V : in_set(V), cost(V, C) }.

% --- Output ---
#show in_set/1.
#show total_cost/1.