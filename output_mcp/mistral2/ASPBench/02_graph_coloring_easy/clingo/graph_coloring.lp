% Define the vertices
vertex(1..6).

% Define the edges
edge(1,2). edge(1,3).
edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Define the colors (will be chosen by the solver)
color(1..6). % Allow up to 6 colors (can be reduced by optimization)

% Assign colors to vertices
{ colored(V, C) : color(C) } = 1 :- vertex(V).

% Ensure no two adjacent vertices have the same color
:- edge(V1, V2), colored(V1, C), colored(V2, C).

% Define the set of used colors
used_color(C) :- colored(_, C).

% Calculate the number of colors used
num_colors(N) :- N = #count{ C : used_color(C) }.

% Minimize the number of colors used
#minimize{ N : num_colors(N) }.

% Show the coloring and the number of colors
#show colored/2.
#show num_colors/1.