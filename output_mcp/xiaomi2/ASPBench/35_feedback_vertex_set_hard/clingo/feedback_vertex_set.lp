% Vertices
vertex(1..15).

% Costs
cost(1,10). cost(2,4). cost(3,5). cost(4,6). cost(5,7). cost(6,9). cost(7,8).
cost(8,2). cost(9,4). cost(10,3). cost(11,5). cost(12,7). cost(13,6). cost(14,6). cost(15,12).

% Protected vertices
protected(1). protected(15).

% Groups
group(a,2). group(a,3). group(a,4).
group(b,5). group(b,6). group(b,7).
group(c,8). group(c,9). group(c,10).
group(d,11). group(d,12). group(d,13).
group(e,14).

% Core edges
core_edge(1,2). core_edge(1,5). core_edge(1,8).
core_edge(2,3). core_edge(3,4). core_edge(4,2).
core_edge(5,6). core_edge(6,7). core_edge(7,5).
core_edge(8,9). core_edge(9,10). core_edge(10,8).
core_edge(11,12). core_edge(12,13). core_edge(13,11).
core_edge(2,11). core_edge(4,14). core_edge(7,14). core_edge(10,15).
core_edge(14,1).

% Conditional edges
conditional_edge(3,7). conditional_edge(3,11).
conditional_edge(6,10). conditional_edge(6,13).
conditional_edge(9,13). conditional_edge(9,14).
conditional_edge(12,4). conditional_edge(12,7).

% Decision: remove a vertex (only non-protected)
{ remove(V) } :- vertex(V), not protected(V).

% Group constraint: at most one vertex per group can be removed
:- remove(V1), remove(V2), group(G, V1), group(G, V2), V1 != V2.

% Present edges after removal
present_edge(U,V) :- core_edge(U,V), not remove(U).
present_edge(U,V) :- conditional_edge(U,V), not remove(U).

% Assign a topological order to remaining vertices (1..15)
{ order(V, N) } :- vertex(V), not remove(V), N = 1..15.

% Each remaining vertex gets exactly one order
1 { order(V, N) : N = 1..15 } 1 :- vertex(V), not remove(V).

% Orders must be distinct
:- order(V1, N), order(V2, N), V1 != V2.

% Acyclicity: for every present edge, order(u) < order(v)
:- present_edge(U,V), order(U, N1), order(V, N2), N1 >= N2.

% Minimize total removal cost
#minimize { C, V : remove(V), cost(V, C) }.

% Output predicates
feedback_set(V) :- remove(V).
costs(V, C) :- remove(V), cost(V, C).
total_cost(S) :- S = #sum { C, V : remove(V), cost(V, C) }.
remaining_vertices(V) :- vertex(V), not remove(V).

#show feedback_set/1.
#show costs/2.
#show total_cost/1.
#show remaining_vertices/1.