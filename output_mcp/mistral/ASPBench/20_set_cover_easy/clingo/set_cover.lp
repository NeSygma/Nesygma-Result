% Universe of elements
 element(1..8).

% Available sets
 set(0..5).

% Elements contained in each set
 contains(0,1). contains(0,2). contains(0,3).
 contains(1,2). contains(1,4). contains(1,5).
 contains(2,3). contains(2,6). contains(2,7).
 contains(3,1). contains(3,4). contains(3,8).
 contains(4,5). contains(4,6). contains(4,7). contains(4,8).
 contains(5,1). contains(5,2). contains(5,6).

% Choice rule: select sets
{selected(Set) : set(Set)}.

% Ensure all elements are covered by at least one selected set
covered(E) :- element(E), selected(S), contains(S,E).
:- element(E), not covered(E).

% Minimize the number of selected sets
#minimize { 1@1, Set : selected(Set) }.

% Show selected sets and covered elements
#show selected/1.
#show covered/1.