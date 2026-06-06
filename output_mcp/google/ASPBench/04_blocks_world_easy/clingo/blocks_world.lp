% --- Domain ---
block(a; b; c).
position(table).
position(B) :- block(B).

% --- Time Horizon ---
#const max_time = 3.
time(0..max_time).

% --- Initial State ---
on(c, a, 0).
on(a, table, 0).
on(b, table, 0).

% --- Goal State ---
goal(a, b).
goal(b, c).
goal(c, table).

% --- State Logic ---
% A block is clear if nothing is on it
clear(B, T) :- block(B), time(T), not on(_, B, T).
clear(table, T) :- time(T).

% --- Actions ---
% Move(Block, From, To, Time)
% Choice rule: At each time T < max_time, move exactly one block
{ move(B, From, To, T) : block(B), position(From), position(To), B != To } 1 :- time(T), T < max_time.

% Preconditions
:- move(B, From, To, T), not on(B, From, T).
:- move(B, From, To, T), not clear(B, T).
:- move(B, From, To, T), To != table, not clear(To, T).
:- move(B, From, To, T), To != table, B == To.
:- move(B, From, To, T), To != table, on(B, To, T). % Cannot move onto itself

% Effects
on(B, To, T+1) :- move(B, From, To, T).
on(B, Old, T+1) :- on(B, Old, T), not move(B, Old, _, T), time(T+1).

% Frame Axioms (Persistence)
% If a block is not moved, it stays where it is
% If a block is moved, it is no longer at its old position
% (Handled by the on/3 rules above)

% --- Goal Constraint ---
:- not on(B, Target, max_time) : goal(B, Target).

% --- Optimization ---
% Minimize moves (already fixed to 3, but let's ensure it works)
#minimize { 1, B, T : move(B, _, _, T) }.

% --- Output ---
#show move/4.
#show on/3.