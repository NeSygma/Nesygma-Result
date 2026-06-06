%%% Instance Data %%%

% Vertices
vertex(1..24).

% Zones
zone(1;2;3).
zone_of(1,1). zone_of(2,1). zone_of(3,1). zone_of(4,1). zone_of(5,1). zone_of(6,1). zone_of(7,1). zone_of(8,1).
zone_of(9,2). zone_of(10,2). zone_of(11,2). zone_of(12,2). zone_of(13,2). zone_of(14,2). zone_of(15,2). zone_of(16,2).
zone_of(17,3). zone_of(18,3). zone_of(19,3). zone_of(20,3). zone_of(21,3). zone_of(22,3). zone_of(23,3). zone_of(24,3).

% Types
type(1,core). type(9,core). type(17,core).
type(2,support). type(3,support). type(10,support). type(11,support). type(18,support). type(19,support).
type(4,peripheral). type(5,peripheral). type(6,peripheral). type(7,peripheral). type(8,peripheral).
type(12,peripheral). type(13,peripheral). type(14,peripheral). type(15,peripheral). type(16,peripheral).
type(20,peripheral). type(21,peripheral). type(22,peripheral). type(23,peripheral). type(24,peripheral).

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

% Symmetric edges
edge(Y,X) :- edge(X,Y).

%%% Choice: Select vertices for the independent set %%%
{ selected(V) : vertex(V) }.

%%% Constraint 1: Standard Independence %%%
:- selected(V1), selected(V2), edge(V1,V2), V1 < V2.

%%% Helper predicates for types %%%
core(V)    :- type(V, core).
support(V) :- type(V, support).
peripheral(V) :- type(V, peripheral).

%%% Constraint 2: Core Count Limit (at most 2) %%%
core_count(N) :- N = #count{ V : selected(V), core(V) }.
:- core_count(N), N > 2.

%%% Constraint 3: Core-Support Dependency %%%
% For each selected core, there must be at least one selected support in the same zone.
:- selected(V), core(V), zone_of(V, Z),
   not selected(U) : support(U), zone_of(U, Z).

%%% Constraint 4: Conditional Zone Exclusion %%%
% If any peripheral from zone 1 is selected, then no vertex from zone 3 can be selected.
has_zone1_peripheral :- selected(V), peripheral(V), zone_of(V, 1).
:- has_zone1_peripheral, selected(V), zone_of(V, 3).

%%% Constraint 5: Peripheral Headcount Rule %%%
% Peripheral count must not exceed core count.
peripheral_count(N) :- N = #count{ V : selected(V), peripheral(V) }.
:- peripheral_count(P), core_count(C), P > C.

%%% Objective: Maximize the size of the independent set %%%
set_size(N) :- N = #count{ V : selected(V) }.
#maximize { N : set_size(N) }.

%%% Output %%%
#show selected/1.
#show set_size/1.
#show core_count/1.
#show peripheral_count/1.