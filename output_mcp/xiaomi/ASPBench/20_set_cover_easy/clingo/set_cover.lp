% ===== DOMAIN DEFINITIONS =====

% Universe elements
element(1). element(2). element(3). element(4).
element(5). element(6). element(7). element(8).

% Available sets
set(0). set(1). set(2). set(3). set(4). set(5).

% Set membership (which elements are in which sets)
% Set 0: {1, 2, 3}
contains(0, 1). contains(0, 2). contains(0, 3).

% Set 1: {2, 4, 5}
contains(1, 2). contains(1, 4). contains(1, 5).

% Set 2: {3, 6, 7}
contains(2, 3). contains(2, 6). contains(2, 7).

% Set 3: {1, 4, 8}
contains(3, 1). contains(3, 4). contains(3, 8).

% Set 4: {5, 6, 7, 8}
contains(4, 5). contains(4, 6). contains(4, 7). contains(4, 8).

% Set 5: {1, 2, 6}
contains(5, 1). contains(5, 2). contains(5, 6).

% ===== CHOICE RULE =====
% Select or not select each set
{ selected(S) } :- set(S).

% ===== DERIVED PREDICATES =====

% An element is covered if at least one selected set contains it
covered(E) :- element(E), selected(S), contains(S, E).

% Count the number of selected sets
num_selected(N) :- N = #count { S : selected(S) }.

% ===== CONSTRAINTS =====

% All elements must be covered (every element must be in at least one selected set)
:- element(E), not covered(E).

% ===== OPTIMIZATION =====

% Minimize the number of selected sets
#minimize { 1, S : selected(S) }.

% ===== OUTPUT =====

#show selected/1.
#show num_selected/1.
#show covered/1.