%% Instance Data
vertex(1..24).

%% Zones
zone(V,1) :- V=1..8.
zone(V,2) :- V=9..16.
zone(V,3) :- V=17..24.

%% Types
type(V,core)     :- V=1; V=9; V=17.
type(V,support)   :- V=2; V=3; V=10; V=11; V=18; V=19.
type(V,peripheral) :- V=4; V=5; V=6; V=7; V=8; V=12; V=13; V=14; V=15; V=16; V=20; V=21; V=22; V=23; V=24.

%% Edges (undirected, given once)
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

%% Symmetric edges
edge(X,Y) :- edge(Y,X), X<Y.

%% Decision: select vertices for independent set
{ selected(V) } :- vertex(V).

%% Constraint 1: Standard Independence - no edges between selected vertices
:- selected(U), selected(V), edge(U,V).

%% Derived categories
core_sel(V) :- selected(V), type(V,core).
support_sel(V) :- selected(V), type(V,support).
peripheral_sel(V) :- selected(V), type(V,peripheral).

%% Constraint 2: Core Count Limit - at most 2 core vertices
:- #count{V : core_sel(V)} > 2.

%% Constraint 3: Core-Support Dependency
%% For each selected core vertex, at least one support from same zone must be selected
has_core_support(C) :- core_sel(C), support_sel(S), zone(C,Z), zone(S,Z).
:- core_sel(C), not has_core_support(C).

%% Constraint 4: Conditional Zone Exclusion
%% If any peripheral from zone 1 selected, then no vertex from zone 3 selected
peripheral_zone1(V) :- selected(V), type(V,peripheral), zone(V,1).
zone3_sel(V) :- selected(V), zone(V,3).
:- peripheral_zone1(_), zone3_sel(_).

%% Constraint 5: Peripheral Headcount Rule
%% #peripheral <= #core. Compute counts and compare.
core_count(C) :- C = #count{V : core_sel(V)}.
peripheral_count(P) :- P = #count{V : peripheral_sel(V)}.
:- peripheral_count(P), core_count(C), P > C.

%% Objective: maximize independent set size
#maximize {1,V : selected(V)}.

%% Output
#show selected/1.