% Domain definitions
row(1..5).
col(1..5).
val(1..5).

% Pre-filled cells (given constraints)
given(1,1,1).
given(2,3,3).
given(3,4,4).
given(4,5,5).
given(5,2,2).

% For cells with given values, they must have that value
grid(R,C,V) :- given(R,C,V).

% For empty cells, choose exactly one value from 1..5
{ grid(R,C,V) : val(V) } 1 :- row(R), col(C), not given(R,C,_).

% Each row must contain each value exactly once
:- row(R), val(V), #count{C : col(C), grid(R,C,V)} != 1.

% Each column must contain each value exactly once
:- col(C), val(V), #count{R : row(R), grid(R,C,V)} != 1.

% Each cell must have exactly one value (redundant but explicit)
:- row(R), col(C), #count{V : val(V), grid(R,C,V)} != 1.

% Solved indicator
solved :- grid(_,_,_).

#show grid/3.
#show solved.