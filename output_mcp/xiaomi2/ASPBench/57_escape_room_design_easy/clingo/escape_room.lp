% ============================================
% Escape Room Puzzle Ordering - ASP Model
% ============================================

% --- Domain: Puzzles ---
puzzle(1). puzzle(2). puzzle(3). puzzle(4). puzzle(5). puzzle(6).

% --- Domain: Positions (1..6) ---
pos(1). pos(2). pos(3). pos(4). pos(5). pos(6).

% --- Domain: Difficulty Levels ---
difficulty_level(1). difficulty_level(2). difficulty_level(3).

% --- Puzzle Data: Difficulty ---
difficulty(1, 1).  % Puzzle 1: easy
difficulty(2, 1).  % Puzzle 2: easy
difficulty(3, 2).  % Puzzle 3: medium
difficulty(4, 2).  % Puzzle 4: medium
difficulty(5, 3).  % Puzzle 5: hard
difficulty(6, 3).  % Puzzle 6: hard

% --- Puzzle Data: Prerequisites ---
% prereq(Puzzle, Prerequisite) means Prerequisite must be completed before Puzzle
prereq(2, 1).   % Puzzle 2 needs Puzzle 1
prereq(3, 2).   % Puzzle 3 needs Puzzle 2
prereq(3, 4).   % Puzzle 3 needs Puzzle 4
prereq(4, 1).   % Puzzle 4 needs Puzzle 1
prereq(5, 3).   % Puzzle 5 needs Puzzle 3
prereq(6, 5).   % Puzzle 6 needs Puzzle 5

% ============================================
% Decision Variables
% ============================================

% Assign each puzzle to exactly one position
1 { position(P, S) : pos(S) } 1 :- puzzle(P).

% Each position has exactly one puzzle
1 { position(P, S) : puzzle(P) } 1 :- pos(S).

% ============================================
% Constraint 1: Dependencies must be satisfied
% If Q is a prerequisite for P, then Q must come before P
% ============================================
:- prereq(P, Q), position(P, Sp), position(Q, Sq), Sp <= Sq.

% ============================================
% Derived: Check if all dependencies are satisfied
% (In any valid answer set, they will be by construction)
% ============================================
dep_satisfied(P, Q) :- prereq(P, Q), position(P, Sp), position(Q, Sq), Sq < Sp.
all_deps_satisfied :- puzzle(P), prereq(P, Q), dep_satisfied(P, Q).
all_deps_satisfied :- puzzle(P), not has_prereq(P).
has_prereq(P) :- prereq(P, _).

% ============================================
% Derived: Difficulty progression
% ============================================
diff_at_pos(S, D) :- position(P, S), difficulty(P, D).

% ============================================
% Output: Puzzle ordering
% ============================================
puzzle_order(S, P) :- position(P, S).

% ============================================
% Output: Difficulty progression
% ============================================
difficulty_progression(S, D) :- diff_at_pos(S, D).

% ============================================
% Output: Puzzle details
% ============================================
puzzle_details(P, D, Q) :- prereq(P, Q), difficulty(P, D).

% ============================================
% Show directives
% ============================================
#show puzzle_order/2.
#show difficulty_progression/2.
#show all_deps_satisfied/0.
#show puzzle_details/3.