% Domains
time(0..10). % Set a reasonable time horizon
robot(a;b;c).
row(0..4).
col(0..4).

% Directions
direction(up;down;left;right).

% Initial positions at time 0
position(a, 0, 1, 0).
position(b, 1, 1, 0).
position(c, 3, 1, 0).

% Target position
target(2, 3).

% Wall constraints (vertical walls on right side of columns)
% wall_block(FromCol, ToCol, Row) means there's a wall blocking movement from FromCol to ToCol at Row
wall_block(0, 1, R) :- row(R). % Wall blocks moving from col 0 to col 1 at all rows
wall_block(1, 2, R) :- row(R), R != 2. % Wall blocks moving from col 1 to col 2 except at row 2
wall_block(2, 3, R) :- row(R), R != 2. % Wall blocks moving from col 2 to col 3 except at row 2

% Define adjacent cells with direction
% Moving up: from (Row, Col) to (Row-1, Col)
adjacent(Row, Col, NewRow, Col, up) :-
    row(Row), col(Col),
    NewRow = Row - 1, row(NewRow).

% Moving down: from (Row, Col) to (Row+1, Col)
adjacent(Row, Col, NewRow, Col, down) :-
    row(Row), col(Col),
    NewRow = Row + 1, row(NewRow).

% Moving left: from (Row, Col) to (Row, Col-1)
adjacent(Row, Col, Row, NewCol, left) :-
    row(Row), col(Col),
    NewCol = Col - 1, col(NewCol).

% Moving right: from (Row, Col) to (Row, Col+1)
adjacent(Row, Col, Row, NewCol, right) :-
    row(Row), col(Col),
    NewCol = Col + 1, col(NewCol).

% Movement rules - each robot can move to an adjacent cell if not blocked by a wall
% A robot can choose to move or stay (frame axiom handles staying)
1 { move(Robot, NewRow, NewCol, T) :
    position(Robot, Row, Col, T-1),
    adjacent(Row, Col, NewRow, NewCol, _),
    not wall_block(Col, NewCol, Row),
    T > 0 } 1 :- robot(Robot), time(T).

% Update positions after moves
position(Robot, NewRow, NewCol, T) :- move(Robot, NewRow, NewCol, T), time(T).

% Frame axiom: if a robot doesn't move, it stays in the same position
position(Robot, Row, Col, T) :- position(Robot, Row, Col, T-1), time(T), not move(Robot, _, _, T).

% No collisions: two robots cannot be in the same cell at the same time
:- position(R1, R, C, T), position(R2, R, C, T), robot(R1), robot(R2), R1 != R2, time(T).

% Target condition: robot A must reach target position
reached_target(T) :- position(a, 2, 3, T), time(T).

% We want to find the minimum T where the target is reached
#minimize { T@1 : reached_target(T) }.

% Show the solution
#show move/4.
#show position/4.
#show reached_target/1.