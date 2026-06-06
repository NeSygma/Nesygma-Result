% Puzzles
puzzle(1). puzzle(2). puzzle(3). puzzle(4). puzzle(5). puzzle(6).

% Difficulty
difficulty(1,1). difficulty(2,1). difficulty(3,2). difficulty(4,2). difficulty(5,3). difficulty(6,3).

% Prerequisites
prereq(2,1). prereq(3,2). prereq(3,4). prereq(4,1). prereq(5,3). prereq(6,5).

% Positions
pos_range(1). pos_range(2). pos_range(3). pos_range(4). pos_range(5). pos_range(6).

% Each position has exactly one puzzle
1 { pos(P, Pos) : puzzle(P) } 1 :- pos_range(Pos).

% Each puzzle has exactly one position
1 { pos(P, Pos) : pos_range(Pos) } 1 :- puzzle(P).

% Dependency constraints: prereq must come before
:- prereq(P, Q), pos(P, PosP), pos(Q, PosQ), PosQ >= PosP.

% Define order
order(Pos, P) :- pos(P, Pos).

% Difficulty progression
difficulty_progression(Pos, D) :- order(Pos, P), difficulty(P, D).

% Puzzle details
puzzle_detail(P, D) :- puzzle(P), difficulty(P, D).

% Dependencies satisfied
dependencies_satisfied.

#show order/2.
#show difficulty_progression/2.
#show puzzle_detail/2.
#show prereq/2.
#show dependencies_satisfied.