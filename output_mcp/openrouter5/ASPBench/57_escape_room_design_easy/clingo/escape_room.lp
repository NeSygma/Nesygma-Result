%%% Domain Facts %%%

% Puzzles 1-6
puzzle(1..6).

% Difficulty levels
difficulty(1;2;3).

% Puzzle difficulties
puzzle_difficulty(1,1).
puzzle_difficulty(2,1).
puzzle_difficulty(3,2).
puzzle_difficulty(4,2).
puzzle_difficulty(5,3).
puzzle_difficulty(6,3).

% Prerequisites: prereq(PrereqPuzzle, Puzzle)
prereq(1,2).
prereq(2,3).
prereq(4,3).
prereq(1,4).
prereq(3,5).
prereq(5,6).

%%% Generate a permutation (ordering) of the 6 puzzles %%%

% Each position 1..6 gets exactly one puzzle
1 { order(Pos, P) : puzzle(P) } 1 :- Pos = 1..6.

% Each puzzle appears exactly once
1 { order(Pos, P) : Pos = 1..6 } 1 :- puzzle(P).

%%% Constraint: Prerequisites must come before the puzzle %%%

% If puzzle P has prerequisite Q, then Q must be at an earlier position than P
:- prereq(Q, P), order(PosQ, Q), order(PosP, P), PosQ >= PosP.

%%% Derived predicates for output %%%

% Position of each puzzle
pos(P, Pos) :- order(Pos, P).

% Difficulty progression: difficulty at each position
difficulty_at_pos(Pos, D) :- order(Pos, P), puzzle_difficulty(P, D).

% Dependencies satisfied: check that for every prereq, the prereq position < puzzle position
dependencies_satisfied :- 
    #count { Q,P : prereq(Q,P), pos(Q,PosQ), pos(P,PosP), PosQ < PosP } = N,
    #count { Q,P : prereq(Q,P) } = N.

% Puzzle details
puzzle_detail(P, D, Qs) :- 
    puzzle(P), 
    puzzle_difficulty(P, D),
    Qs = #count { Q : prereq(Q,P) }.

%%% Show output %%%

#show order/2.
#show difficulty_at_pos/2.
#show dependencies_satisfied/1.
#show puzzle_detail/3.