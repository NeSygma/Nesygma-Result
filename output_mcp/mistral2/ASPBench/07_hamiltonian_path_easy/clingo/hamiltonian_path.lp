% Declare vertices and edges
vertex(0..5).
edge(0,1). edge(0,2).
edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Positions in the path
position(0..5).

% Generate a path: assign a vertex to each position
1 { path(V, T) : vertex(V) } 1 :- position(T).

% Start at vertex 0 and end at vertex 5
:- not path(0, 0).
:- not path(5, 5).

% Ensure each vertex appears exactly once
:- vertex(V), 2 { path(V, T) : position(T) }.

% Follow directed edges: if V is at T and W is at T+1, then edge(V,W) must exist
:- path(V, T), path(W, T+1), T < 5, not edge(V, W).

% Ensure all vertices are visited (implicitly enforced by the "exactly once" constraint above)

% Collect all Hamiltonian paths
hamiltonian_path(T, V) :- path(V, T).

% Show the paths
#show hamiltonian_path/2.