% Define the directed graph
vertex(1..6).

edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% Choice rule: select a set of vertices to remove
{ removed(V) : vertex(V) }.

% Define the remaining graph: an edge u->v remains if neither u nor v is removed
remaining_edge(U,V) :- edge(U,V), not removed(U), not removed(V).

% Assign a position (topological order) to each remaining vertex
% We use a choice rule to assign positions; positions are integers from 0 to |V|-1
{ pos(V,P) : P = 0..5 } :- vertex(V), not removed(V).

% Ensure that for every remaining edge U->V, pos(U) < pos(V)
:- remaining_edge(U,V), pos(U,P1), pos(V,P2), P1 >= P2.

% Ensure that each remaining vertex has exactly one position
:- vertex(V), not removed(V), not 1 { pos(V,P) : P = 0..5 }.

% Ensure that positions are unique for remaining vertices
:- pos(V1,P), pos(V2,P), V1 != V2, not removed(V1), not removed(V2).

% Minimize the number of removed vertices
#minimize { V : removed(V) }.

% Show the removed vertices in the answer set
#show removed/1.
#show pos/2.