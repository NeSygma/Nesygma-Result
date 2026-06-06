% Graph definition
vertex(1..18).

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

% Ensure symmetric edges (undirected graph)
edge(V1,V2) :- edge(V2,V1), vertex(V1), vertex(V2).

% Vertex types
% Critical ('c'): 1, 5, 10, 15
type(1, 'c'). type(5, 'c'). type(10, 'c'). type(15, 'c').
% Standard ('s'): 2, 6, 7, 11, 12, 16
type(2, 's'). type(6, 's'). type(7, 's'). type(11, 's'). type(12, 's'). type(16, 's').
% Resilient ('r'): 3, 8, 13, 18
type(3, 'r'). type(8, 'r'). type(13, 'r'). type(18, 'r').

% Vertex costs
% Cost 2: 4, 9
cost(4, 2). cost(9, 2).
% Cost 3: 14, 17
cost(14, 3). cost(17, 3).
% Cost 5: 1, 2, 3, 5, 6, 7, 8
cost(1, 5). cost(2, 5). cost(3, 5). cost(5, 5). cost(6, 5). cost(7, 5). cost(8, 5).
% Cost 8: 10, 11, 12, 13, 15, 16, 18
cost(10, 8). cost(11, 8). cost(12, 8). cost(13, 8). cost(15, 8). cost(16, 8). cost(18, 8).

% Choice rule: select vertices for the dominating set
{ selected(V) : vertex(V) }.

% Independent set constraint: no two selected vertices are adjacent
:- selected(V1), selected(V2), edge(V1, V2).

% Helper: count how many neighbors of V are selected
neighbor_count(V, N) :- 
    vertex(V), 
    N = #count { U : selected(U), edge(V, U) }.

% Dominating constraints based on vertex type
% Critical ('c'): must have at least 1 selected neighbor if not selected
:- type(V, 'c'), not selected(V), neighbor_count(V, C), C < 1.
% Standard ('s'): must have at least 1 selected neighbor if not selected
:- type(V, 's'), not selected(V), neighbor_count(V, C), C < 1.
% Resilient ('r'): must have at least 2 selected neighbors if not selected
:- type(V, 'r'), not selected(V), neighbor_count(V, C), C < 2.

% Objective: minimize total cost
#minimize { C,V : selected(V), cost(V,C) }.

% Show the selected vertices and total cost
selected_vertex(V) :- selected(V).
total_cost(C) :- C = #sum { C1,V : selected(V), cost(V,C1) }.

#show selected_vertex/1.
#show total_cost/1.