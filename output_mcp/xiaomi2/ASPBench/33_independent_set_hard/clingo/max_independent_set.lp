% Vertices
vertex(1..24).

% Zones
zone(1). zone(2). zone(3).

% Zone membership
in_zone(V, 1) :- vertex(V), V >= 1, V <= 8.
in_zone(V, 2) :- vertex(V), V >= 9, V <= 16.
in_zone(V, 3) :- vertex(V), V >= 17, V <= 24.

% Types
type(1, core). type(9, core). type(17, core).
type(2, support). type(3, support). type(10, support). type(11, support). type(18, support). type(19, support).
type(4, peripheral). type(5, peripheral). type(6, peripheral). type(7, peripheral). type(8, peripheral).
type(12, peripheral). type(13, peripheral). type(14, peripheral). type(15, peripheral). type(16, peripheral).
type(20, peripheral). type(21, peripheral). type(22, peripheral). type(23, peripheral). type(24, peripheral).

% Edges (undirected, stored both ways)
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

% Make edges symmetric
edge(X, Y) :- edge(Y, X).

% Choice: select vertices into independent set
{ selected(V) } :- vertex(V).

% Constraint 1: Standard Independence - no two selected vertices connected by an edge
:- selected(X), selected(Y), edge(X, Y), X < Y.

% Constraint 2: Core Count Limit - at most 2 core vertices
:- #count{ V : selected(V), type(V, core) } > 2.

% Constraint 3: Core-Support Dependency
% For every core vertex in set, at least one support vertex from same zone must be in set
has_support_in_zone(Z) :- selected(V), type(V, support), in_zone(V, Z).
:- selected(V), type(V, core), in_zone(V, Z), not has_support_in_zone(Z).

% Constraint 4: Conditional Zone Exclusion
has_peripheral_zone1 :- selected(V), type(V, peripheral), in_zone(V, 1).
:- has_peripheral_zone1, selected(V), in_zone(V, 3).

% Constraint 5: Peripheral Headcount Rule
core_count(N) :- N = #count{ V : selected(V), type(V, core) }.
peripheral_count(N) :- N = #count{ V : selected(V), type(V, peripheral) }.
:- peripheral_count(P), core_count(C), P > C.

% Objective: maximize size of independent set
#maximize { 1, V : selected(V) }.

% Output
independent_set(V) :- selected(V).
core_vertices(V) :- selected(V), type(V, core).
support_vertices(V) :- selected(V), type(V, support).
peripheral_vertices(V) :- selected(V), type(V, peripheral).
size(N) :- N = #count{ V : selected(V) }.

#show independent_set/1.
#show size/1.
#show core_vertices/1.
#show support_vertices/1.
#show peripheral_vertices/1.
#show core_count/1.
#show peripheral_count/1.