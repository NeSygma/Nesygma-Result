% Vertices
vertex(0..5).

% Directed edges
edge(0,1). edge(0,2). edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4). edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Start and end vertices
start(0).
end(5).

% Time steps: 0 to 5 (6 vertices, so 6 positions)
time(0..5).

% Choose which vertex is at each time step
1 { at(V, T) : vertex(V) } 1 :- time(T).

% Each vertex appears exactly once
1 { at(V, T) : time(T) } 1 :- vertex(V).

% Start vertex must be at time 0
:- start(S), not at(S, 0).

% End vertex must be at time 5
:- end(E), not at(E, 5).

% Consecutive vertices must have a directed edge
:- at(V1, T), at(V2, T+1), not edge(V1, V2), time(T), T < 5.

% Display the path as a sequence
path(T, V) :- at(V, T).

#show path/2.