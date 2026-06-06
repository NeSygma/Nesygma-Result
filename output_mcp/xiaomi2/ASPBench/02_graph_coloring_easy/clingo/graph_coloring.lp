% Graph Coloring Problem - Minimize Chromatic Number

% ============ Domain Facts ============
% Vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% Edges (undirected - stored as edge(X,Y) where X < Y)
edge(1,2). edge(1,3). edge(2,3). edge(2,4). edge(3,4). edge(3,5). edge(4,5). edge(4,6). edge(5,6).

% Symmetric edge relation
edge(X,Y) :- edge(Y,X).

% ============ Color Assignment ============
% Possible colors (upper bound - will be minimized)
color(1..6).

% Each vertex gets exactly one color
1 { colored(V, C) : color(C) } 1 :- vertex(V).

% ============ Constraints ============
% Adjacent vertices must have different colors
:- edge(V1, V2), colored(V1, C), colored(V2, C).

% ============ Optimization ============
% Minimize the number of colors used
#minimize { C : colored(_, C) }.

% ============ Output ============
% Show the coloring assignments
#show colored/2.

% Show the number of colors used
num_colors(N) :- N = #count { C : colored(_, C) }.
#show num_colors/1.