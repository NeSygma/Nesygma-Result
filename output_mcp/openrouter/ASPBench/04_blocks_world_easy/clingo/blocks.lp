% Blocks and positions
block(a). block(b). block(c).
position(table).
position(X) :- block(X).

% Time horizon
max_time(5).
time(0..5) :- max_time(M), M=5.

% Initial state at time 0
on(a, table, 0).
on(b, table, 0).
on(c, a, 0).

% Define clear blocks (including table always clear)
clear(X,T) :- block(X), not on(_,X,T).
clear(table,T) :- time(T).

% Choice of move at each time step >0 (at most one move per step)
{ move(B,From,To,T) : block(B), position(From), position(To) } 1 :- time(T), T>0.
% At most one move per step
:- 2 { move(_,_,_,T) }.

% Preconditions
:- move(B,From,To,T), not clear(B,T-1).
:- move(B,From,To,T), not on(B,From,T-1).
:- move(B,From,To,T), To != table, not clear(To,T-1).
:- move(B,From,To,T), B = To.

% Effect of move
on(B,To,T) :- move(B,From,To,T).
% Persistence for blocks not moved
on(B,X,T) :- on(B,X,T-1), not move(B,_,_,T).

% Exclusivity: at most one block on a non-table support
:- on(B1,S,T), on(B2,S,T), B1 != B2, S != table.

% Goal at final time
:- not on(a,b,5).
:- not on(b,c,5).
:- not on(c,table,5).

% Define do(T) when a move occurs
 do(T) :- move(_,_,_,T).

% Minimize number of moves
#minimize { 1,T : do(T) }.

% Compute plan length
plan_length(L) :- L = #count { T : do(T) }.

#show plan_length/1.
#show move/4.