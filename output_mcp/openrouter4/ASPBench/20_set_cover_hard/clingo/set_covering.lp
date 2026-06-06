% Universe elements
element(1..20).

% Sets
set(0..13).

% Elements covered by each set
covers(0,1). covers(0,2). covers(0,3). covers(0,4). covers(0,5).
covers(1,1). covers(1,6). covers(1,11). covers(1,16).
covers(2,2). covers(2,7). covers(2,12). covers(2,17).
covers(3,3). covers(3,8). covers(3,13). covers(3,18).
covers(4,4). covers(4,9). covers(4,14). covers(4,19).
covers(5,5). covers(5,10). covers(5,15). covers(5,20).
covers(6,6). covers(6,7). covers(6,8). covers(6,9). covers(6,10).
covers(7,1). covers(7,3). covers(7,5). covers(7,7). covers(7,9).
covers(8,2). covers(8,4). covers(8,6). covers(8,8). covers(8,10).
covers(9,1). covers(9,2). covers(9,3). covers(9,4). covers(9,5). covers(9,6). covers(9,7).
covers(10,11). covers(10,12). covers(10,13). covers(10,14). covers(10,15).
covers(11,8). covers(11,9). covers(11,10).
covers(12,1). covers(12,5). covers(12,10). covers(12,15).
covers(13,16). covers(13,17). covers(13,18). covers(13,19). covers(13,20).

% Costs
cost(0,1). cost(1,1). cost(2,1). cost(3,1). cost(4,1). cost(5,1). cost(6,1). cost(7,1). cost(8,1).
cost(9,4). cost(10,4). cost(11,4). cost(12,4). cost(13,4).

% Categories (standard sets)
category(0,a). category(1,a). category(2,a).
category(3,b). category(4,b). category(5,b).
category(6,c). category(7,c). category(8,c).

% Specialized sets (cost > 1)
specialized(9). specialized(10). specialized(11). specialized(12). specialized(13).

% Decision: select a set
{ selected(S) } :- set(S).

% Constraint 1: Full Coverage - every element covered by at least one selected set
covered(E) :- selected(S), covers(S,E).
:- element(E), not covered(E).

% Constraint 2: Prerequisites
:- selected(9), not selected(0).
:- selected(11), not selected(6).

% Constraint 3: Mutual exclusion
:- selected(12), selected(13).

% Constraint 4: Category Balancing
% If any specialized set is selected, must include at least one set from each standard category
any_specialized :- selected(S), specialized(S).
:- any_specialized, { selected(S) : category(S,a) } = 0.
:- any_specialized, { selected(S) : category(S,b) } = 0.
:- any_specialized, { selected(S) : category(S,c) } = 0.

% Constraint 5: Redundancy Penalty
% Count how many selected sets cover each element
element_coverage(E, N) :- N = #count { S : selected(S), covers(S,E) }, element(E).

% Penalty: for each element covered by more than 3 sets, penalty of 2
penalty_element(E) :- element_coverage(E, N), N > 3.
total_penalty(P) :- P = #sum { 2, E : penalty_element(E) }.

% Base cost calculation
total_base_cost(C) :- C = #sum { Cost, S : selected(S), cost(S,Cost) }.

% Total cost
total_cost(TC) :- total_base_cost(BC), total_penalty(P), TC = BC + P.

% Minimize total cost
#minimize { TC : total_cost(TC) }.

% Show results
#show selected/1.
#show total_base_cost/1.
#show total_penalty/1.
#show total_cost/1.