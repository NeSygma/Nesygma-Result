% Vertices
vertex(1..24).

% Types
% Core vertices
core(1). core(9). core(17).
% Support vertices
support(2). support(3). support(10). support(11). support(18). support(19).
% Peripheral vertices (derived)
peripheral(V) :- vertex(V), not core(V), not support(V).

% Zones
zone(1,1). zone(2,1). zone(3,1). zone(4,1). zone(5,1). zone(6,1). zone(7,1). zone(8,1).
zone(9,2). zone(10,2). zone(11,2). zone(12,2). zone(13,2). zone(14,2). zone(15,2). zone(16,2).
zone(17,3). zone(18,3). zone(19,3). zone(20,3). zone(21,3). zone(22,3). zone(23,3). zone(24,3).

% Edges (undirected)
edge(1,2). edge(2,1).
edge(1,4). edge(4,1).
edge(1,10). edge(10,1).
edge(1,17). edge(17,1).
edge(2,5). edge(5,2).
edge(2,9). edge(9,2).
edge(3,6). edge(6,3).
edge(4,7). edge(7,4).
edge(5,8). edge(8,5).
edge(6,7). edge(7,6).
edge(8,16). edge(16,8).
edge(8,24). edge(24,8).
edge(9,10). edge(10,9).
edge(9,12). edge(12,9).
edge(9,17). edge(17,9).
edge(10,14). edge(14,10).
edge(11,15). edge(15,11).
edge(12,16). edge(16,12).
edge(13,14). edge(14,13).
edge(16,24). edge(24,16).
edge(17,18). edge(18,17).
edge(17,20). edge(20,17).
edge(18,19). edge(19,18).
edge(18,21). edge(21,18).
edge(19,22). edge(22,19).
edge(20,23). edge(23,20).
edge(21,24). edge(24,21).

% Choice of vertices in the independent set
{in_set(V)} :- vertex(V).

% Constraint: No two adjacent vertices in the set
:- in_set(U), in_set(V), edge(U,V).

% Constraint: At most two core vertices
:- #count{V : in_set(V), core(V)} > 2.

% Support in same zone as a core vertex
support_in_same_zone(C) :- in_set(S), support(S), zone(C,Z), zone(S,Z).
:- in_set(C), core(C), not support_in_same_zone(C).

% Conditional zone exclusion: peripheral from zone1 forbids any vertex from zone3
:- in_set(V1), peripheral(V1), zone(V1,1), in_set(V3), zone(V3,3).

% Objective: maximize size of the independent set
#maximize {1 : in_set(V)}.

% Show directives
#show in_set/1.
#show core_in_set/1.
#show support_in_set/1.
#show peripheral_in_set/1.
#show core_count/1.
#show support_count/1.
#show peripheral_count/1.
#show size/1.