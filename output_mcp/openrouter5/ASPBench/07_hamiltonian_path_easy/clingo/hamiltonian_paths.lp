% --- Graph Definition ---
vertex(0..5).

% Directed edges
edge(0,1). edge(0,2).
edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Start and end vertices
start(0).
end(5).

% --- Hamiltonian Path Modeling ---
% Each vertex (except start) has exactly one incoming edge in the path
% Each vertex (except end) has exactly one outgoing edge in the path

% Choice: for each vertex (except end), select exactly one outgoing edge to be in the path
{ path_edge(V, U) : edge(V, U) } 1 :- vertex(V), not end(V).

% Choice: for each vertex (except start), select exactly one incoming edge to be in the path
{ path_edge(V, U) : edge(V, U) } 1 :- vertex(U), not start(U).

% --- Constraints ---

% No vertex can have both incoming and outgoing edges that are not consistent
% (already handled by the choice rules above)

% Prevent cycles: ensure the path forms a single chain from start to end
% Use reachability: start can reach all vertices via path edges
reachable(Start) :- start(Start).
reachable(U) :- reachable(V), path_edge(V, U).

% Every vertex must be reachable from start
:- vertex(V), not reachable(V).

% --- Output ---
% Define the path order: start at vertex 0, then follow path edges
% We'll use a step numbering to order the path
step(0..5).

% Position of each vertex in the path
1 { pos(V, S) : step(S) } 1 :- vertex(V).
1 { pos(V, S) : vertex(V) } 1 :- step(S).

% Start at position 0
pos(Start, 0) :- start(Start).

% End at position 5
pos(End, 5) :- end(End).

% If there's a path edge from V to U, then U's position is V's position + 1
:- path_edge(V, U), pos(V, S1), pos(U, S2), S2 != S1 + 1.

% --- Show the path ---
% Show path edges
#show path_edge/2.
% Show the sequence
#show pos/2.