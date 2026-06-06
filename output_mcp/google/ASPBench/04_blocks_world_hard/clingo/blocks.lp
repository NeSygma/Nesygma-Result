% Blocks and Weights
block(a;b;c;d;e;f;g;h;i;j;k;l).
weight(a,1; b,2; c,3; d,4; e,5; f,6; g,7; h,8; i,9; j,10; k,11; l,12).

% Time horizon
#const max_time = 50.
time(0..max_time).

% Initial Configuration
on(a,b,0). on(b,c,0). on(c,d,0). on(d,table,0).
on(e,f,0). on(f,g,0). on(g,h,0). on(h,table,0).
on(i,j,0). on(j,k,0). on(k,l,0). on(l,table,0).

% Goal Configuration
goal(c,f). goal(f,i). goal(i,l). goal(l,table).
goal(b,e). goal(e,h). goal(h,k). goal(k,table).
goal(a,d). goal(d,g). goal(g,j). goal(j,table).

% Clear block definition
clear(B, T) :- block(B), not on(_, B, T).
clear(table, T).

% Height definition
height(table, 0, T) :- time(T).
height(B, H+1, T) :- on(B, S, T), height(S, H, T).

% Move action
{ move(B, From, To, T) : block(B), on(B, From, T), clear(B, T), To != From, To != B, (To == table ; clear(To, T)) } 1 :- T < max_time.

% Constraints
% 1. Weight constraint: Heavier block cannot be on lighter block
:- move(B, _, To, T), To != table, weight(B, W1), weight(To, W2), W1 > W2.
:- on(B, S, T), S != table, weight(B, W1), weight(S, W2), W1 > W2.

% 2. Table limit: At most 6 blocks on table
:- time(T), #count { B : on(B, table, T) } > 6.

% 3. Height limit: No tower may exceed height 5
:- move(B, _, To, T), To != table, height(To, H, T), H >= 5.

% State transitions
on(B, To, T+1) :- move(B, From, To, T).
on(B, S, T+1) :- on(B, S, T), not move(B, S, _, T), not move(B, _, _, T).

% Goal condition
goal_met(T) :- T <= max_time, #count { B, S : on(B, S, T), goal(B, S) } = 12.
:- not goal_met(max_time).

% Optimization: Minimize moves
#minimize { 1, B, T : move(B, _, _, T) }.

#show move/4.