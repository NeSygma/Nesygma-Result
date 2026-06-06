% Independent Dominating Set with Type-Specific Domination Requirements

% ===== 1. DOMAIN DEFINITIONS =====
% Vertices 1-18
vertex(1..18).

% ===== 2. GRAPH EDGES (undirected) =====
% Define edges in both directions for symmetry
edge(1,2). edge(2,1).
edge(1,4). edge(4,1).
edge(1,5). edge(5,1).
edge(2,4). edge(4,2).
edge(2,5). edge(5,2).
edge(3,4). edge(4,3).
edge(3,9). edge(9,3).
edge(4,5). edge(5,4).
edge(4,18). edge(18,4).
edge(6,7). edge(7,6).
edge(6,9). edge(9,6).
edge(6,10). edge(10,6).
edge(7,9). edge(9,7).
edge(8,9). edge(9,8).
edge(8,14). edge(14,8).
edge(9,10). edge(10,9).
edge(11,12). edge(12,11).
edge(11,14). edge(14,11).
edge(12,14). edge(14,12).
edge(13,14). edge(14,13).
edge(13,17). edge(17,13).
edge(15,16). edge(16,15).
edge(15,17). edge(17,15).
edge(16,17). edge(17,16).
edge(17,18). edge(18,17).

% ===== 3. VERTEX TYPES =====
% Critical vertices ('c')
type(1, c). type(5, c). type(10, c). type(15, c).
% Standard vertices ('s')
type(2, s). type(6, s). type(7, s). type(11, s). type(12, s). type(16, s).
% Resilient vertices ('r')
type(3, r). type(8, r). type(13, r). type(18, r).

% ===== 4. VERTEX COSTS =====
cost(4, 2). cost(9, 2).
cost(14, 3). cost(17, 3).
cost(1, 5). cost(2, 5). cost(3, 5). cost(5, 5). cost(6, 5). cost(7, 5). cost(8, 5).
cost(10, 8). cost(11, 8). cost(12, 8). cost(13, 8). cost(15, 8). cost(16, 8). cost(18, 8).

% ===== 5. DECISION VARIABLES =====
% Each vertex can be either in the dominating set or not
{ selected(V) } :- vertex(V).

% ===== 6. CONSTRAINTS =====

% 6.1 Independent Set: No two adjacent vertices can both be selected
:- selected(V1), selected(V2), edge(V1, V2), V1 != V2.

% 6.2 Domination Requirements for Non-Selected Vertices
% Helper: Count selected neighbors for each vertex
neighbor_count(V, N) :- vertex(V), N = #count{ U : edge(V, U), selected(U) }.

% Critical vertices: Must have at least 1 selected neighbor if not in set
:- not selected(V), type(V, c), neighbor_count(V, N), N < 1.

% Standard vertices: Must have at least 1 selected neighbor if not in set
:- not selected(V), type(V, s), neighbor_count(V, N), N < 1.

% Resilient vertices: Must have at least 2 distinct selected neighbors if not in set
:- not selected(V), type(V, r), neighbor_count(V, N), N < 2.

% 6.3 All vertices must be dominated (either in set or meet adjacency requirement)
% This is already enforced by the above constraints for non-selected vertices
% For selected vertices, they dominate themselves

% ===== 7. OBJECTIVE: MINIMIZE TOTAL COST =====
% Compute total cost of selected vertices
total_cost(S) :- S = #sum{ C, V : selected(V), cost(V, C) }.

% Minimize total cost
#minimize{ C, V : selected(V), cost(V, C) }.

% ===== 8. OUTPUT =====
% Show selected vertices (sorted by vertex number)
#show selected/1.
% Show total cost
#show total_cost/1.