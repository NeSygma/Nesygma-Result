% --- Domain Definitions ---
vertex(0..5).
position_index(0..5).

% --- Directed Edges ---
edge(0,1). edge(0,2). edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4). edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Start and end vertices
start(0).
end(5).

% --- Assignment: each vertex gets exactly one position ---
1 { position(V, P) : position_index(P) } 1 :- vertex(V).

% --- Each position has exactly one vertex ---
1 { position(V, P) : vertex(V) } 1 :- position_index(P).

% --- Start vertex must be at position 0 ---
:- position(0, P), P != 0.

% --- End vertex must be at position 5 ---
:- position(5, P), P != 5.

% --- Consecutive positions must follow a directed edge ---
:- position(U, P), position(V, Q), P+1 = Q, not edge(U, V).

% --- Output: show the position assignment for each vertex ---
#show position/2.

% --- Also show a path representation for readability ---
path_sequence(P, V) :- position(V, P).
#show path_sequence/2.