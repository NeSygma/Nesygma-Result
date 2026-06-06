% Universe elements
element(1..8).

% Sets and their elements
set(0). set(1). set(2). set(3). set(4). set(5).

set_contents(0,1). set_contents(0,2). set_contents(0,3).
set_contents(1,2). set_contents(1,4). set_contents(1,5).
set_contents(2,3). set_contents(2,6). set_contents(2,7).
set_contents(3,1). set_contents(3,4). set_contents(3,8).
set_contents(4,5). set_contents(4,6). set_contents(4,7). set_contents(4,8).
set_contents(5,1). set_contents(5,2). set_contents(5,6).

% Choice of sets
{selected(S)} :- set(S).

% Coverage definition
covered(E) :- selected(S), set_contents(S,E).

% Every element must be covered
:- element(E), not covered(E).

% Optimization: minimize number of selected sets
#minimize { 1,S : selected(S) }.

% Compute total number of selected sets
total(N) :- N = #count{S : selected(S)}.

#show selected/1.
#show covered/1.
#show total/1.