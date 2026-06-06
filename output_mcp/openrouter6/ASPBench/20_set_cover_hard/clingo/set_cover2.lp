% Set Cover Problem with Constraints and Penalty

% --- Domain Definitions ---
element(1..20).
set(0..13).

% --- Set Data ---
% Set 0: {1,2,3,4,5}, cost=1, category=A
set_elements(0,1). set_elements(0,2). set_elements(0,3). set_elements(0,4). set_elements(0,5).
set_cost(0,1). set_category(0,"A").

% Set 1: {1,6,11,16}, cost=1, category=A
set_elements(1,1). set_elements(1,6). set_elements(1,11). set_elements(1,16).
set_cost(1,1). set_category(1,"A").

% Set 2: {2,7,12,17}, cost=1, category=A
set_elements(2,2). set_elements(2,7). set_elements(2,12). set_elements(2,17).
set_cost(2,1). set_category(2,"A").

% Set 3: {3,8,13,18}, cost=1, category=B
set_elements(3,3). set_elements(3,8). set_elements(3,13). set_elements(3,18).
set_cost(3,1). set_category(3,"B").

% Set 4: {4,9,14,19}, cost=1, category=B
set_elements(4,4). set_elements(4,9). set_elements(4,14). set_elements(4,19).
set_cost(4,1). set_category(4,"B").

% Set 5: {5,10,15,20}, cost=1, category=B
set_elements(5,5). set_elements(5,10). set_elements(5,15). set_elements(5,20).
set_cost(5,1). set_category(5,"B").

% Set 6: {6,7,8,9,10}, cost=1, category=C
set_elements(6,6). set_elements(6,7). set_elements(6,8). set_elements(6,9). set_elements(6,10).
set_cost(6,1). set_category(6,"C").

% Set 7: {1,3,5,7,9}, cost=1, category=C
set_elements(7,1). set_elements(7,3). set_elements(7,5). set_elements(7,7). set_elements(7,9).
set_cost(7,1). set_category(7,"C").

% Set 8: {2,4,6,8,10}, cost=1, category=C
set_elements(8,2). set_elements(8,4). set_elements(8,6). set_elements(8,8). set_elements(8,10).
set_cost(8,1). set_category(8,"C").

% Set 9: {1,2,3,4,5,6,7}, cost=4 (specialized)
set_elements(9,1). set_elements(9,2). set_elements(9,3). set_elements(9,4). set_elements(9,5). set_elements(9,6). set_elements(9,7).
set_cost(9,4). set_category(9,"specialized").

% Set 10: {11,12,13,14,15}, cost=4 (specialized)
set_elements(10,11). set_elements(10,12). set_elements(10,13). set_elements(10,14). set_elements(10,15).
set_cost(10,4). set_category(10,"specialized").

% Set 11: {8,9,10}, cost=4 (specialized)
set_elements(11,8). set_elements(11,9). set_elements(11,10).
set_cost(11,4). set_category(11,"specialized").

% Set 12: {1,5,10,15}, cost=4 (specialized)
set_elements(12,1). set_elements(12,5). set_elements(12,10). set_elements(12,15).
set_cost(12,4). set_category(12,"specialized").

% Set 13: {16,17,18,19,20}, cost=4 (specialized)
set_elements(13,16). set_elements(13,17). set_elements(13,18). set_elements(13,19). set_elements(13,20).
set_cost(13,4). set_category(13,"specialized").

% --- Selection Choice Rule ---
% Each set can be selected or not
{ selected(S) } :- set(S).

% --- Constraints ---
% 1. Full Coverage: each element must be covered by at least one selected set
covered(E) :- element(E), set_elements(S, E), selected(S).
:- element(E), not covered(E).

% 2. Prerequisites
% Set 9 requires Set 0
:- selected(9), not selected(0).
% Set 11 requires Set 6
:- selected(11), not selected(6).

% 3. Mutual Exclusion: Set 12 and Set 13 cannot be selected together
:- selected(12), selected(13).

% 4. Category Balancing: If any specialized set is selected, must include at least one set from each standard category A, B, C
% Define standard categories
standard_category("A"). standard_category("B"). standard_category("C").
% Check if any specialized set is selected
specialized_selected :- selected(S), set_cost(S, C), C > 1.
% For each standard category, require at least one selected set from that category
:- specialized_selected, standard_category(Cat), not (selected(S), set_category(S, Cat)).

% --- Coverage Counting ---
% Count how many selected sets cover each element
coverage_count(E, N) :- element(E), N = #count{ S : set_elements(S, E), selected(S) }.

% --- Redundancy Penalty ---
% For each element covered by more than 3 sets, add penalty of 2
% Use helper predicate for penalty per element
penalty_element(E, 2) :- coverage_count(E, N), N > 3.
redundancy_penalty(P) :- P = #sum{ Pen, E : penalty_element(E, Pen) }.

% --- Total Cost Calculation ---
base_cost(C) :- C = #sum{ Cost, S : selected(S), set_cost(S, Cost) }.
total_cost(T) :- base_cost(B), redundancy_penalty(P), T = B + P.

% --- Objective: Minimize Total Cost ---
#minimize { T : total_cost(T) }.

% --- Output Fields ---
% selected_sets: we show selected(S) for each selected set
% total_sets: count of selected sets
total_sets(N) :- N = #count{ S : selected(S) }.
% covered_elements: we show covered(E) for each covered element (should be all 1..20)
% base_cost, redundancy_penalty, total_cost already defined

% --- Show directives ---
#show selected/1.
#show total_sets/1.
#show covered/1.
#show base_cost/1.
#show redundancy_penalty/1.
#show total_cost/1.
#show coverage_count/2.