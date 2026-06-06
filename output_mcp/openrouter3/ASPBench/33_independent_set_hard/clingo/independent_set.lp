% Maximum Independent Set with Constraints

% ===== Domain Declarations =====
vertex(1..24).
zone(1..3).
type(core; support; peripheral).

% ===== Vertex Attributes =====
% Zone assignments
zone(V, 1) :- vertex(V), V >= 1, V <= 8.
zone(V, 2) :- vertex(V), V >= 9, V <= 16.
zone(V, 3) :- vertex(V), V >= 17, V <= 24.

% Type assignments
type(V, core) :- vertex(V), V = 1; V = 9; V = 17.
type(V, support) :- vertex(V), V = 2; V = 3; V = 10; V = 11; V = 18; V = 19.
type(V, peripheral) :- vertex(V), not type(V, core), not type(V, support).

% ===== Edges =====
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

% Make edges undirected
edge(V2, V1) :- edge(V1, V2).

% ===== Independent Set Selection =====
% Choose which vertices are in the independent set
{ selected(V) } :- vertex(V).

% ===== Constraint 1: Standard Independence =====
% No two selected vertices can be connected by an edge
:- selected(V1), selected(V2), edge(V1, V2).

% ===== Constraint 2: Core Count Limit =====
% At most 2 core vertices can be selected
core_count(N) :- N = #count{ V : selected(V), type(V, core) }.
:- core_count(N), N > 2.

% ===== Constraint 3: Core-Support Dependency =====
% For each core vertex selected, at least one support vertex from same zone must be selected
% Helper: For each core vertex, check if there's a support vertex in same zone
has_support_in_zone(V, Z) :- selected(V), type(V, core), zone(V, Z), 
                              selected(S), type(S, support), zone(S, Z).
:- selected(V), type(V, core), zone(V, Z), not has_support_in_zone(V, Z).

% ===== Constraint 4: Conditional Zone Exclusion =====
% If any peripheral vertex from zone 1 is selected, no vertices from zone 3 can be selected
has_peripheral_zone1 :- selected(V), type(V, peripheral), zone(V, 1).
has_zone3 :- selected(V), zone(V, 3).
:- has_peripheral_zone1, has_zone3.

% ===== Constraint 5: Peripheral Headcount Rule =====
% Peripheral count must not exceed core count
peripheral_count(N) :- N = #count{ V : selected(V), type(V, peripheral) }.
:- peripheral_count(P), core_count(C), P > C.

% ===== Objective: Maximize Set Size =====
size(N) :- N = #count{ V : selected(V) }.

% ===== Optimization =====
#maximize { 1, V : selected(V) }.

% ===== Output =====
#show selected/1.
#show size/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.

% Helper predicates for output
core_vertices(V) :- selected(V), type(V, core).
support_vertices(V) :- selected(V), type(V, support).
peripheral_vertices(V) :- selected(V), type(V, peripheral).

#show core_vertices/1.
#show support_vertices/1.
#show peripheral_vertices/1.