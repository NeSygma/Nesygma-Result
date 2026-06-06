% vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7). vertex(8). vertex(9). vertex(10). vertex(11). vertex(12). vertex(13). vertex(14). vertex(15).

% protected vertices
protected(1). protected(15).

% costs
cost(1,10). cost(2,4). cost(3,5). cost(4,6). cost(5,7). cost(6,9). cost(7,8). cost(8,2). cost(9,4). cost(10,3). cost(11,5). cost(12,7). cost(13,6). cost(14,6). cost(15,12).

% groups
group(a). group_member(2,a). group_member(3,a). group_member(4,a).
group(b). group_member(5,b). group_member(6,b). group_member(7,b).
group(c). group_member(8,c). group_member(9,c). group_member(10,c).
group(d). group_member(11,d). group_member(12,d). group_member(13,d).
group(e). group_member(14,e).

% core edges
core_edge(1,2). core_edge(1,5). core_edge(1,8).
core_edge(2,3). core_edge(3,4). core_edge(4,2).
core_edge(5,6). core_edge(6,7). core_edge(7,5).
core_edge(8,9). core_edge(9,10). core_edge(10,8).
core_edge(11,12). core_edge(12,13). core_edge(13,11).
core_edge(2,11). core_edge(4,14). core_edge(7,14). core_edge(10,15).
core_edge(14,1).

% conditional edges
cond_edge(3,7). cond_edge(3,11).
cond_edge(6,10). cond_edge(6,13).
cond_edge(9,13). cond_edge(9,14).
cond_edge(12,4). cond_edge(12,7).

% choice of removal
{ removed(V) } :- vertex(V), not protected(V).

% at most one per group
0 { removed(V) : group_member(V,G) } 1 :- group(G).

% remaining vertices
remaining(V) :- vertex(V), not removed(V).

% edges in remaining graph
edge(U,V) :- core_edge(U,V), remaining(U), remaining(V).
edge(U,V) :- cond_edge(U,V), remaining(U), remaining(V).

% reachability
reachable(U,V) :- edge(U,V).
reachable(U,W) :- edge(U,V), reachable(V,W).

% no cycles
:- reachable(V,V).

% minimize cost
#minimize { C@1 : removed(V), cost(V,C) }.

% total cost
total_cost(C) :- C = #sum{C1 : removed(V), cost(V,C1)}.

% show
#show removed/1.
#show cost/2.
#show total_cost/1.
#show remaining/1.