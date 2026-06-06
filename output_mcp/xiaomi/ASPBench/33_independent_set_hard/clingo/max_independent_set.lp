% Domain definitions
vertex(1..24).

% Zone assignments
zone(V, 1) :- V = 1..8.
zone(V, 2) :- V = 9..16.
zone(V, 3) :- V = 17..24.

% Type assignments
type(1, core). type(9, core). type(17, core).
type(2, support). type(3, support). type(10, support). type(11, support). type(18, support). type(19, support).
type(4, peripheral). type(5, peripheral). type(6, peripheral). type(7, peripheral). type(8, peripheral).
type(12, peripheral). type(13, peripheral). type(14, peripheral). type(15, peripheral). type(16, peripheral).
type(20, peripheral). type(21, peripheral). type(22, peripheral). type(23, peripheral). type(24, peripheral).

% Edges (undirected, store both directions)
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

% Symmetric edges
edge(V2, V1) :- edge(V1, V2).

% Choice: each vertex can be in the independent set or not
{in_set(V)} :- vertex(V).

% Constraint 1: Standard Independence - no two adjacent vertices can both be in set
:- in_set(V1), in_set(V2), edge(V1, V2).

% Derived predicates for types in set
core_in_set(V) :- in_set(V), type(V, core).
support_in_set(V) :- in_set(V), type(V, support).
peripheral_in_set(V) :- in_set(V), type(V, peripheral).

% Counts
core_count(N) :- N = #count{V : core_in_set(V)}.
support_count(N) :- N = #count{V : support_in_set(V)}.
peripheral_count(N) :- N = #count{V : peripheral_in_set(V)}.

% Constraint 2: Core Count Limit - at most 2 core vertices
:- core_count(N), N > 2.

% Constraint 3: Core-Support Dependency
% For each core vertex in set, at least one support vertex from same zone must be in set
has_support_in_zone(Z) :- support_in_set(V), zone(V, Z).
:- core_in_set(V), zone(V, Z), not has_support_in_zone(Z).

% Constraint 4: Conditional Zone Exclusion
% If any peripheral vertex from zone 1 is in set, then no vertex from zone 3 can be in set
has_zone1_peripheral :- peripheral_in_set(V), zone(V, 1).
has_zone3_vertex :- in_set(V), zone(V, 3).
:- has_zone1_peripheral, has_zone3_vertex.

% Constraint 5: Peripheral Headcount Rule
% Peripheral count must not exceed core count
:- peripheral_count(NP), core_count(NC), NP > NC.

% Objective: maximize size of independent set
#maximize {1, V : in_set(V)}.

% Output formatting
#show in_set/1.
#show core_in_set/1.
#show support_in_set/1.
#show peripheral_in_set/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.