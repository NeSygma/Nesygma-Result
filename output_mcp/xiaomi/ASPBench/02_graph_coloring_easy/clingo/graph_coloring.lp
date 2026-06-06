% ==============================
% Graph Coloring Problem
% Minimize number of colors used
% ==============================

% --- Domain: Vertices ---
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% --- Domain: Edges (undirected, stored both ways) ---
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(2,3). edge(3,2).
edge(2,4). edge(4,2).
edge(3,4). edge(4,3).
edge(3,5). edge(5,3).
edge(4,5). edge(5,4).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).

% --- Domain: Colors (upper bound = number of vertices) ---
% We allow up to 6 colors; the optimizer will minimize usage
color(1). color(2). color(3). color(4). color(5). color(6).

% --- Choice Rule: Assign exactly one color to each vertex ---
1 { colored(V, C) : color(C) } 1 :- vertex(V).

% --- Constraint: Adjacent vertices must have different colors ---
:- edge(V1, V2), colored(V1, C), colored(V2, C).

% --- Derived: Which colors are actually used ---
used_color(C) :- colored(_, C).

% --- Derived: Total number of colors used ---
num_colors(N) :- N = #count { C : used_color(C) }.

% --- Optimization: Minimize the number of colors used ---
#minimize { 1, C : used_color(C) }.

% --- Output ---
#show colored/2.
#show num_colors/1.