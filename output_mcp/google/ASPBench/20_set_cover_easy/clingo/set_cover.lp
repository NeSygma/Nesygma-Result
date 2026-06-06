% Universe and Sets
universe(1..8).
set(0..5).

% Set contents
contains(0, 1). contains(0, 2). contains(0, 3).
contains(1, 2). contains(1, 4). contains(1, 5).
contains(2, 3). contains(2, 6). contains(2, 7).
contains(3, 1). contains(3, 4). contains(3, 8).
contains(4, 5). contains(4, 6). contains(4, 7). contains(4, 8).
contains(5, 1). contains(5, 2). contains(5, 6).

% Selection
{ selected(S) } :- set(S).

% Coverage
covered(E) :- selected(S), contains(S, E).

% Constraint: All elements must be covered
:- universe(E), not covered(E).

% Objective: Minimize the number of selected sets
#minimize { 1, S : selected(S) }.

% Output
total_sets(N) :- N = #count { S : selected(S) }.
#show selected/1.
#show total_sets/1.