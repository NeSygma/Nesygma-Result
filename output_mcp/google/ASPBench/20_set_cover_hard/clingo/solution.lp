% Universe and Sets
element(1..20).
set(0..13).

% Set Elements
set_element(0, 1..5).
set_element(1, 1; 6; 11; 16).
set_element(2, 2; 7; 12; 17).
set_element(3, 3; 8; 13; 18).
set_element(4, 4; 9; 14; 19).
set_element(5, 5; 10; 15; 20).
set_element(6, 6..10).
set_element(7, 1; 3; 5; 7; 9).
set_element(8, 2; 4; 6; 8; 10).
set_element(9, 1..7).
set_element(10, 11..15).
set_element(11, 8..10).
set_element(12, 1; 5; 10; 15).
set_element(13, 16..20).

% Costs
cost(0..8, 1).
cost(9..13, 4).

% Categories
category(0..2, "A").
category(3..5, "B").
category(6..8, "C").
specialized(9..13).

% Selection
{ selected(S) : set(S) }.

% 1. Full Coverage
covered(E) :- element(E), selected(S), set_element(S, E).
:- element(E), not covered(E).

% 2. Prerequisites
:- selected(9), not selected(0).
:- selected(11), not selected(6).

% 3. Mutual Exclusion
:- selected(12), selected(13).

% 4. Category Balancing
has_specialized :- selected(S), specialized(S).
has_cat(Cat) :- selected(S), category(S, Cat).
:- has_specialized, not has_cat("A").
:- has_specialized, not has_cat("B").
:- has_specialized, not has_cat("C").

% 5. Redundancy Penalty
coverage_count(E, N) :- element(E), N = #count { S : selected(S), set_element(S, E) }.
is_redundant(E) :- coverage_count(E, N), N > 3.
redundant_count(C) :- C = #count { E : is_redundant(E) }.
redundancy_penalty(P) :- redundant_count(C), P = C * 2.
redundancy_penalty(0) :- not redundant_count(_).

% Objective
base_cost(BC) :- BC = #sum { C, S : selected(S), cost(S, C) }.
total_cost(TC) :- base_cost(BC), redundancy_penalty(P), TC = BC + P.

#minimize { TC : total_cost(TC) }.

#show selected/1.
#show total_cost/1.