% Clique Optimization Problem with Type Diversity and Weight Constraints

% ===== DOMAIN DECLARATION =====
% Vertices 0-19
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7). vertex(8). vertex(9).
vertex(10). vertex(11). vertex(12). vertex(13). vertex(14). vertex(15). vertex(16). vertex(17). vertex(18). vertex(19).

% Types
type(alpha). type(beta). type(gamma). type(delta).

% Vertex types (from table)
type(0, alpha). type(1, alpha). type(2, alpha). type(3, alpha). type(4, beta). type(5, alpha). type(6, beta). type(7, beta). type(8, beta). type(9, delta).
type(10, delta). type(11, beta). type(12, gamma). type(13, gamma). type(14, gamma). type(15, delta). type(16, delta). type(17, gamma). type(18, alpha). type(19, beta).

% Vertex weights (from table)
weight(0, 20). weight(1, 20). weight(2, 15). weight(3, 20). weight(4, 30). weight(5, 15). weight(6, 30). weight(7, 30). weight(8, 18). weight(9, 10).
weight(10, 10). weight(11, 12). weight(12, 25). weight(13, 25). weight(14, 20). weight(15, 5). weight(16, 5). weight(17, 19). weight(18, 40). weight(19, 40).

% Edges (undirected - we'll add both directions for convenience)
edge(0, 1). edge(0, 3). edge(0, 4). edge(0, 6). edge(0, 7). edge(0, 9). edge(0, 10).
edge(1, 3). edge(1, 4). edge(1, 6). edge(1, 7). edge(1, 9).
edge(2, 5). edge(2, 8). edge(2, 11). edge(2, 14). edge(2, 17). edge(2, 18).
edge(3, 4). edge(3, 6). edge(3, 7). edge(3, 9).
edge(4, 6). edge(4, 7). edge(4, 9).
edge(5, 8). edge(5, 11). edge(5, 14). edge(5, 17). edge(5, 19).
edge(6, 7). edge(6, 9).
edge(7, 9).
edge(8, 11). edge(8, 14). edge(8, 17).
edge(11, 14). edge(11, 17).
edge(12, 13).
edge(14, 17).
edge(15, 16).

% Add reverse edges for undirected graph
edge(U, V) :- edge(V, U).

% ===== CLIQUE SELECTION =====
% Choose which vertices are in the clique (0 or 1 per vertex)
{ clique(V) } :- vertex(V).

% ===== CONSTRAINTS =====

% 1. Clique property: For any two vertices in clique, edge must exist
:- clique(U), clique(V), U != V, not edge(U, V).

% 2. Type diversity: At most 2 vertices of any single type
type_count(T, C) :- type(T), C = #count{ V : clique(V), type(V, T) }.
:- type_count(T, C), C > 2.

% 3. Weight limit: Total weight ≤ 100
clique_total_weight(S) :- S = #sum{ W, V : clique(V), weight(V, W) }.
:- clique_total_weight(S), S > 100.

% ===== DERIVED PROPERTIES =====
% Clique size
clique_size(N) :- N = #count{ V : clique(V) }.

% Edges within clique (for output)
clique_edge(U, V) :- clique(U), clique(V), U < V, edge(U, V).

% Type distribution for output
clique_type_distribution(T, C) :- type(T), C = #count{ V : clique(V), type(V, T) }.

% ===== OPTIMIZATION =====
% Maximize clique size
#maximize { 1, V : clique(V) }.

% ===== OUTPUT =====
#show clique/1.
#show clique_size/1.
#show clique_edge/2.
#show clique_total_weight/1.
#show clique_type_distribution/2.