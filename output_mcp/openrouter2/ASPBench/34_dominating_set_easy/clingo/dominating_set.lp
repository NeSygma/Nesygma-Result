% Define vertices
vertex(1..7).

% Define adjacency (directed edges as given)
adj(1,2). adj(1,3).
adj(2,1). adj(2,3). adj(2,4).
adj(3,1). adj(3,2). adj(3,5).
adj(4,2). adj(4,6).
adj(5,3). adj(5,6). adj(5,7).
adj(6,4). adj(6,5). adj(6,7).
adj(7,5). adj(7,6).

% Choice rule: each vertex may be in the dominating set or not
{dominating_set(V)} :- vertex(V).

% A vertex is dominated if it is in the set or has a neighbor in the set
neighbor_in_set(V) :- adj(V,U), dominating_set(U).

% Constraint: every vertex must be dominated
:- vertex(V), not dominating_set(V), not neighbor_in_set(V).

% Objective: minimize the size of the dominating set
#minimize {1@1, V : dominating_set(V)}.

% Compute size
size(S) :- S = #count{V : dominating_set(V)}.

#show dominating_set/1.
#show size/1.