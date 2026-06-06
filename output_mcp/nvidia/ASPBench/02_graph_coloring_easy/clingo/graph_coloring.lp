% Define vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% Define possible colors (we will minimize their usage)
color(1). color(2). color(3). color(4). color(5). color(6).

% Edge list (undirected)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(2,3). edge(3,2).
edge(2,4). edge(4,2).
edge(3,4). edge(4,3).
edge(3,5). edge(5,3).
edge(4,5). edge(5,4).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).

% Each vertex must be assigned exactly one color
{ col(V, C) : color(C) } 1 :- vertex(V).

% Adjacent vertices cannot share the same color
:- col(U, C), col(V, C), edge(U, V).

% A color is used if some vertex is assigned that color
used_color(C) :- col(V, C).

% Minimize the total number of used colors
#minimize { C : used_color(C) }.

% Compute the total number of used colors (optional, for output)
num_colors(N) :- N = #count{ C : used_color(C) }.

% Show the coloring and the number of colors used
#show col/2.
#show num_colors/1.