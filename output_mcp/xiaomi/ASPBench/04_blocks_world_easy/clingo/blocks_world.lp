% Blocks World Planning Problem
% Find shortest sequence of moves from initial to goal state

% ============ DOMAIN ============
block(a). block(b). block(c).
position(P) :- block(P).
position(table).

% Time horizon (we'll find optimal within this bound)
time(0..10).

% ============ INITIAL STATE ============
on(a, table, 0).
on(b, table, 0).
on(c, a, 0).

% ============ GOAL STATE ============
goal_on(a, b).
goal_on(b, c).
goal_on(c, table).

% ============ ACTIONS ============
% Choice rule: at each time step, we can move one clear block to another position
{ move(B, From, To, T) : block(B), position(From), position(To), From != To } 1 :- time(T), T > 0.

% ============ PRECONDITIONS ============
% A block can only be moved if it's clear (nothing on top)
:- move(B, _, _, T), block(OnTop), on(OnTop, B, T).

% A block can only be moved from its current position
:- move(B, From, _, T), not on(B, From, T).

% A block cannot be moved to itself
:- move(B, _, B, T).

% A block can only be placed on a clear block or table
:- move(B, _, To, T), To != table, not clear(To, T).

% ============ EFFECTS (State Change) ============
% After moving B from From to To:
% - B is now on To
on(B, To, T) :- move(B, _, To, T), time(T), T > 0.

% - B is no longer on From (handled by frame axiom below)

% ============ FRAME AXIOMS (Persistence) ============
% A block stays in its position unless moved
on(B, P, T) :- on(B, P, T-1), time(T), T > 0, not move(B, P, _, T).

% ============ DERIVED PREDICATES ============
% A block is clear if nothing is on top of it
clear(B, T) :- block(B), time(T), not block(OnTop), on(OnTop, B, T).

% ============ GOAL CONSTRAINT ============
% At the final time step, all goal conditions must be satisfied
:- goal_on(B, P), time(T), not on(B, P, T), 
   #count{ T2 : time(T2), T2 > T, move(_, _, _, T2) } = 0.

% ============ OPTIMIZATION ============
% Minimize the number of moves
#minimize { 1, B, From, To, T : move(B, From, To, T) }.

% ============ SYMMETRY BREAKING ============
% Don't move a block and then immediately move it back
:- move(B, From1, To1, T), move(B, From2, To2, T+1), From1 == To2, To1 == From2.

% ============ OUTPUT ============
#show move/4.