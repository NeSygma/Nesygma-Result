%%% Set Cover Problem %%%

% Universe elements
element(1..8).

% Available sets: set_id, element
set_elem(0,1). set_elem(0,2). set_elem(0,3).
set_elem(1,2). set_elem(1,4). set_elem(1,5).
set_elem(2,3). set_elem(2,6). set_elem(2,7).
set_elem(3,1). set_elem(3,4). set_elem(3,8).
set_elem(4,5). set_elem(4,6). set_elem(4,7). set_elem(4,8).
set_elem(5,1). set_elem(5,2). set_elem(5,6).

% Set IDs
set_id(0..5).

% Choice: select a subset of sets
{ selected(S) } :- set_id(S).

% Constraint: every element must be covered by at least one selected set
covered(E) :- selected(S), set_elem(S, E).
:- element(E), not covered(E).

% Objective: minimize the number of selected sets
#minimize { 1,S : selected(S) }.

% Output
#show selected/1.
#show total_sets/1.
#show covered_elements/1.

% Derive output predicates
total_sets(N) :- N = #count { S : selected(S) }.
covered_elements(E) :- covered(E).