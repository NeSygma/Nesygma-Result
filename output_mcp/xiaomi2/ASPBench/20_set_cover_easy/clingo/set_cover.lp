% === Domain ===
element(1). element(2). element(3). element(4).
element(5). element(6). element(7). element(8).

set(0). set(1). set(2). set(3). set(4). set(5).

% === Set membership (which elements belong to which set) ===
in(0,1). in(0,2). in(0,3).
in(1,2). in(1,4). in(1,5).
in(2,3). in(2,6). in(2,7).
in(3,1). in(3,4). in(3,8).
in(4,5). in(4,6). in(4,7). in(4,8).
in(5,1). in(5,2). in(5,6).

% === Choice: select sets ===
{ selected(S) } :- set(S).

% === Constraint: every element must be covered by at least one selected set ===
:- element(E), not covered(E).

covered(E) :- element(E), selected(S), in(S, E).

% === Objective: minimize number of selected sets ===
#minimize { 1,S : selected(S) }.

% === Output ===
#show selected/1.