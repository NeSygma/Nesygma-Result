% vertices
vertex(0..5).
% directed edges
edge(0,1). edge(0,2). edge(1,2). edge(1,3). edge(1,4). edge(2,1). edge(2,3). edge(2,4). edge(3,4). edge(3,5). edge(4,3). edge(4,5).
% positions 1..6 (path length = number of vertices)
pos(1..6).
% each position gets exactly one vertex
1 { at(V,P) : vertex(V) } 1 :- pos(P).
% each vertex appears exactly once
1 { at(V,P) : pos(P) } 1 :- vertex(V).
% start and end constraints
:- not at(0,1).
:- not at(5,6).
% edge continuity constraint
:- at(V,P), at(W,P1), P1 = P+1, not edge(V,W), pos(P), pos(P1).
% expose path as predicate path(Position,Vertex)
path(P,V) :- at(V,P).
% existence sentinel
exists :- at(0,1).
#show path/2.
#show exists/0.