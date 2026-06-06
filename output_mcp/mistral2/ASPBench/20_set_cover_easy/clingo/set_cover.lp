% Universe elements
element(1). element(2). element(3). element(4). element(5).
element(6). element(7). element(8).

% Available sets
set(0). set(1). set(2). set(3). set(4). set(5).

% Contains relation: set(S) contains element(E)
contains(0,1). contains(0,2). contains(0,3).
contains(1,2). contains(1,4). contains(1,5).
contains(2,3). contains(2,6). contains(2,7).
contains(3,1). contains(3,4). contains(3,8).
contains(4,5). contains(4,6). contains(4,7). contains(4,8).
contains(5,1). contains(5,2). contains(5,6).

% Choice rule: select sets
{ selected(S) : set(S) }.

% Coverage constraint: every element must be covered by at least one selected set
covered(E) :- element(E), selected(S), contains(S,E).

% Ensure all elements are covered
:- element(E), not covered(E).

% Minimize the number of selected sets
#minimize { 1@1: selected(S) }.

% Output the selected sets and the total number of sets selected
#show selected/1.
#show total_selected/1.