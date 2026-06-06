% Define the puzzles
puzzle(1..6).

% Define difficulty levels for each puzzle
difficulty(1,1).  % Puzzle 1: difficulty 1 (easy)
difficulty(2,1).  % Puzzle 2: difficulty 1 (easy)
difficulty(3,2).  % Puzzle 3: difficulty 2 (medium)
difficulty(4,2).  % Puzzle 4: difficulty 2 (medium)
difficulty(5,3).  % Puzzle 5: difficulty 3 (hard)
difficulty(6,3).  % Puzzle 6: difficulty 3 (hard)

% Define prerequisites (dependencies)
% Puzzle 2 needs puzzle 1
prerequisite(1,2).
% Puzzle 3 needs puzzles 2 and 4
prerequisite(2,3).
prerequisite(4,3).
% Puzzle 4 needs puzzle 1
prerequisite(1,4).
% Puzzle 5 needs puzzle 3
prerequisite(3,5).
% Puzzle 6 needs puzzle 5
prerequisite(5,6).

% Define positions (ordering)
position(1..6).

% Each puzzle is assigned exactly one position
1 { assigned_position(P, Pos) : position(Pos) } 1 :- puzzle(P).

% No puzzle can be assigned to more than one position
:- assigned_position(P, Pos1), assigned_position(P, Pos2), Pos1 != Pos2.

% A puzzle cannot be completed before all its prerequisites are completed
:- assigned_position(P2, Pos2), assigned_position(P1, Pos1), prerequisite(P1, P2), Pos2 =< Pos1.

% Check if all dependencies are satisfied
% If there's no violated dependency, dependencies are satisfied
violated_dependency :- assigned_position(P2, Pos2), assigned_position(P1, Pos1), prerequisite(P1, P2), Pos2 =< Pos1.
dependencies_satisfied :- not violated_dependency.

% Show the solution
#show assigned_position/2.
#show difficulty/2.
#show dependencies_satisfied/0.