% === Domain ===
vertex(0..5).
position(0..5).

% === Directed Edges ===
edge(0,1). edge(0,2). edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4). edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% === Choice: assign each vertex to exactly one position ===
1 { in_path(V, P) : position(P) } 1 :- vertex(V).

% === Each position has exactly one vertex ===
1 { in_path(V, P) : vertex(V) } 1 :- position(P).

% === Start at vertex 0, end at vertex 5 ===
in_path(0, 0).
in_path(5, 5).

% === Consecutive positions must follow a directed edge ===
:- position(P), P < 5, in_path(V1, P), in_path(V2, P+1), not edge(V1, V2).

% === Output: show the path as ordered sequence ===
path_at(P, V) :- in_path(V, P), position(P).

#show path_at/2.