% Maximum Independent Set Problem

% 1. Declare vertices
vertex(1). vertex(2). vertex(3). vertex(4).
vertex(5). vertex(6). vertex(7). vertex(8).

% 2. Declare edges (undirected graph - store both directions)
edge(1, 2). edge(2, 1).
edge(1, 3). edge(3, 1).
edge(1, 4). edge(4, 1).
edge(2, 5). edge(5, 2).
edge(3, 6). edge(6, 3).
edge(3, 7). edge(7, 3).
edge(4, 8). edge(8, 4).
edge(5, 6). edge(6, 5).
edge(6, 7). edge(7, 6).
edge(7, 8). edge(8, 7).

% 3. Choice rule: select vertices for the independent set
% Each vertex can be either selected or not selected
{ selected(V) } :- vertex(V).

% 4. Constraint: No two selected vertices can be connected by an edge
% If V1 and V2 are connected by an edge, they cannot both be selected
:- selected(V1), selected(V2), edge(V1, V2), V1 != V2.

% 5. Compute the size of the independent set
size(N) :- N = #count{ V : selected(V) }.

% 6. Optimization: maximize the size of the independent set
#maximize { 1, V : selected(V) }.

% 7. Show the solution
#show selected/1.
#show size/1.