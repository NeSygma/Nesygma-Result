% --- Declare the graph ---
vertex(1..6).
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% --- Choice rule for vertex removal ---
{ removed(V) : vertex(V) }.

% --- Edge removal: if U or V is removed, edge(U,V) is removed ---
edge_remaining(U,V) :- edge(U,V), not removed(U), not removed(V).

% --- Reachability: transitive closure of remaining edges ---
reachable(U,V) :- edge_remaining(U,V).
reachable(U,V) :- reachable(U,W), reachable(W,V).

% --- Check for cycles: no vertex is reachable from itself ---
:- vertex(V), reachable(V,V).

% --- Minimize the number of removed vertices ---
#minimize { V : removed(V) }.

% --- Show the solution ---
#show removed/1.