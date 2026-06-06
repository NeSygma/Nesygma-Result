%% Problem: Set Cover with Constraints and Penalty
%% Universe elements 1..20
element(1..20).

%% Sets: set(Index, Cost, Category)
set(0, 1, a).
set(1, 1, a).
set(2, 1, a).
set(3, 1, b).
set(4, 1, b).
set(5, 1, b).
set(6, 1, c).
set(7, 1, c).
set(8, 1, c).
set(9, 4, specialized).
set(10, 4, specialized).
set(11, 4, specialized).
set(12, 4, specialized).
set(13, 4, specialized).

%% Set membership: member(SetIndex, Element)
member(0, 1). member(0, 2). member(0, 3). member(0, 4). member(0, 5).
member(1, 1). member(1, 6). member(1, 11). member(1, 16).
member(2, 2). member(2, 7). member(2, 12). member(2, 17).
member(3, 3). member(3, 8). member(3, 13). member(3, 18).
member(4, 4). member(4, 9). member(4, 14). member(4, 19).
member(5, 5). member(5, 10). member(5, 15). member(5, 20).
member(6, 6). member(6, 7). member(6, 8). member(6, 9). member(6, 10).
member(7, 1). member(7, 3). member(7, 5). member(7, 7). member(7, 9).
member(8, 2). member(8, 4). member(8, 6). member(8, 8). member(8, 10).
member(9, 1). member(9, 2). member(9, 3). member(9, 4). member(9, 5). member(9, 6). member(9, 7).
member(10, 11). member(10, 12). member(10, 13). member(10, 14). member(10, 15).
member(11, 8). member(11, 9). member(11, 10).
member(12, 1). member(12, 5). member(12, 10). member(12, 15).
member(13, 16). member(13, 17). member(13, 18). member(13, 19). member(13, 20).

%% Standard categories
standard_category(a). standard_category(b). standard_category(c).

%% Category of each set
set_category(S, a) :- set(S, _, a).
set_category(S, b) :- set(S, _, b).
set_category(S, c) :- set(S, _, c).
set_category(S, specialized) :- set(S, _, specialized).

%% Decision: select a set
{ selected(S) } :- set(S, _, _).

%% Constraint 1: Full Coverage - every element must be covered by at least one selected set
covered(E) :- selected(S), member(S, E).
:- element(E), not covered(E).

%% Constraint 2: Prerequisites
%% Selecting Set 9 requires selecting Set 0
:- selected(9), not selected(0).
%% Selecting Set 11 requires selecting Set 6
:- selected(11), not selected(6).

%% Constraint 3: Mutual Exclusion - Set 12 and Set 13 cannot be selected together
:- selected(12), selected(13).

%% Constraint 4: Category Balancing
%% If any specialized set is selected, must include at least one set from each standard category A, B, C
has_specialized :- selected(S), set_category(S, specialized).
selected_from_cat(Cat) :- selected(S), set_category(S, Cat), standard_category(Cat).
:- has_specialized, standard_category(Cat), not selected_from_cat(Cat).

%% Constraint 5: Redundancy Penalty
%% For each element covered by more than 3 sets, penalty of 2
cover_count(E, C) :- C = #count { S : selected(S), member(S, E) }, element(E).
over_covered(E) :- cover_count(E, C), C > 3.
redundancy_penalty(P) :- P = #sum { 2, E : over_covered(E) }.

%% Base cost
base_cost(C) :- C = #sum { Cost, S : selected(S), set(S, Cost, _) }.

%% Total cost
total_cost(TC) :- base_cost(BC), redundancy_penalty(RP), TC = BC + RP.

%% Objective: minimize total cost
#minimize { TC : total_cost(TC) }.

%% Output
#show selected/1.
#show base_cost/1.
#show redundancy_penalty/1.
#show total_cost/1.
#show cover_count/2.