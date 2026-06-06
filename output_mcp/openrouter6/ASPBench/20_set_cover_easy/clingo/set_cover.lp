% Set Cover Problem

% Universe elements
element(1..8).

% Available sets
set(0). set(1). set(2). set(3). set(4). set(5).

% Elements in each set
contains(0,1). contains(0,2). contains(0,3).
contains(1,2). contains(1,4). contains(1,5).
contains(2,3). contains(2,6). contains(2,7).
contains(3,1). contains(3,4). contains(3,8).
contains(4,5). contains(4,6). contains(4,7). contains(4,8).
contains(5,1). contains(5,2). contains(5,6).

% Choice rule: select any subset of sets
{selected(S)} :- set(S).

% Coverage: each element must be covered by at least one selected set
selected_set_contains(E) :- selected(S), contains(S,E).
:- element(E), not selected_set_contains(E).

% Minimize the number of selected sets
#minimize { 1,S : selected(S) }.

% Output selected sets as an array (list of indices)
selected_set(S) :- selected(S).

% Total number of selected sets
total_sets(N) :- N = #count{ S : selected_set(S) }.

% Covered elements (all elements in universe)
covered_element(E) :- element(E).

% Show relevant predicates
#show selected_set/1.
#show total_sets/1.
#show covered_element/1.