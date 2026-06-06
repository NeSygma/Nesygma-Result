% Graph Coloring Problem
% Vertices: 1..6
% Edges as given

vertex(1..6).

% Edges (undirected)
edge(1,2). edge(1,3).
edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Assign each vertex a color from 1 to 6 (upper bound)
1 { color(V, C) : C = 1..6 } 1 :- vertex(V).

% Adjacent vertices must have different colors
:- edge(U,V), color(U,C), color(V,C).

% Count distinct colors used
num_colors(N) :- N = #count { C : color(_, C) }.

% Minimize the number of colors used
#minimize { N : num_colors(N) }.

% Show the coloring and the number of colors
#show color/2.
#show num_colors/1.