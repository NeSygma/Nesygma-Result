%%% Escape Room Puzzle Ordering %%%

%%% Domain Facts %%%
% Puzzles with their difficulty levels
puzzle(1, 1).  % puzzle 1, difficulty 1
puzzle(2, 1).  % puzzle 2, difficulty 1
puzzle(3, 2).  % puzzle 3, difficulty 2
puzzle(4, 2).  % puzzle 4, difficulty 2
puzzle(5, 3).  % puzzle 5, difficulty 3
puzzle(6, 3).  % puzzle 6, difficulty 3

% Prerequisites: prereq(Prereq, Puzzle) means Prereq must be completed before Puzzle
prereq(1, 2).     % puzzle 2 needs puzzle 1
prereq(2, 3).     % puzzle 3 needs puzzle 2
prereq(4, 3).     % puzzle 3 needs puzzle 4
prereq(1, 4).     % puzzle 4 needs puzzle 1
prereq(3, 5).     % puzzle 5 needs puzzle 3
prereq(5, 6).     % puzzle 6 needs puzzle 5

%%% Domain %%%
position(1..6).
puzzle_id(1..6).

%%% Choice: assign each puzzle to exactly one position %%%
1 { order(P, Pos) : position(Pos) } 1 :- puzzle_id(P).
1 { order(P, Pos) : puzzle_id(P) } 1 :- position(Pos).

%%% Constraint: all dependencies must be satisfied %%%
% If puzzle A is a prerequisite of puzzle B, then A must come before B
:- prereq(A, B), order(A, PosA), order(B, PosB), PosA >= PosB.

%%% Derived predicates for output %%%

% Puzzle at each position
puzzle_at(Pos, P) :- order(P, Pos).

% Difficulty at each position
difficulty_at(Pos, D) :- puzzle_at(Pos, P), puzzle(P, D).

% Dependencies satisfied check
dependencies_satisfied :- #count { A, B : prereq(A, B), order(A, PosA), order(B, PosB), PosA >= PosB } = 0.

%%% Show output in required format %%%
#show puzzle_at/2.
#show difficulty_at/2.
#show dependencies_satisfied/0.

% Puzzle details helper
puzzle_details(P, D, PrereqSet) :- puzzle(P, D), PrereqSet = #count { R : prereq(R, P) }.
#show puzzle_details/3.