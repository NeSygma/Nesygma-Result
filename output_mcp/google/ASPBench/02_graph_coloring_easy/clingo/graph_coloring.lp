% Vertices
vertex(1..6).

% Edges
edge(1,2). edge(1,3).
edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Undirected edges
edge(Y, X) :- edge(X, Y).

% Colors
color(1..6).

% Each vertex must be assigned exactly one color
1 { assigned(V, C) : color(C) } 1 :- vertex(V).

% No two adjacent vertices can have the same color
:- assigned(V1, C), assigned(V2, C), edge(V1, V2).

% Track used colors
used(C) :- assigned(_, C).

% Objective: Minimize the number of colors used
#minimize { 1, C : used(C) }.

% Output
num_colors(N) :- N = #count { C : used(C) }.
#show num_colors/1.
#show assigned/2.