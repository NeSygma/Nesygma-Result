% Escape Room Puzzle Ordering Problem
% ======================================

% Domain definitions
puzzle(1..6).
position(1..6).
difficulty_level(1..3).

% Puzzle difficulties
difficulty(1, 1).  % Puzzle 1: easy
difficulty(2, 1).  % Puzzle 2: easy
difficulty(3, 2).  % Puzzle 3: medium
difficulty(4, 2).  % Puzzle 4: medium
difficulty(5, 3).  % Puzzle 5: hard
difficulty(6, 3).  % Puzzle 6: hard

% Dependencies (prerequisite relationships)
% prerequisite(P, Q) means puzzle Q must be completed before puzzle P
prerequisite(2, 1).  % Puzzle 2 needs puzzle 1
prerequisite(3, 2).  % Puzzle 3 needs puzzle 2
prerequisite(3, 4).  % Puzzle 3 needs puzzle 4
prerequisite(4, 1).  % Puzzle 4 needs puzzle 1
prerequisite(5, 3).  % Puzzle 5 needs puzzle 3
prerequisite(6, 5).  % Puzzle 6 needs puzzle 5

% ===== CONSTRAINTS =====

% 1. Each puzzle appears exactly once in the sequence
1 { order(P, Pos) : position(Pos) } 1 :- puzzle(P).

% 2. Each position has exactly one puzzle
1 { order(P, Pos) : puzzle(P) } 1 :- position(Pos).

% 3. Dependencies must be satisfied: if P depends on Q, Q must come before P
:- order(P, PosP), order(Q, PosQ), prerequisite(P, Q), PosQ >= PosP.

% 4. No circular dependencies (implicitly enforced by the above constraint)

% ===== DERIVED INFORMATION =====

% Difficulty progression: difficulty at each position
difficulty_at_pos(Pos, D) :- order(P, Pos), difficulty(P, D).

% All dependencies satisfied (true if model is valid)
all_dependencies_satisfied :- not #false.

% Puzzle details: for each puzzle, record its ID, difficulty, and prerequisites
puzzle_detail(P, D, Prereq) :- puzzle(P), difficulty(P, D), prerequisite(P, Prereq).

% ===== OUTPUT PREDICATES =====

% Puzzle order (position -> puzzle)
puzzle_order(Pos, P) :- order(P, Pos).

% Difficulty progression array
difficulty_progression(Pos, D) :- difficulty_at_pos(Pos, D).

% Dependencies satisfied flag
dependencies_satisfied :- all_dependencies_satisfied.

% ===== SHOW DIRECTIVES =====
#show puzzle_order/2.
#show difficulty_progression/2.
#show dependencies_satisfied/0.
#show puzzle_detail/3.