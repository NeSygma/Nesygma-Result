% Escape Room Puzzle Ordering Problem

% Domain declarations
puzzle(1..6).
position(1..6).
difficulty_level(1..3).

% Instance data: puzzle difficulties
difficulty(1, 1).  % Puzzle 1: easy
difficulty(2, 1).  % Puzzle 2: easy
difficulty(3, 2).  % Puzzle 3: medium
difficulty(4, 2).  % Puzzle 4: medium
difficulty(5, 3).  % Puzzle 5: hard
difficulty(6, 3).  % Puzzle 6: hard

% Instance data: prerequisites (dependencies)
% prerequisite(P, Q) means Q must be completed before P
prerequisite(2, 1).  % Puzzle 2 needs puzzle 1
prerequisite(3, 2).  % Puzzle 3 needs puzzle 2
prerequisite(3, 4).  % Puzzle 3 needs puzzle 4
prerequisite(4, 1).  % Puzzle 4 needs puzzle 1
prerequisite(5, 3).  % Puzzle 5 needs puzzle 3
prerequisite(6, 5).  % Puzzle 6 needs puzzle 5

% Choice rule: assign each puzzle to exactly one position
{ position(P, N) : position(N) } = 1 :- puzzle(P).

% Constraint: each position has exactly one puzzle
{ position(P, N) : puzzle(P) } = 1 :- position(N).

% Constraint: no two puzzles at same position
:- position(P1, N), position(P2, N), P1 != P2.

% Constraint: no puzzle at multiple positions
:- position(P, N1), position(P, N2), N1 != N2.

% Helper: order(N, P) means puzzle P is at position N
order(N, P) :- position(P, N).

% Topological ordering constraint: if P depends on Q, then Q must come before P
:- position(P, Np), position(Q, Nq), prerequisite(P, Q), Np <= Nq.

% Sentinel atom to ensure non-empty answer set
solution_exists :- puzzle(_).

% Show directives for output
#show position/2.
#show order/2.
#show solution_exists/0.

% Additional output for clarity
#show puzzle(P) : puzzle(P).
#show difficulty(P, D) : difficulty(P, D).
#show prerequisite(P, Q) : prerequisite(P, Q).