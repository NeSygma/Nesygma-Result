% Define the vertices
vertex(0..5).

% Define the directed edges
edge(0,1). edge(0,2).
edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Time steps (0 to 5 for 6 vertices)
time(0..5).

% Choice rule: select a vertex for each time step
{ path(T, V) : vertex(V) } 1 :- time(T).

% Ensure each vertex appears exactly once in the path
:- vertex(V), not 1 { path(T, V) : time(T) } 1.

% Path must start at vertex 0
:- path(0, V), V != 0.

% Path must end at vertex 5
:- path(5, V), V != 5.

% Consecutive vertices must be connected by a directed edge
:- path(T, V1), path(T+1, V2), not edge(V1, V2), time(T), T < 5.

% Show the paths
#show path/2.

% Define a path as a sequence of vertices for output
path_sequence(V0, V1, V2, V3, V4, V5) :-
    path(0, V0), path(1, V1), path(2, V2), path(3, V3), path(4, V4), path(5, V5),
    V0 = 0, V5 = 5.

#show path_sequence/6.

% Count the number of valid paths
path_count(N) :- N = #count{ V0, V1, V2, V3, V4, V5 : path_sequence(V0, V1, V2, V3, V4, V5) }.

% Indicate if at least one path exists
has_path :- path_count(_).

#show path_count/1.
#show has_path/0.