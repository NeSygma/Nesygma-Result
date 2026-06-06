% Grid puzzle: Two robots moving on a 4x4 grid with walls.

% Domain definitions
rows(0..3).
cols(0..3).
cell(R,C) :- rows(R), cols(C).

% Walls: cells (0,2) and (1,2) are walls
wall(0,2).
wall(1,2).

% Robots
robot(a).
robot(b).

% Initial positions at time 0
at(0,1,a,0).
at(1,1,b,0).

% Target position for robot a
target(2,1).

% Time horizon: enough for optimal solution (minimum 3 moves)
time(0..5).

% Directions: up, down, left, right
direction(-1,0). % up
direction(1,0).  % down
direction(0,-1). % left
direction(0,1).  % right

% Occupied cells at time T
occupied(R,C,T) :- at(R,C,_,T).

% Possible moves based on current positions
possible_move(T,Robot,R,C,ToR,ToC) :-
    time(T), time(T+1),
    robot(Robot),
    at(R,C,Robot,T),
    direction(dr,dc),
    ToR = R + dr,
    ToC = C + dc,
    cell(ToR,ToC),
    not wall(ToR,ToC),
    not occupied(ToR,ToC,T).

% Choice rule: at each time step, at most one move can be selected
{ move(T,Robot,R,C,ToR,ToC) : possible_move(T,Robot,R,C,ToR,ToC) } 0..1 :- time(T), time(T+1).

% Frame axioms: positions at time T+1
% If a robot moves, its position changes to the destination
at(ToR,ToC,Robot,T+1) :- move(T,Robot,_,_,ToR,ToC), at(_,_,Robot,T), time(T+1).
% If a robot does not move, its position persists
at(R,C,Robot,T+1) :- at(R,C,Robot,T), not move(T,Robot,_,_,_,_), time(T+1).

% Each robot has exactly one position at each time
1 { at(R,C,Robot,T) : cell(R,C) } 1 :- robot(Robot), time(T).

% No two robots occupy the same cell at the same time
:- at(R,C,Robot1,T), at(R,C,Robot2,T), Robot1 != Robot2.

% Goal: robot a reaches target
goal_reached(T) :- at(2,1,a,T).

% After goal is reached, no more moves allowed
:- goal_reached(T), move(t,_,_,_,_,_), t > T.

% Solution found if goal is reached at some time
solution_found :- goal_reached(_).

% Total number of moves
moves(N) :- N = #count{ T,Robot,R,C,ToR,ToC : move(T,Robot,R,C,ToR,ToC) }.

% Final positions: at the last time step (time 5) if goal is reached by then
% We output positions at time 5, assuming no moves after goal.
final_pos(Robot,R,C) :- at(R,C,Robot,5), goal_reached(_).

% Show directives
#show solution_found/0.
#show moves/1.
#show move/6.
#show final_pos/3.

% Minimize the number of moves
#minimize { 1,T,Robot,R,C,ToR,ToC : move(T,Robot,R,C,ToR,ToC) }.