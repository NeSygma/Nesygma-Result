% Define the domain
vertex(1..24).

% Define zones (vertex, zone)
zone(1,1). zone(2,1). zone(3,1). zone(4,1). zone(5,1). zone(6,1). zone(7,1). zone(8,1).
zone(9,2). zone(10,2). zone(11,2). zone(12,2). zone(13,2). zone(14,2). zone(15,2). zone(16,2).
zone(17,3). zone(18,3). zone(19,3). zone(20,3). zone(21,3). zone(22,3). zone(23,3). zone(24,3).

% Define types (vertex, type)
type(1,core).   type(9,core).   type(17,core).
type(2,support). type(3,support). type(10,support). type(11,support). type(18,support). type(19,support).
type(4,peripheral). type(5,peripheral). type(6,peripheral). type(7,peripheral).
type(8,peripheral). type(12,peripheral). type(13,peripheral). type(14,peripheral).
type(15,peripheral). type(16,peripheral). type(20,peripheral). type(21,peripheral).
type(22,peripheral). type(23,peripheral). type(24,peripheral).

% Define edges (undirected, so both directions)
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
edge(18,19).
edge(18,21).
edge(19,22).
edge(20,23).
edge(21,24).

% For undirected edges, also add the reverse direction
edge(V1,V2) :- edge(V2,V1), V1 < V2.

% Choice rule for the independent set
{in_set(V)} :- vertex(V).

% Constraint 1: Standard independence (no two connected vertices in the set)
:- in_set(V1), in_set(V2), edge(V1,V2), V1 < V2.

% Constraint 2: Core count limit (at most 2 core vertices)
core_count(N) :- N = #count{V : in_set(V), type(V,core)}.
:- core_count(N), N > 2.

% Constraint 3: Core-Support Dependency
% For each core vertex in the set, there must be at least one support vertex in the same zone in the set
has_support_in_same_zone(V) :- in_set(V), type(V,core), in_set(W), type(W,support), zone(V,Z), zone(W,Z).
:- in_set(V), type(V,core), not has_support_in_same_zone(V).

% Constraint 4: Conditional Zone Exclusion
% If any peripheral vertex from zone 1 is in the set, then no vertex from zone 3 can be in the set
peripheral_in_zone1 :- in_set(V), type(V,peripheral), zone(V,1).
vertex_in_zone3 :- in_set(V), zone(V,3).
:- peripheral_in_zone1, vertex_in_zone3.

% Constraint 5: Peripheral Headcount Rule
% Number of peripheral vertices ≤ number of core vertices
peripheral_count(P) :- P = #count{V : in_set(V), type(V,peripheral)}.
core_count(C) :- C = #count{V : in_set(V), type(V,core)}.
:- peripheral_count(P), core_count(C), P > C.

% Objective: Maximize the size of the independent set
#maximize {1@1, V : in_set(V)}.

% Helper predicates for output
core_vertices(V) :- in_set(V), type(V,core).
support_vertices(V) :- in_set(V), type(V,support).
peripheral_vertices(V) :- in_set(V), type(V,peripheral).

% Counts for output
size(N) :- N = #count{V : in_set(V)}.

% Show directives
#show in_set/1.
#show size/1.
#show core_vertices/1.
#show support_vertices/1.
#show peripheral_vertices/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.