% Minimum-cost feedback vertex set problem

%%% DATA %%%

% Vertices
vertex(1..15).

% Removal costs
cost(1,10). cost(2,4). cost(3,5). cost(4,6).
cost(5,7). cost(6,9). cost(7,8).
cost(8,2). cost(9,4). cost(10,3).
cost(11,5). cost(12,7). cost(13,6).
cost(14,6). cost(15,12).

% Protected vertices (cannot be removed)
protected(1). protected(15).

% Vertex groups
group(2,a). group(3,a). group(4,a).
group(5,b). group(6,b). group(7,b).
group(8,c). group(9,c). group(10,c).
group(11,d). group(12,d). group(13,d).
group(14,e).

% Core edges (always part of graph structure)
edge_core(1,2). edge_core(1,5). edge_core(1,8).
edge_core(2,3). edge_core(3,4). edge_core(4,2).
edge_core(5,6). edge_core(6,7). edge_core(7,5).
edge_core(8,9). edge_core(9,10). edge_core(10,8).
edge_core(11,12). edge_core(12,13). edge_core(13,11).
edge_core(2,11). edge_core(4,14). edge_core(7,14). edge_core(10,15).
edge_core(14,1).

% Conditional edges (exist only if source vertex is not removed)
edge_cond(3,7). edge_cond(3,11).
edge_cond(6,10). edge_cond(6,13).
edge_cond(9,13). edge_cond(9,14).
edge_cond(12,4). edge_cond(12,7).

%%% DECISION VARIABLES %%%

% Choose which vertices to remove (cannot remove protected vertices)
{ remove(V) } :- vertex(V), not protected(V).

%%% CONSTRAINTS %%%

% Protected vertices cannot be removed
:- protected(V), remove(V).

% At most one vertex per group can be removed
:- group(V1,G), group(V2,G), V1 != V2, remove(V1), remove(V2).

%%% DERIVED FACTS %%%

% Vertices that remain
remain(V) :- vertex(V), not remove(V).

% Edges that exist in the remaining graph:
% Core edges exist if source remains
edge_exists(U,V) :- edge_core(U,V), remain(U).
% Conditional edges exist if source remains
edge_exists(U,V) :- edge_cond(U,V), remain(U).

% Edges where both endpoints remain (these can form cycles)
edge_remaining(U,V) :- edge_exists(U,V), remain(V).

%%% ACYCLICITY CHECK %%%
% Compute reachability in the remaining graph
reachable(U,V) :- edge_remaining(U,V).
reachable(U,V) :- edge_remaining(U,W), reachable(W,V).

% No vertex can reach itself (no cycles)
:- reachable(V,V).

%%% OBJECTIVE %%%

% Total cost of removed vertices
total_cost(C) :- C = #sum { Cost,V : remove(V), cost(V,Cost) }.

% Minimize total removal cost
#minimize { C,V : remove(V), cost(V,C) }.

%%% OUTPUT %%%
#show remove/1.
#show total_cost/1.