% --- Blocks World Planning ---

% Domain
block(a; b; c).
location(a; b; c; table).

% Time horizon (sufficient for optimal plan of 3 moves)
#const max_time = 5.
time(0..max_time).

% --- Initial State (time 0) ---
on(a, table, 0).
on(b, table, 0).
on(c, a, 0).

% --- Goal State ---
goal_on(a, b).
goal_on(b, c).
goal_on(c, table).

% --- Action Generation ---
% At each step S (1..max_time), optionally move at most one block to a location
{ move(Block, To, S) : block(Block), location(To), To != Block } 1 :- time(S), S > 0.

% --- Preconditions ---

% A block is clear if no other block is on top of it
clear(Block, T) :- block(Block), time(T), not on(_, Block, T).

% A moved block must be clear at the previous time
:- move(Block, To, S), not clear(Block, S-1).

% If the target is a block, it must be clear at the previous time
:- move(Block, Target, S), block(Target), not clear(Target, S-1).

% --- Effects ---
% After moving Block to To at step S, it is on To at time S
on(Block, To, S) :- move(Block, To, S).

% --- Frame Axioms (Persistence) ---
% If Block was on Loc at S-1 and not moved at S, it stays on Loc at S
on(Block, Loc, S) :- on(Block, Loc, S-1), time(S), S > 0, not moved(Block, S).
moved(Block, S) :- move(Block, _, S).

% --- State Constraints ---
% A block can only be in one place at a time
:- on(Block, Loc1, S), on(Block, Loc2, S), Loc1 != Loc2.

% At most one block can be on top of another block (except table)
:- on(X, Y, S), on(Z, Y, S), X != Z, block(Y).

% No block can be on itself
:- on(Block, Block, S).

% --- Goal Achievement ---
% All goal conditions must hold at the final time
:- goal_on(Block, Loc), not on(Block, Loc, max_time).

% --- Optimization ---
% Minimize total number of moves
#minimize { 1, S : move(_, _, S) }.

% --- Output Derivation ---

% Derive the source location for each move
from(Block, Loc, S) :- move(Block, _, S), on(Block, Loc, S-1).

% Aggregate into plan_step for clean output
plan_step(S, Block, From, To) :- move(Block, To, S), from(Block, From, S).

% Compute plan length
plan_length(N) :- N = #count { S : move(_, _, S) }.

% Show results
#show plan_length/1.
#show plan_step/4.