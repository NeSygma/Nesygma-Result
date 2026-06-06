% Recital problem

% Domains
position(1..5).
pianist(wayne); pianist(zara).
type(modern); type(traditional).

% Next positions
next(1,2). next(2,3). next(3,4). next(4,5).

% Assign pianist and type for each solo
{ pianist(P, Pos) : pianist(P) } 1 :- position(Pos).
{ type(T, Pos) : type(T) } 1 :- position(Pos).

% Constraints
% 1. Third solo is traditional
type(3, traditional).

% 2. Fifth solo is traditional (given)
type(5, traditional).

% 3. Exactly one consecutive traditional pair
consecutive_traditional(i) :- type(i, traditional), type(j, traditional), next(i,j).
:- #count{ i : consecutive_traditional(i) } != 1.

% 4. Fourth solo condition
:- type(4, traditional), pianist(4, zara).
:- type(4, modern), pianist(4, wayne).

% 5. Pianist of second solo != pianist of fifth solo
:- pianist(2, P), pianist(5, P).

% 6. No traditional piece until Wayne performs at least one modern piece
modern_wayne(i) :- pianist(i, wayne), type(i, modern).
:- type(i, traditional), #count{ j : modern_wayne(j), j < i } = 0.

% Show assignments
#show pianist/2.
#show type/2.