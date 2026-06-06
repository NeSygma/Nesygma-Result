% --- Declare the vertices ---
vertex(0..15).

% --- Declare the edges ---
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

edge(3, 4, 1). edge(7, 8, 2). edge(11, 12, 3). edge(15, 0, 1).
edge(1, 6, 2). edge(5, 10, 3). edge(9, 14, 1).

% Ensure edges are undirected by adding reverse edges
edge(V1, V2, W) :- edge(V2, V1, W), vertex(V1), vertex(V2).

% --- Assign vertices to partitions ---
% Choice rule: Assign each vertex to a partition (1 to 4)
1 { partition(V, P) : P = 1..4 } 1 :- vertex(V).

% --- Ensure each partition has exactly 4 vertices ---
:- partition(V, P), #count{V : partition(V, P)} != 4.

% --- Identify edges crossing partitions (cut edges) ---
cut_edge(U, V, W) :-
    edge(U, V, W),
    partition(U, P1),
    partition(V, P2),
    P1 != P2.

% --- Calculate the total cut weight ---
cut_weight_total(W) :- W = #sum { W, U, V : cut_edge(U, V, W) }.

% --- Minimize the total cut weight ---
#minimize { W : cut_weight_total(W) }.

% --- Show the partition assignments and cut edges ---
#show partition/2.
#show cut_edge/3.
#show cut_weight_total/1.