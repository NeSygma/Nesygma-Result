% Vertices
vertex(0..15).
partition(1..4).

% Edges (U < V)
edge(0, 1, 10). edge(0, 2, 10). edge(0, 3, 10).
edge(1, 2, 10). edge(1, 3, 10).
edge(2, 3, 10).

edge(4, 5, 10). edge(4, 6, 10). edge(4, 7, 10).
edge(5, 6, 10). edge(5, 7, 10).
edge(6, 7, 10).

edge(8, 9, 10). edge(8, 10, 10). edge(8, 11, 10).
edge(9, 10, 10). edge(9, 11, 10).
edge(10, 11, 10).

edge(12, 13, 10). edge(12, 14, 10). edge(12, 15, 10).
edge(13, 14, 10). edge(13, 15, 10).
edge(14, 15, 10).

edge(3, 4, 1).
edge(7, 8, 2).
edge(11, 12, 3).
edge(0, 15, 1).
edge(1, 6, 2).
edge(5, 10, 3).
edge(9, 14, 1).

% Partitioning
1 { assigned(V, P) : partition(P) } 1 :- vertex(V).
:- partition(P), not 4 { assigned(V, P) : vertex(V) } 4.

% Cut weight
crosses(U, V, W) :- edge(U, V, W), assigned(U, P1), assigned(V, P2), P1 != P2.
total_weight(S) :- S = #sum { W, U, V : crosses(U, V, W) }.

#minimize { S : total_weight(S) }.

% Output
#show assigned/2.
#show total_weight/1.
#show crosses/3.