% Vertices
vertex(0..5).

% Edges
edge(0,1). edge(0,2). edge(1,2). edge(1,3). edge(1,4). edge(2,1). edge(2,3). edge(2,4). edge(3,4). edge(3,5). edge(4,3). edge(4,5).

% Each vertex must appear exactly once in the path (at some position 0..5)
1 { pos(V, P) : P = 0..5 } 1 :- vertex(V).

% Each position must be occupied by exactly one vertex
1 { pos(V, P) : vertex(V) } 1 :- P = 0..5.

% Start at 0, end at 5
:- not pos(0, 0).
:- not pos(5, 5).

% Path must follow directed edges
:- pos(U, P), pos(V, P+1), not edge(U, V), P < 5.

% Output formatting
#show pos/2.