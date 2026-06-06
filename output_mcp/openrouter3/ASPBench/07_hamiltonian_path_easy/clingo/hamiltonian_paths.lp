% Hamiltonian Paths from 0 to 5 in a directed graph

% Define vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5).

% Define directed edges
edge(0,1). edge(0,2). edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4). edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Define start and end vertices
start(0). end(5).

% Define positions in the path (1 to 6 for 6 vertices)
position(1..6).

% Choice rule: select which vertex appears at each position
{ at_position(V, P) : vertex(V) } 1 :- position(P).

% Each vertex appears exactly once in the path
1 { at_position(V, P) : position(P) } 1 :- vertex(V).

% Path must start at vertex 0
at_position(0, 1).

% Path must end at vertex 5
at_position(5, 6).

% Consecutive vertices in the path must have a directed edge
:- at_position(V1, P), at_position(V2, P+1), not edge(V1, V2).

% Helper predicate to extract the path as a sequence
path_sequence(P) :- at_position(V, P).

% Count the number of valid paths
count(N) :- N = #count { V2,V3,V4,V5 : 
    at_position(0,1), at_position(V2,2), at_position(V3,3), 
    at_position(V4,4), at_position(V5,5), at_position(5,6) }.

% Check if at least one path exists
exists(true) :- count(N), N > 0.
exists(false) :- count(N), N = 0.

% Show the actual paths - use a helper predicate to avoid unsafe variables
path(V1,V2,V3,V4,V5,V6) :- at_position(0,1), at_position(V2,2), at_position(V3,3), 
    at_position(V4,4), at_position(V5,5), at_position(5,6).

#show path/6.
#show count/1.
#show exists/1.