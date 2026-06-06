% Set Covering Problem with Constraints and Optimization

% ===== 1. DOMAIN DEFINITIONS =====
% Universe of elements
element(1..20).

% Sets with indices 0-13
set(0..13).

% Categories
category(a). category(b). category(c).

% ===== 2. SET DATA =====
% Set elements (using quoted strings for constants)
set_elements(0, 1). set_elements(0, 2). set_elements(0, 3). set_elements(0, 4). set_elements(0, 5).
set_elements(1, 1). set_elements(1, 6). set_elements(1, 11). set_elements(1, 16).
set_elements(2, 2). set_elements(2, 7). set_elements(2, 12). set_elements(2, 17).
set_elements(3, 3). set_elements(3, 8). set_elements(3, 13). set_elements(3, 18).
set_elements(4, 4). set_elements(4, 9). set_elements(4, 14). set_elements(4, 19).
set_elements(5, 5). set_elements(5, 10). set_elements(5, 15). set_elements(5, 20).
set_elements(6, 6). set_elements(6, 7). set_elements(6, 8). set_elements(6, 9). set_elements(6, 10).
set_elements(7, 1). set_elements(7, 3). set_elements(7, 5). set_elements(7, 7). set_elements(7, 9).
set_elements(8, 2). set_elements(8, 4). set_elements(8, 6). set_elements(8, 8). set_elements(8, 10).
set_elements(9, 1). set_elements(9, 2). set_elements(9, 3). set_elements(9, 4). set_elements(9, 5). set_elements(9, 6). set_elements(9, 7).
set_elements(10, 11). set_elements(10, 12). set_elements(10, 13). set_elements(10, 14). set_elements(10, 15).
set_elements(11, 8). set_elements(11, 9). set_elements(11, 10).
set_elements(12, 1). set_elements(12, 5). set_elements(12, 10). set_elements(12, 15).
set_elements(13, 16). set_elements(13, 17). set_elements(13, 18). set_elements(13, 19). set_elements(13, 20).

% Set costs
set_cost(0, 1). set_cost(1, 1). set_cost(2, 1). set_cost(3, 1). set_cost(4, 1). set_cost(5, 1).
set_cost(6, 1). set_cost(7, 1). set_cost(8, 1).
set_cost(9, 4). set_cost(10, 4). set_cost(11, 4). set_cost(12, 4). set_cost(13, 4).

% Set categories
set_category(0, a). set_category(1, a). set_category(2, a).
set_category(3, b). set_category(4, b). set_category(5, b).
set_category(6, c). set_category(7, c). set_category(8, c).
% Specialized sets (9-13) have no category

% ===== 3. SELECTION MODEL =====
% Choice rule: each set can be selected or not
{ selected(S) } :- set(S).

% ===== 4. CONSTRAINTS =====
% 4.1 Full Coverage: All elements must be covered by at least one selected set
covered(E) :- element(E), set_elements(S, E), selected(S).
:- element(E), not covered(E).

% 4.2 Prerequisites
% Set 9 requires Set 0
:- selected(9), not selected(0).
% Set 11 requires Set 6
:- selected(11), not selected(6).

% 4.3 Mutual Exclusion: Set 12 and Set 13 cannot be selected together
:- selected(12), selected(13).

% 4.4 Category Balancing: If any specialized set is selected, must have at least one from each standard category
% Specialized sets are 9-13 (cost > 1)
specialized_selected :- selected(9).
specialized_selected :- selected(10).
specialized_selected :- selected(11).
specialized_selected :- selected(12).
specialized_selected :- selected(13).

% Standard category selections
has_category_a :- selected(S), set_category(S, a).
has_category_b :- selected(S), set_category(S, b).
has_category_c :- selected(S), set_category(S, c).

% Constraint: If specialized set selected, must have all standard categories
:- specialized_selected, not has_category_a.
:- specialized_selected, not has_category_b.
:- specialized_selected, not has_category_c.

% ===== 5. COST CALCULATION =====
% 5.1 Base cost: sum of costs of selected sets
base_cost(C) :- C = #sum { Cost, S : selected(S), set_cost(S, Cost) }.

% 5.2 Count coverage per element
coverage_count(E, N) :- element(E), N = #count { S : selected(S), set_elements(S, E) }.

% 5.3 Redundancy penalty: 2 per element covered by more than 3 sets
redundancy_penalty(P) :- P = #sum { 2, E : coverage_count(E, N), N > 3 }.

% 5.4 Total cost
total_cost(TC) :- base_cost(B), redundancy_penalty(P), TC = B + P.

% ===== 6. OPTIMIZATION =====
#minimize { TC : total_cost(TC) }.

% ===== 7. OUTPUT =====
% Show selected sets
#show selected/1.

% Show coverage information
#show covered/1.

% Show cost breakdown
#show base_cost/1.
#show redundancy_penalty/1.
#show total_cost/1.

% Show coverage count for debugging
#show coverage_count/2.