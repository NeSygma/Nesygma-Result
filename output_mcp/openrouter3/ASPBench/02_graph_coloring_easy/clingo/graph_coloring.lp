% Graph Coloring Problem
% Find minimum number of colors for a graph

% Domain: Vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% Edges (undirected graph)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(2,3). edge(3,2).
edge(2,4). edge(4,2).
edge(3,4). edge(4,3).
edge(3,5). edge(5,3).
edge(4,5). edge(5,4).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).

% Maximum possible colors (upper bound)
max_color(6).

% Choice rule: Assign a color to each vertex
% We don't know the number of colors in advance, so we allow colors 1-6
{color(V, C) : C = 1..6} 1 :- vertex(V).

% Constraint: Each vertex gets exactly one color
% (Already enforced by the choice rule with cardinality 1)

% Constraint: Adjacent vertices must have different colors
:- edge(V1, V2), color(V1, C), color(V2, C).

% Helper: Determine which colors are actually used
used_color(C) :- color(_, C).

% Count the number of colors used
num_colors(N) :- N = #count { C : used_color(C) }.

% Optimization: Minimize the number of colors used
#minimize { N : num_colors(N) }.

% Show the solution
#show color/2.
#show num_colors/1.