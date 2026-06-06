% vertices
vertex(1..6).
% edges
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% choice of removed vertices
{removed(V)} :- vertex(V).
keep(V) :- vertex(V), not removed(V).

% rank domain
rank_range(1..6).
% assign exactly one rank to each kept vertex
1 { rank(V,R) : rank_range(R) } 1 :- keep(V).
% distinct ranks for distinct kept vertices
:- rank(V,R), rank(W,R), V != W, keep(V), keep(W).
% enforce acyclicity: for each edge between kept vertices, rank must increase
:- edge(U,V), keep(U), keep(V), rank(U,R1), rank(V,R2), R1 >= R2.

% minimize number of removed vertices
#minimize { 1, V : removed(V) }.

#show removed/1.
#show rank/2.