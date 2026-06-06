% Graph Coloring Problem - Chromatic Number Minimization

% --- Domain ---
vertex(1..6).

% --- Edges ---
edge(1,2). edge(1,3).
edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Adjacency relation (undirected)
adjacent(V1,V2) :- edge(V1,V2).
adjacent(V1,V2) :- edge(V2,V1).

% Maximum possible colors (upper bound = number of vertices)
max_color(1..6).

% --- Assignment: each vertex gets exactly one color ---
1 { color(V,C) : max_color(C) } 1 :- vertex(V).

% --- Constraint: adjacent vertices must have different colors ---
:- adjacent(V1,V2), color(V1,C), color(V2,C).

% --- Track which colors are used ---
color_used(C) :- color(V,C).

% --- Compute the number of distinct colors used ---
num_colors(N) :- N = #count { C : color_used(C) }.

% --- Optimization: minimize the number of distinct colors used ---
#minimize { 1,C : color_used(C) }.

% --- Output ---
#show color/2.
#show num_colors/1.