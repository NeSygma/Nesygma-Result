% Graph vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% Directed edges
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% Choice: select vertices to remove
{remove(V) : vertex(V)}.

% A vertex is kept if it's not removed
kept(V) :- vertex(V), not remove(V).

% An edge exists in the remaining graph if both endpoints are kept
remaining_edge(X,Y) :- edge(X,Y), kept(X), kept(Y).

% Define reachability in the remaining graph
% Base: direct edges
reachable(X,Y) :- remaining_edge(X,Y).
% Transitive closure
reachable(X,Z) :- reachable(X,Y), remaining_edge(Y,Z).

% No cycles allowed: a vertex cannot reach itself
:- reachable(V,V), kept(V).

% Minimize the number of removed vertices
#minimize {1,V : remove(V)}.

% Show the removed vertices
#show remove/1.