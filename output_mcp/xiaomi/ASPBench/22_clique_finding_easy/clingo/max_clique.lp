% ============ Domain ============
vertex(0..6).

% ============ Edge Data (undirected, stored as U < V) ============
edge(0,1). edge(0,2). edge(0,3).
edge(1,2). edge(1,3). edge(1,4).
edge(2,3). edge(2,5).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Make edge symmetric for lookup
edge(U,V) :- edge(V,U), vertex(U), vertex(V).

% ============ Choice: Select vertices for the clique ============
{ in_clique(V) } :- vertex(V).

% ============ Constraint: Every pair in clique must be connected ============
:- in_clique(U), in_clique(V), U != V, not edge(U,V).

% ============ Derived: Clique edges ============
clique_edge(U,V) :- in_clique(U), in_clique(V), U < V, edge(U,V).

% ============ Compute clique size ============
clique_size(N) :- N = #count{V : in_clique(V)}.

% ============ Optimization: Maximize clique size ============
#maximize { N : clique_size(N) }.

% ============ Output ============
#show in_clique/1.
#show clique_size/1.
#show clique_edge/2.