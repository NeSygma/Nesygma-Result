% ============ DOMAIN ============
vertex(0..11).

% ============ VERTEX LEVELS ============
level(0, 2). level(1, 2).
level(2, 1). level(3, 1). level(4, 1). level(5, 1).
level(6, 0). level(7, 0). level(8, 0). level(9, 0). level(10, 0). level(11, 0).

% ============ RESOURCE COSTS ============
cost(0, 10). cost(1, 10). cost(2, 8). cost(3, 5). cost(4, 7). cost(5, 6).
cost(6, 2). cost(7, 2). cost(8, 3). cost(9, 3). cost(10, 4). cost(11, 4).

% ============ EDGES (undirected, canonical V1 < V2) ============
uedge(0, 2, 5, fiber).
uedge(1, 3, 4, fiber).
uedge(2, 3, 3, fiber).
uedge(2, 4, 6, copper).
uedge(2, 6, 2, copper).
uedge(3, 5, 2, fiber).
uedge(3, 7, 8, copper).
uedge(4, 8, 5, fiber).
uedge(5, 9, 4, copper).
uedge(5, 10, 3, fiber).
uedge(6, 7, 1, copper).
uedge(9, 10, 7, fiber).
uedge(10, 11, 2, copper).

% Both directions for traversal
edge(V1, V2, W, T) :- uedge(V1, V2, W, T).
edge(V2, V1, W, T) :- uedge(V1, V2, W, T).

% ============ TERMINAL GROUPS ============
terminal(6, a). terminal(7, a).
terminal(10, b). terminal(11, b).

% ============ NON-TERMINAL IDENTIFICATION ============
non_terminal(V) :- vertex(V), not terminal(V, _).

% ============ CHOICE: SELECT STEINER VERTICES ============
{steiner(V)} :- non_terminal(V).

% ============ VERTICES IN TREE ============
in_tree(V) :- terminal(V, _).
in_tree(V) :- steiner(V).

% ============ CHOICE: SELECT TREE EDGES (canonical V1 < V2) ============
{tree_edge(V1, V2)} :- uedge(V1, V2, _, _), in_tree(V1), in_tree(V2).

% Both directions for reachability
tree_edge_dir(V1, V2) :- tree_edge(V1, V2).
tree_edge_dir(V2, V1) :- tree_edge(V1, V2).

% ============ CONSTRAINT 1: TREE STRUCTURE (connected + acyclic) ============
% Connectivity via reachability from a chosen root
{root(V)} :- in_tree(V).
1 {root(V) : in_tree(V)} 1.

reachable(V) :- root(V), in_tree(V).
reachable(V2) :- reachable(V1), tree_edge_dir(V1, V2), in_tree(V2).

% All vertices in tree must be reachable from root
:- in_tree(V), not reachable(V).

% Acyclicity: edges = vertices - 1
tree_size(N) :- N = #count{V : in_tree(V)}.
tree_edge_count(M) :- M = #count{V1, V2 : tree_edge(V1, V2)}.
:- tree_size(N), tree_edge_count(M), M != N - 1.

% ============ CONSTRAINT 2: HIERARCHY ============
% Steiner vertex at level L cannot connect to vertex at level > L
:- tree_edge(V1, V2), steiner(V1), level(V1, L1), level(V2, L2), L2 > L1.
:- tree_edge(V1, V2), steiner(V2), level(V2, L2), level(V1, L1), L1 > L2.

% ============ CONSTRAINT 3: RESOURCE BUDGET (<= 20) ============
total_steiner_cost(S) :- S = #sum{C, V : steiner(V), cost(V, C)}.
:- total_steiner_cost(S), S > 20.

% ============ CONSTRAINT 4: COPPER EDGE LIMIT (<= 3) ============
copper_count(N) :- N = #count{V1, V2 : tree_edge(V1, V2), uedge(V1, V2, _, copper)}.
:- copper_count(N), N > 3.

% ============ CONSTRAINT 5: GATEWAY REQUIREMENT ============
% For each terminal group, at least one Steiner vertex connects directly to a terminal
gateway(V, G) :- steiner(V), terminal(T, G), tree_edge_dir(V, T).
has_gateway(G) :- gateway(V, G).
:- terminal(_, G), not has_gateway(G).

% ============ CONSTRAINT 6: GATEWAY CONNECTIVITY ============
% All gateways connected through path using only Steiner vertices
is_gateway(V) :- gateway(V, _).

% Steiner-only subgraph edges (tree edges with both endpoints Steiner)
steiner_edge(V1, V2) :- tree_edge(V1, V2), steiner(V1), steiner(V2).
steiner_edge_dir(V1, V2) :- steiner_edge(V1, V2).
steiner_edge_dir(V2, V1) :- steiner_edge(V1, V2).

% Pick a gateway root for connectivity check
{groot(V)} :- is_gateway(V).
1 {groot(V) : is_gateway(V)} 1.

% Reachability in Steiner subgraph
g_reachable(V) :- groot(V), is_gateway(V).
g_reachable(V2) :- g_reachable(V1), steiner_edge_dir(V1, V2), steiner(V2).

% All gateways must be reachable from groot
:- is_gateway(V), not g_reachable(V).

% ============ OBJECTIVE: MINIMIZE TOTAL EDGE WEIGHT ============
total_weight(W) :- W = #sum{Wt, V1, V2 : tree_edge(V1, V2), uedge(V1, V2, Wt, _)}.

#minimize{W@1 : total_weight(W)}.

% ============ OUTPUT ============
#show tree_edge/2.
#show steiner/1.
#show in_tree/1.
#show total_weight/1.
#show copper_count/1.
#show total_steiner_cost/1.
#show gateway/2.
#show tree_size/1.
#show tree_edge_count/1.