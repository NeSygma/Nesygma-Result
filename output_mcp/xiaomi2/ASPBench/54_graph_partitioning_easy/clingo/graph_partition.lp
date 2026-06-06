% Vertices
vertex(0..7).

% Edges (undirected, stored with from < to)
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).

% Assign each vertex to exactly one partition (1 or 2)
1 { assign(V, 1); assign(V, 2) } 1 :- vertex(V).

% Exactly 4 vertices in partition 1
:- #count { V : assign(V, 1) } != 4.

% Exactly 4 vertices in partition 2
:- #count { V : assign(V, 2) } != 4.

% An edge crosses if its endpoints are in different partitions
crosses(U, V) :- edge(U, V), assign(U, P1), assign(V, P2), P1 != P2.

% Count crossing edges
cut_size(N) :- N = #count { U,V : crosses(U,V), edge(U,V) }.

% Minimize the cut size
#minimize { 1,U,V : crosses(U,V), edge(U,V) }.

% Output
#show assign/2.
#show cut_size/1.
#show crosses/2.