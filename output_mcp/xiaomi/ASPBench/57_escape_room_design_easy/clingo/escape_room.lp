% Domain: Puzzles
puzzle(1..6).

% Difficulty levels for each puzzle
difficulty(1, 1).  % Puzzle 1: easy
difficulty(2, 1).  % Puzzle 2: easy
difficulty(3, 2).  % Puzzle 3: medium
difficulty(4, 2).  % Puzzle 4: medium
difficulty(5, 3).  % Puzzle 5: hard
difficulty(6, 3).  % Puzzle 6: hard

% Prerequisites: prereq(P, Q) means puzzle P requires puzzle Q
prereq(2, 1).  % Puzzle 2 needs puzzle 1
prereq(3, 2).  % Puzzle 3 needs puzzle 2
prereq(3, 4).  % Puzzle 3 needs puzzle 4
prereq(4, 1).  % Puzzle 4 needs puzzle 1
prereq(5, 3).  % Puzzle 5 needs puzzle 3
prereq(6, 5).  % Puzzle 6 needs puzzle 5

% Positions in the sequence (1 to 6)
position(1..6).

% Assign each puzzle to exactly one position
1 { position(P, Pos) : position(Pos) } 1 :- puzzle(P).

% Each position has exactly one puzzle
1 { position(P, Pos) : puzzle(P) } 1 :- position(Pos).

% A puzzle cannot be completed before all its prerequisites
% If puzzle P requires puzzle Q, then Q must be at an earlier position
:- prereq(P, Q), position(P, PosP), position(Q, PosQ), PosQ >= PosP.

% Show the ordering
#show position/2.

% Show puzzle details
#show puzzle/1.
#show difficulty/2.
#show prereq/2.