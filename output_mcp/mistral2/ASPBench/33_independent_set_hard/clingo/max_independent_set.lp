% Define the vertices
vertex(1..24).

% Define zones
zone(1,1). zone(2,1). zone(3,1). zone(4,1). zone(5,1). zone(6,1). zone(7,1). zone(8,1).
zone(9,2). zone(10,2). zone(11,2). zone(12,2). zone(13,2). zone(14,2). zone(15,2). zone(16,2).
zone(17,3). zone(18,3). zone(19,3). zone(20,3). zone(21,3). zone(22,3). zone(23,3). zone(24,3).

% Define types
% Core vertices: 1, 9, 17
type(1, core). type(9, core). type(17, core).
% Support vertices: 2, 3, 10, 11, 18, 19
type(2, support). type(3, support). type(10, support). type(11, support). type(18, support). type(19, support).
% Peripheral vertices: 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24
type(4, peripheral). type(5, peripheral). type(6, peripheral). type(7, peripheral). type(8, peripheral).
type(12, peripheral). type(13, peripheral). type(14, peripheral). type(15, peripheral). type(16, peripheral).
type(20, peripheral). type(21, peripheral). type(22, peripheral). type(23, peripheral). type(24, peripheral).

% Define edges
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

% Choice rule: choose which vertices are in the set
{ in_set(V) : vertex(V) }.

% Standard independence: no two vertices in the set can be connected by an edge
:- in_set(V1), in_set(V2), edge(V1, V2), V1 < V2.

% Count the number of core, support, and peripheral vertices in the set
core_in_set(V) :- in_set(V), type(V, core).
support_in_set(V) :- in_set(V), type(V, support).
peripheral_in_set(V) :- in_set(V), type(V, peripheral).

core_count(C) :- C = #count{ V : core_in_set(V) }.
support_count(S) :- S = #count{ V : support_in_set(V) }.
peripheral_count(P) :- P = #count{ V : peripheral_in_set(V) }.

% Core count limit: at most two core vertices in the set
:- core_count(C), C > 2.

% Core-Support Dependency: for every core vertex in the set, at least one support vertex from the same zone must also be in the set
:- core_in_set(V), not support_in_set(W), zone(V, Z), zone(W, Z), type(W, support).

% Conditional Zone Exclusion: if any peripheral vertex from zone 1 is in the set, no vertex from zone 3 can be in the set
:- peripheral_in_set(V), zone(V, 1), in_set(U), zone(U, 3).

% Peripheral Headcount Rule: the number of peripheral vertices in the set must not exceed the number of core vertices in the set
:- peripheral_count(P), core_count(C), P > C.

% Size of the independent set
size(S) :- S = #count{ V : in_set(V) }.

% Objective: maximize the size of the independent set
#maximize { S : size(S) }.

% Show the vertices in the set, their types, and counts
#show in_set/1.
#show core_in_set/1.
#show support_in_set/1.
#show peripheral_in_set/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.
#show size/1.