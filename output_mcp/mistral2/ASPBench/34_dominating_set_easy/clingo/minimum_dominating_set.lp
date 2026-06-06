% Define the graph
vertex(1..7).

edge(1,2). edge(1,3).
edge(2,1). edge(2,3). edge(2,4).
edge(3,1). edge(3,2). edge(3,5).
edge(4,2). edge(4,6).
edge(5,3). edge(5,6). edge(5,7).
edge(6,4). edge(6,5). edge(6,7).
edge(7,5). edge(7,6).

% Choice rule: select a subset of vertices as the dominating set
{ in_set(V) : vertex(V) }.

% Constraint 1: Every vertex is either in the set or adjacent to a vertex in the set
dominated(V) :- in_set(V).
dominated(V) :- edge(V, U), in_set(U).
:- vertex(V), not dominated(V).

% Constraint 2: No vertex appears more than once (implicit in the choice rule)

% Objective: Minimize the size of the dominating set
#minimize { 1@1 : in_set(V) }.

% Show the dominating set and its size
#show in_set/1.
size(N) :- N = #count{ V : in_set(V) }.
#show size/1.