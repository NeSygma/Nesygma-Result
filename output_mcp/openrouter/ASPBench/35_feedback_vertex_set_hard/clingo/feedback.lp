% Vertices
vertex(1..15).

% Costs
vertex_cost(1,10). vertex_cost(2,4). vertex_cost(3,5). vertex_cost(4,6).
vertex_cost(5,7). vertex_cost(6,9). vertex_cost(7,8).
vertex_cost(8,2). vertex_cost(9,4). vertex_cost(10,3).
vertex_cost(11,5). vertex_cost(12,7). vertex_cost(13,6).
vertex_cost(14,6). vertex_cost(15,12).

% Protected vertices (cannot be removed)
protected(1). protected(15).

% Choice: which vertices to remove (except protected)
{ remove(V) } :- vertex(V), not protected(V).
% Ensure protected not removed
:- remove(P), protected(P).

% Groups (at most one removed per group)
group(a). group(b). group(c). group(d). group(e).
in_group(2,a). in_group(3,a). in_group(4,a).
in_group(5,b). in_group(6,b). in_group(7,b).
in_group(8,c). in_group(9,c). in_group(10,c).
in_group(11,d). in_group(12,d). in_group(13,d).
in_group(14,e).
% Group constraint
:- group(G), #count{ V : remove(V), in_group(V,G) } > 1.

% Core edges (always present) - only if both endpoints not removed
edge_core(1,2). edge_core(1,5). edge_core(1,8).
edge_core(2,3). edge_core(3,4). edge_core(4,2).
edge_core(5,6). edge_core(6,7). edge_core(7,5).
edge_core(8,9). edge_core(9,10). edge_core(10,8).
edge_core(11,12). edge_core(12,13). edge_core(13,11).
edge_core(2,11). edge_core(4,14). edge_core(7,14). edge_core(10,15).
edge_core(14,1).

% Conditional edges (present only if source not removed and target not removed)
cond_edge(3,7). cond_edge(3,11).
cond_edge(6,10). cond_edge(6,13).
cond_edge(9,13). cond_edge(9,14).
cond_edge(12,4). cond_edge(12,7).

% Define effective edges (only if both vertices remain)
edge(U,V) :- edge_core(U,V), not remove(U), not remove(V).
edge(U,V) :- cond_edge(U,V), not remove(U), not remove(V).

% Reachability for cycle detection
reach(X,Y) :- edge(X,Y).
reach(X,Y) :- edge(X,Z), reach(Z,Y).
% No vertex may reach itself (no cycles)
:- reach(V,V).

% Remaining vertices
remaining(V) :- vertex(V), not remove(V).

% Total cost
total_cost(C) :- C = #sum{Cost,V : remove(V), vertex_cost(V,Cost)}.

% Optimization: minimize total cost, then number of removals, then sum of IDs
#minimize { Cost,V : remove(V), vertex_cost(V,Cost) }.
#minimize { 1,V : remove(V) }.
#minimize { V,V : remove(V) }.

#show remove/1.
#show total_cost/1.
#show remaining/1.