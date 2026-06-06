% Blocks and weights
block(a). weight(a,1).
block(b). weight(b,2).
block(c). weight(c,3).
block(d). weight(d,4).
block(e). weight(e,5).
block(f). weight(f,6).
block(g). weight(g,7).
block(h). weight(h,8).
block(i). weight(i,9).
block(j). weight(j,10).
block(k). weight(k,11).
block(l). weight(l,12).

% Locations: table or a block
location(table).
location(X) :- block(X).

% Time horizon
max_time(50).
time(0..50).

% Initial configuration at time 0
on(d,table,0). on(c,d,0). on(b,c,0). on(a,b,0).
on(h,table,0). on(g,h,0). on(f,g,0). on(e,f,0).
on(l,table,0). on(k,l,0). on(j,k,0). on(i,j,0).

% Goal locations (desired at time 50)
goal_loc(l,table).
goal_loc(i,l).
goal_loc(f,i).
goal_loc(c,f).

goal_loc(k,table).
goal_loc(h,k).
goal_loc(e,h).
goal_loc(b,e).

goal_loc(j,table).
goal_loc(g,j).
goal_loc(d,g).
goal_loc(a,d).

% Enforce goal at final time
:- on(B,Loc,50), goal_loc(B,Goal), Loc != Goal.
% Ensure each block has a goal location defined
:- block(B), not goal_loc(B,_).

% Define clear blocks at each time (a block is clear if nothing is on it)
clear(B,T) :- block(B), time(T), not on(_,B,T).

% Define moved predicate for frame axioms
moved(B,T) :- move(B,_,_,T).

% At most one move per step (0 or 1)
0 { move(B,F,To,T) : block(B), location(F), location(To), B!=F, B!=To, F!=To } 1 :- time(T), max_time(M), T < M.

% Preconditions for a move
:- move(B,_,_,T), not clear(B,T).               % block to move must be clear
:- move(B,F,_,T), not on(B,F,T).                % source must be current location
:- move(B,_,To,T), To != table, not clear(To,T). % destination must be clear if not table
% Weight constraint: heavier cannot be placed on lighter
:- move(B,_,To,T), To != table, weight(To,Wto), weight(B,Wb), Wb > Wto.

% Frame axioms: persistence of location unless moved
on(B,Loc,T+1) :- on(B,Loc,T), not moved(B,T), time(T), time(T+1).
% Effect of move
on(B,To,T+1) :- move(B,_,To,T), time(T), time(T+1).

% Table limit: at most 6 blocks on table at any time
:- #count{B : on(B,table,T)} > 6, time(T).

% Define above relation for height counting
above(Y,X,T) :- on(Y,X,T).
above(Y,X,T) :- on(Y,Z,T), above(Z,X,T).

% Height limit: no tower higher than 5 (i.e., at most 4 blocks above any block)
:- above(_,X,T), #count{Y : above(Y,X,T)} > 4, time(T).

% Ensure each block is on exactly one location at each time
:- on(B,Loc1,T), on(B,Loc2,T), Loc1 != Loc2.

% Show the moves
#show move/4.