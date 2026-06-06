% Domain
block(a; b; c).
position(table; a; b; c).

% Time steps
#const max_time = 10.
time(0..max_time).

% Initial state
on(a, table, 0).
on(b, table, 0).
on(c, a, 0).

% Helper: a block is clear if nothing is on it
clear(Block, Time) :- block(Block), time(Time), not on(_, Block, Time).

% Action: move a clear block from one position to another
{ move(Block, From, To, Time) : position(To) } :-
    block(Block),
    time(Time),
    Time < max_time,
    position(From),
    on(Block, From, Time),
    clear(Block, Time),
    To != Block,  % Cannot move onto itself
    (To == table ; clear(To, Time)).  % Target must be clear (table is always clear)

% Effect: update state
% Block is on To after move
on(Block, To, Time+1) :- move(Block, _, To, Time).

% Frame axiom: if not moved, block stays where it was
on(Block, Pos, Time+1) :- 
    on(Block, Pos, Time),
    time(Time),
    Time < max_time,
    not move(Block, _, _, Time).

% Constraint: cannot have two blocks on the same position (except table)
:- on(Block1, Pos, Time), on(Block2, Pos, Time), Block1 != Block2, Pos != table.

% Goal constraint: at final time, we must have the goal state
goal_reached(T) :- 
    on(a, b, T),
    on(b, c, T),
    on(c, table, T).

:- time(T), not goal_reached(T).

% Count the number of moves
num_moves(N) :- N = #count { Time : move(_, _, _, Time) }.

% Optimization: minimize the number of moves
#minimize { N@1 : num_moves(N) }.

% Show the plan
#show move/4.
#show num_moves/1.