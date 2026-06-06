% ===== DOMAIN =====
% Elements 1..20
element(1..20).

% Sets 0..13
set(0..13).

% ===== SET DATA =====
% Set 0: {1,2,3,4,5}, cost=1, category=A
covers(0,1). covers(0,2). covers(0,3). covers(0,4). covers(0,5).
cost(0,1). category(0,a).

% Set 1: {1,6,11,16}, cost=1, category=A
covers(1,1). covers(1,6). covers(1,11). covers(1,16).
cost(1,1). category(1,a).

% Set 2: {2,7,12,17}, cost=1, category=A
covers(2,2). covers(2,7). covers(2,12). covers(2,17).
cost(2,1). category(2,a).

% Set 3: {3,8,13,18}, cost=1, category=B
covers(3,3). covers(3,8). covers(3,13). covers(3,18).
cost(3,1). category(3,b).

% Set 4: {4,9,14,19}, cost=1, category=B
covers(4,4). covers(4,9). covers(4,14). covers(4,19).
cost(4,1). category(4,b).

% Set 5: {5,10,15,20}, cost=1, category=B
covers(5,5). covers(5,10). covers(5,15). covers(5,20).
cost(5,1). category(5,b).

% Set 6: {6,7,8,9,10}, cost=1, category=C
covers(6,6). covers(6,7). covers(6,8). covers(6,9). covers(6,10).
cost(6,1). category(6,c).

% Set 7: {1,3,5,7,9}, cost=1, category=C
covers(7,1). covers(7,3). covers(7,5). covers(7,7). covers(7,9).
cost(7,1). category(7,c).

% Set 8: {2,4,6,8,10}, cost=1, category=C
covers(8,2). covers(8,4). covers(8,6). covers(8,8). covers(8,10).
cost(8,1). category(8,c).

% Set 9: {1,2,3,4,5,6,7}, cost=4, specialized
covers(9,1). covers(9,2). covers(9,3). covers(9,4). covers(9,5). covers(9,6). covers(9,7).
cost(9,4). category(9,specialized).

% Set 10: {11,12,13,14,15}, cost=4, specialized
covers(10,11). covers(10,12). covers(10,13). covers(10,14). covers(10,15).
cost(10,4). category(10,specialized).

% Set 11: {8,9,10}, cost=4, specialized
covers(11,8). covers(11,9). covers(11,10).
cost(11,4). category(11,specialized).

% Set 12: {1,5,10,15}, cost=4, specialized
covers(12,1). covers(12,5). covers(12,10). covers(12,15).
cost(12,4). category(12,specialized).

% Set 13: {16,17,18,19,20}, cost=4, specialized
covers(13,16). covers(13,17). covers(13,18). covers(13,19). covers(13,20).
cost(13,4). category(13,specialized).

% Standard category helper
standard(a). standard(b). standard(c).

% ===== CHOICE RULE =====
{ selected(S) } :- set(S).

% ===== CONSTRAINT 1: Full Coverage =====
:- element(E), not covered(E).
covered(E) :- selected(S), covers(S, E).

% ===== CONSTRAINT 2: Prerequisites =====
% Set 9 requires Set 0
:- selected(9), not selected(0).
% Set 11 requires Set 6
:- selected(11), not selected(6).

% ===== CONSTRAINT 3: Mutual Exclusion =====
:- selected(12), selected(13).

% ===== CONSTRAINT 4: Category Balancing =====
% If any specialized set is selected, must have at least one from each of A, B, C
has_specialized :- selected(S), category(S, specialized).
has_cat(C) :- selected(S), category(S, C).
:- has_specialized, standard(C), not has_cat(C).

% ===== REDUNDANCY PENALTY CALCULATION =====
% Count how many sets cover each element
cov_count(E, N) :- element(E), N = #count { S : selected(S), covers(S, E) }.

% Penalty of 2 for each element covered by more than 3 sets
elem_penalty(E, 2) :- cov_count(E, N), N > 3.
elem_penalty(E, 0) :- cov_count(E, N), N <= 3.

% ===== COST CALCULATION =====
base_cost(B) :- B = #sum { C, S : selected(S), cost(S, C) }.
redundancy_penalty(R) :- R = #sum { P, E : elem_penalty(E, P) }.
total_cost(T) :- base_cost(B), redundancy_penalty(R), T = B + R.

% ===== OPTIMIZATION =====
#minimize { T : total_cost(T) }.

% ===== OUTPUT =====
#show selected/1.
#show base_cost/1.
#show redundancy_penalty/1.
#show total_cost/1.
#show covered/1.