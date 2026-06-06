% Maximum Independent Set with Constraints

% Vertices
vertex(1..24).

% Zones
zone(V,1) :- V >= 1, V <= 8.
zone(V,2) :- V >= 9, V <= 16.
zone(V,3) :- V >= 17, V <= 24.

% Types
type(1, core). type(9, core). type(17, core).
type(2, support). type(3, support). type(10, support). type(11, support). type(18, support). type(19, support).
type(4, peripheral). type(5, peripheral). type(6, peripheral). type(7, peripheral). type(8, peripheral).
type(12, peripheral). type(13, peripheral). type(14, peripheral). type(15, peripheral). type(16, peripheral).
type(20, peripheral). type(21, peripheral). type(22, peripheral). type(23, peripheral). type(24, peripheral).

% Edges (undirected)
edge(1,2). edge(1,4). edge(1,10). edge(1,17).
edge(2,5). edge(2,9).
edge(3,6).
edge(4,7).
edge(5,8).
edge(6,7).
edge(8,16). edge(8,24).
edge(9,10). edge(9,12). edge(9,17).
edge(10,14).
edge(11,15).
edge(12,16).
edge(13,14).
edge(16,24).
edge(17,18). edge(17,20).
edge(18,19). edge(18,21).
edge(19,22).
edge(20,23).
edge(21,24).

% Symmetric edges (ensure both directions for safety)
edge(V2, V1) :- edge(V1, V2).

% Selection choice
{selected(V)} :- vertex(V).

% Constraint 1: No two selected vertices are adjacent
:- selected(V1), selected(V2), edge(V1, V2), V1 != V2.

% Counts
core_count(N) :- N = #count{V : selected(V), type(V, core)}.
support_count(N) :- N = #count{V : selected(V), type(V, support)}.
peripheral_count(N) :- N = #count{V : selected(V), type(V, peripheral)}.

% Constraint 2: At most two core vertices
:- core_count(N), N > 2.

% Helper: exists support in zone Z
exists_support_in_zone(Z) :- selected(W), type(W, support), zone(W, Z).

% Constraint 3: For each core vertex, at least one support vertex in same zone
:- selected(V), type(V, core), zone(V, Z), not exists_support_in_zone(Z).

% Constraint 4: If any peripheral from zone 1, then no vertex from zone 3
:- selected(V), type(V, peripheral), zone(V, 1), selected(W), zone(W, 3).

% Constraint 5: Peripheral count <= core count
:- peripheral_count(N), core_count(M), N > M.

% Objective: maximize size
#maximize {1, V : selected(V)}.

% Output predicates
independent_set(V) :- selected(V).
size(N) :- N = #count{V : selected(V)}.
core_vertices(V) :- selected(V), type(V, core).
support_vertices(V) :- selected(V), type(V, support).
peripheral_vertices(V) :- selected(V), type(V, peripheral).

% Show directives
#show independent_set/1.
#show size/1.
#show core_vertices/1.
#show support_vertices/1.
#show peripheral_vertices/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.