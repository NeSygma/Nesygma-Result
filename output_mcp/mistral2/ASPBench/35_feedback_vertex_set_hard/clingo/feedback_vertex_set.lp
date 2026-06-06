%% Domain and facts
vertex(1..15).

% Protected vertices
protected(1). protected(15).

% Vertex costs
cost(1,10). cost(2,4). cost(3,5). cost(4,6).
cost(5,7). cost(6,9). cost(7,8).
cost(8,2). cost(9,4). cost(10,3).
cost(11,5). cost(12,7). cost(13,6).
cost(14,6). cost(15,12).

% Group membership
group(a,2). group(a,3). group(a,4).
group(b,5). group(b,6). group(b,7).
group(c,8). group(c,9). group(c,10).
group(d,11). group(d,12). group(d,13).
group(e,14).

% Core edges (always present if source is not removed)
core_edge(1,2). core_edge(1,5). core_edge(1,8).
core_edge(2,3). core_edge(3,4). core_edge(4,2).
core_edge(5,6). core_edge(6,7). core_edge(7,5).
core_edge(8,9). core_edge(9,10). core_edge(10,8).
core_edge(11,12). core_edge(12,13). core_edge(13,11).
core_edge(2,11). core_edge(4,14). core_edge(7,14). core_edge(10,15).
core_edge(14,1).

% Conditional edges (present only if source and condition vertices are not removed)
conditional_edge(3,7,3). conditional_edge(3,11,3).
conditional_edge(6,10,6). conditional_edge(6,13,6).
conditional_edge(9,13,9). conditional_edge(9,14,9).
conditional_edge(12,4,12). conditional_edge(12,7,12).

% Choice rule for removal
{removed(V) : vertex(V)}.

% Enforce non-removal of protected vertices
:- protected(V), removed(V).

% Group constraint: at most one vertex removed per group
:- group(G,V1), group(G,V2), V1 < V2, removed(V1), removed(V2).

% Edge existence in the remaining graph
edge(U,V) :- core_edge(U,V), not removed(U).
edge(U,V) :- conditional_edge(U,V,C), not removed(U), not removed(C).

% Reachability for acyclicity
reachable(X,Y) :- edge(X,Y).
reachable(X,Z) :- reachable(X,Y), reachable(Y,Z).

% Acyclicity constraint
:- reachable(V,V).

% Total removal cost
removal_cost(C) :- C = #sum{ Cost : removed(V), cost(V,Cost) }.

% Show the feedback set and total cost
#show removed/1.
#show total_cost(C) :- removal_cost(C).