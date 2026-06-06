%%% Data: Universe elements
elem(1..8).

%%% Data: Available sets (set_id, element)
contains(0, 1). contains(0, 2). contains(0, 3).
contains(1, 2). contains(1, 4). contains(1, 5).
contains(2, 3). contains(2, 6). contains(2, 7).
contains(3, 1). contains(3, 4). contains(3, 8).
contains(4, 5). contains(4, 6). contains(4, 7). contains(4, 8).
contains(5, 1). contains(5, 2). contains(5, 6).

%%% Set identifiers
set_id(0..5).

%%% Choice: select a subset of available sets
{ selected(S) : set_id(S) }.

%%% Constraint: every element must be covered by at least one selected set
covered(E) :- elem(E), selected(S), contains(S, E).
:- elem(E), not covered(E).

%%% Count how many sets are selected
total_sets(N) :- N = #count { S : selected(S) }.

%%% Derive the covered elements list
covered_element(E) :- covered(E).

%%% Optimize: minimize the number of selected sets
#minimize { 1@1, S : selected(S) }.

%%% Show results
#show selected_sets(S) : selected(S).
#show total_sets/1.
#show covered_elements(E) : covered_element(E).