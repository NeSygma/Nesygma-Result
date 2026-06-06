% Graph Coloring Problem - Find minimum number of colors

% Instance Data
vertex(1..6).

% Edges (undirected)
edge(1,2). edge(1,3).
edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Make edges symmetric for adjacency checking
adj(X,Y) :- edge(X,Y).
adj(X,Y) :- edge(Y,X).

% We need to find the minimum number of colors.
% Since we know the optimal is 3, we can try k=1,2,3...
% But let's use optimization to find the minimum.

% Maximum possible colors is the number of vertices
max_colors(6).

% Define color numbers up to max possible
color(1..C) :- max_colors(C).

% Each vertex gets exactly one color
1 { assign(V, C) : color(C) } 1 :- vertex(V).

% Constraint: adjacent vertices cannot share the same color
:- adj(V1, V2), assign(V1, C), assign(V2, C).

% Count how many colors are actually used
used_color(C) :- assign(V, C).
num_colors(N) :- N = #count { C : used_color(C) }.

% Minimize the number of colors used
#minimize { 1, C : used_color(C) }.

% Show results
#show num_colors/1.
#show assign/2.