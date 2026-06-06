% Define the graph
vertex(1..6).
edge(1,2). edge(1,3).
edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Define color domain (colors will be 1, 2, 3, ...)
color_domain(1..6).

% Assign exactly one color to each vertex
{color(V, C) : color_domain(C)} = 1 :- vertex(V).

% No two adjacent vertices can have the same color
:- edge(V1, V2), color(V1, C), color(V2, C).

% Compute chromatic number as the maximum color used
chromatic_number(N) :- N = #max {C : color(V, C)}.

% Minimize the chromatic number
#minimize {N : chromatic_number(N)}.

% Show the coloring and chromatic number
#show color/2.
#show chromatic_number/1.