% --- Data ---
vertex(0..11).
level(0, 2). level(1, 2). level(2, 1). level(3, 1). level(4, 1). level(5, 1).
level(6, 0). level(7, 0). level(8, 0). level(9, 0). level(10, 0). level(11, 0).
cost(0, 10). cost(1, 10). cost(2, 8). cost(3, 5). cost(4, 7). cost(5, 6).
cost(6, 2). cost(7, 2). cost(8, 3). cost(9, 3). cost(10, 4). cost(11, 4).

edge(0, 2, 5, fiber). edge(1, 3, 4, fiber). edge(2, 3, 3, fiber). edge(2, 4, 6, copper).
edge(2, 6, 2, copper). edge(3, 5, 2, fiber). edge(3, 7, 8, copper). edge(4, 8, 5, fiber).
edge(5, 9, 4, copper). edge(5, 10, 3, fiber). edge(6, 7, 1, copper). edge(9, 10, 7, fiber).
edge(10, 11, 2, copper).

terminal(6). terminal(7). terminal(10). terminal(11).
group(a, 6). group(a, 7). group(b, 10). group(b, 11).

% --- Choice ---
{ in_tree_edge(U, V, W, T) } :- edge(U, V, W, T).
{ in_tree_edge(V, U, W, T) } :- edge(U, V, W, T).

% --- Derived ---
in_tree_node(U) :- in_tree_edge(U, _, _, _).
in_tree_node(V) :- in_tree_edge(_, V, _, _).
steiner(V) :- in_tree_node(V), not terminal(V).

% --- Constraints ---
% 1. All terminals must be in the tree
:- terminal(V), not in_tree_node(V).

% 2. Connectedness (using reachability from a fixed terminal)
reachable(6).
reachable(V) :- reachable(U), in_tree_edge(U, V, _, _).
:- terminal(V), not reachable(V).
:- in_tree_node(V), not reachable(V).

% 3. Tree structure (Acyclic: edges = nodes - 1)
num_nodes(N) :- N = #count { V : in_tree_node(V) }.
num_edges(E) :- E = #count { U, V : in_tree_edge(U, V, _, _) }.
:- num_nodes(N), num_edges(E), E != N - 1.

% 4. Hierarchy: Steiner vertex at level L cannot connect to a vertex at level > L
:- steiner(U), level(U, LU), in_tree_edge(U, V, _, _), level(V, LV), LU < LV.

% 5. Resource Budget (Steiner vertices)
steiner_cost(C) :- C = #sum { Cost, V : steiner(V), cost(V, Cost) }.
:- steiner_cost(C), C > 20.

% 6. Copper Edge Limit
copper_count(C) :- C = #count { U, V : in_tree_edge(U, V, _, copper) }.
:- copper_count(C), C > 3.

% 7. Gateway Requirement
gateway(V, a) :- steiner(V), in_tree_edge(V, T, _, _), group(a, T).
gateway(V, b) :- steiner(V), in_tree_edge(V, T, _, _), group(b, T).
:- not 1 { gateway(_, a) }.
:- not 1 { gateway(_, b) }.

% 8. Gateway Connectivity (via Steiner vertices)
gateway_node(V) :- gateway(V, _).
reachable_gateway(V) :- gateway(V, a).
reachable_gateway(V) :- reachable_gateway(U), in_tree_edge(U, V, _, _), steiner(V).
:- gateway(V, b), not reachable_gateway(V).

% --- Objective ---
total_weight(W) :- W = #sum { Weight, U, V : in_tree_edge(U, V, Weight, _) }.
#minimize { W : total_weight(W) }.

#show total_weight/1.
#show in_tree_edge/4.
#show steiner/1.
#show gateway/2.