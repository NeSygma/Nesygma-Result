% Blocks World Planning

% Blocks
block(a). block(b). block(c).

% Positions: table and blocks
position(table).
position(P) :- block(P).

% Time horizon (0 to 5)
time(0..5).

% On relation: exactly one position per block per time
1 { on(B, P, T) : position(P) } 1 :- block(B), time(T).

% Clear: block is clear if nothing is on top of it
clear(B, T) :- block(B), time(T), not on(_, B, T).

% Move action: at most one move per time step
{ move(B, From, To, T) : position(To), To != B, on(B, From, T), clear(B, T) } 0..1 :- time(T).

% Frame axioms for on - state persists unless changed
on(B, P, T+1) :- on(B, P, T), time(T), time(T+1), not move(B, _, _, T).
on(B, To, T+1) :- move(B, From, To, T), time(T), time(T+1).

% Constraint: at most one block on top of another
:- on(Y1, X, T), on(Y2, X, T), Y1 != Y2, block(X), time(T).

% Initial state
on(a, table, 0).
on(b, table, 0).
on(c, a, 0).

% Goal state: must be reached at some time T
goal(T) :- on(a, b, T), on(b, c, T), on(c, table, T), time(T).

% Constraint: goal must be reached by the end of the horizon
:- not goal(5).

% Minimize number of moves
#minimize { 1, B, From, To, T : move(B, From, To, T) }.

% Compute plan length
plan_length(L) :- L = #count { B, From, To, T : move(B, From, To, T) }.

% Output plan length
#show plan_length/1.

% Output actions: for each move, output step, action, block, from, to
step(T+1) :- move(_, _, _, T).
action(T+1, "move") :- move(_, _, _, T).
block(T+1, B) :- move(B, _, _, T).
from(T+1, From) :- move(_, From, _, T).
to(T+1, To) :- move(_, _, To, T).

#show step/1.
#show action/2.
#show block/2.
#show from/2.
#show to/2.