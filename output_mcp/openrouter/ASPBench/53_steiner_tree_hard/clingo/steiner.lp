% Vertex levels
level(0,2). level(1,2). level(2,1). level(3,1). level(4,1). level(5,1). level(6,0). level(7,0). level(8,0). level(9,0). level(10,0). level(11,0).
% Vertex resource costs
cost(0,10). cost(1,10). cost(2,8). cost(3,5). cost(4,7). cost(5,6). cost(6,2). cost(7,2). cost(8,3). cost(9,3). cost(10,4). cost(11,4).
% Terminals groups
terminal(6). terminal(7). terminal(10). terminal(11).
% group membership
groupA(6). groupA(7).
groupB(10). groupB(11).
% Edges (undirected)
edge(0,2,5,"fiber"). edge(1,3,4,"fiber"). edge(2,3,3,"fiber"). edge(2,4,6,"copper"). edge(2,6,2,"copper"). edge(3,5,2,"fiber"). edge(3,7,8,"copper"). edge(4,8,5,"fiber"). edge(5,9,4,"copper"). edge(5,10,3,"fiber"). edge(6,7,1,"copper"). edge(9,10,7,"fiber"). edge(10,11,2,"copper").
% make edges symmetric for convenience
edge(V,U,W,T) :- edge(U,V,W,T).
% Choice of edges in the tree (undirected)
{selected_edge(U,V) : edge(U,V,_,_)}.
% Selected vertices: terminals always selected, steiner if incident to a selected edge
selected_vertex(V) :- terminal(V).
selected_vertex(V) :- selected_edge(V,_).
selected_vertex(V) :- selected_edge(_,V).
% Define steiner vertices
steiner(V) :- selected_vertex(V), not terminal(V).
% Ensure edges only between selected vertices
:- selected_edge(U,V), not selected_vertex(U).
:- selected_edge(U,V), not selected_vertex(V).
% Hierarchy constraint: a steiner at level L cannot connect to a vertex with higher level (>L)
:- selected_edge(U,V), steiner(U), level(U,Lu), level(V,Lv), Lv > Lu.
:- selected_edge(U,V), steiner(V), level(V,Lu), level(U,Lv), Lv > Lu.
% Resource budget for steiner vertices
steiner_cost_sum(S) :- S = #sum {C,V : steiner(V), cost(V,C)}.
:- steiner_cost_sum(S), S > 20.
% Copper edge limit
copper_edge_count(Cnt) :- Cnt = #count {U,V : selected_edge(U,V), edge(U,V,_,"copper")}.
:- copper_edge_count(Cnt), Cnt > 3.
% Connectivity: pick root terminal 6 (any terminal works)
reach(6).
reach(V) :- reach(U), selected_edge(U,V).
% All selected vertices must be reachable
:- selected_vertex(V), not reach(V).
% Acyclicity: number of edges = number of vertices - 1
n_edges(N) :- N = #count {U,V : selected_edge(U,V)}.
n_verts(M) :- M = #count {V : selected_vertex(V)}.
:- n_edges(N), n_verts(M), N != M-1.
% Gateways: steiner adjacent to a terminal of each group
gatewayA(V) :- steiner(V), selected_edge(V,T), groupA(T).
gatewayB(V) :- steiner(V), selected_edge(V,T), groupB(T).
% At least one gateway per group
gatewayA_exists :- gatewayA(_).
gatewayB_exists :- gatewayB(_).
:- not gatewayA_exists.
:- not gatewayB_exists.
% Steiner subgraph connectivity (gateways must be connected via steiner-only edges)
steiner_edge(U,V) :- selected_edge(U,V), steiner(U), steiner(V).
% Choose at most one steiner root (optional)
0 { steiner_root(R) : steiner(R) } 1.
steiner_root_exists :- steiner_root(_).
% Reachability among steiner vertices via steiner edges
steiner_reach(R) :- steiner_root(R).
steiner_reach(V) :- steiner_reach(U), steiner_edge(U,V).
% All steiner vertices must be reachable if a root exists
:- steiner(V), steiner_root_exists, not steiner_reach(V).
% Total weight of selected edges
total_weight(W) :- W = #sum {Weight,U,V : selected_edge(U,V), edge(U,V,Weight,_)}.
% Copper count for output
copper_used(C) :- C = #count {U,V : selected_edge(U,V), edge(U,V,_,"copper")}.
% Steiner cost total for output
steiner_cost_total(S) :- S = #sum {C,V : steiner(V), cost(V,C)}.
% Show results
#show selected_edge/2.
#show steiner/1.
#show total_weight/1.
#show copper_used/1.
#show steiner_cost_total/1.
#show gatewayA/1.
#show gatewayB/1.