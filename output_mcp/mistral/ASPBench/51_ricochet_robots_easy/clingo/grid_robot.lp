% Grid size
row(0..3).
col(0..3).

% Robots
robot(a; b).

% Walls: vertical wall between col 1 and 2 for rows 0-1
% Represented as: cannot move from (Row,1) to (Row,2) or (Row,2) to (Row,1) for Row=0,1
invalid_move(Row, 1, 2) :- row(Row), Row = 0..1.
invalid_move(Row, 2, 1) :- row(Row), Row = 0..1.

% Time horizon (0 to max_time)
max_time(5).
time(0..T) :- max_time(T).

% Initial positions
position(a, 0, 0, 1).
position(b, 0, 1, 1).

% Possible moves (cardinal directions)
direction(up; down; left; right).

% Helper predicate: new position based on direction
% up: row decreases by 1
new_pos(R, T, FromRow, FromCol, ToRow, ToCol) :-
    move(R, T, FromRow, FromCol, ToRow, ToCol),
    direction(down),
    ToRow = FromRow + 1,
    ToCol = FromCol.

new_pos(R, T, FromRow, FromCol, ToRow, ToCol) :-
    move(R, T, FromRow, FromCol, ToRow, ToCol),
    direction(up),
    ToRow = FromRow - 1,
    ToCol = FromCol.

new_pos(R, T, FromRow, FromCol, ToRow, ToCol) :-
    move(R, T, FromRow, FromCol, ToRow, ToCol),
    direction(right),
    ToRow = FromRow,
    ToCol = FromCol + 1.

new_pos(R, T, FromRow, FromCol, ToRow, ToCol) :-
    move(R, T, FromRow, FromCol, ToRow, ToCol),
    direction(left),
    ToRow = FromRow,
    ToCol = FromCol - 1.

% Ensure new positions are within grid bounds
valid_move(R, T, FromRow, FromCol, ToRow, ToCol) :-
    new_pos(R, T, FromRow, FromCol, ToRow, ToCol),
    0 <= ToRow, ToRow <= 3,
    0 <= ToCol, ToCol <= 3.

% Choice rule: robots can move in any valid direction or stay (implicitly by not moving)
{ move(R, T, FromRow, FromCol, ToRow, ToCol) : 
    robot(R), 
    time(T), 
    T > 0,
    position(R, T-1, FromRow, FromCol),
    valid_move(R, T, FromRow, FromCol, ToRow, ToCol)
} 1 :- robot(R), time(T), T > 0.

% Frame axiom: if no move is made, position stays the same
position(R, T, Row, Col) :- 
    robot(R), 
    time(T), 
    T > 0,
    position(R, T-1, Row, Col),
    not move(R, T, Row, Col, _, _).

% Effect: update position if move is made
position(R, T, ToRow, ToCol) :- 
    move(R, T, FromRow, FromCol, ToRow, ToCol),
    robot(R), 
    time(T).

% No collisions: two robots cannot be in the same position at the same time
:- position(R1, T, Row, Col), position(R2, T, Row, Col), R1 != R2, time(T).

% Wall constraint: cannot move through walls
:- move(R, T, FromRow, FromCol, ToRow, ToCol),
   invalid_move(FromRow, FromCol, ToCol),
   time(T).

% Goal: Robot A must reach (2,1) at some time T
:- not position(a, T, 2, 1), time(T).

% Count the number of moves
num_moves(M) :- M = #count { move(R, T, _, _, _, _) : robot(R), time(T) }.

% Optimization: minimize the number of moves
#minimize { M : num_moves(M) }.

% Output predicates
solution_found :- position(a, T, 2, 1), time(T).

% Helper to extract move sequence
move_sequence(R, T, FromRow, FromCol, ToRow, ToCol) :- 
    move(R, T, FromRow, FromCol, ToRow, ToCol).

% Final positions
final_position(R, Row, Col) :- position(R, T, Row, Col), time(T), not move(_, T+1, _, _, _, _).

% Show directives
#show solution_found/0.
#show num_moves/1.
#show move_sequence/6.
#show final_position/3.