% Crossword Puzzle Generator - 5x5 Grid with 6 Technology Words

% Grid dimensions
row(0..4).
col(0..4).

% Words to place
word("code", 4).
word("data", 4).
word("tech", 4).
word("chip", 4).
word("byte", 4).
word("net", 3).

% Directions
direction("horizontal").
direction("vertical").

% For each word, we need to choose a starting position and direction
% The word must fit within the grid
% For horizontal: col + len - 1 <= 4
% For vertical: row + len - 1 <= 4

% Define fits constraint
fits(W, R, C, "horizontal") :- word(W, Len), row(R), col(C), C + Len - 1 <= 4.
fits(W, R, C, "vertical") :- word(W, Len), row(R), col(C), R + Len - 1 <= 4.

% Generate placements: each word gets exactly one placement
{ placement(W, R, C, D) : row(R), col(C), direction(D), fits(W, R, C, D) } 1 :- word(W, Len).

% Each word must be placed exactly once
:- word(W, _), not placement(W, _, _, _).

% Define character positions for each word
char_pos("code", 0, "c"). char_pos("code", 1, "o"). char_pos("code", 2, "d"). char_pos("code", 3, "e").
char_pos("data", 0, "d"). char_pos("data", 1, "a"). char_pos("data", 2, "t"). char_pos("data", 3, "a").
char_pos("tech", 0, "t"). char_pos("tech", 1, "e"). char_pos("tech", 2, "c"). char_pos("tech", 3, "h").
char_pos("chip", 0, "c"). char_pos("chip", 1, "h"). char_pos("chip", 2, "i"). char_pos("chip", 3, "p").
char_pos("byte", 0, "b"). char_pos("byte", 1, "y"). char_pos("byte", 2, "t"). char_pos("byte", 3, "e").
char_pos("net", 0, "n"). char_pos("net", 1, "e"). char_pos("net", 2, "t").

% Derive the letter at each grid cell from horizontal placements
grid_letter(R, C, L) :- placement(W, R, C0, "horizontal"), char_pos(W, Pos, L), C = C0 + Pos, row(R), col(C).

% Derive the letter at each grid cell from vertical placements
grid_letter(R, C, L) :- placement(W, R0, C, "vertical"), char_pos(W, Pos, L), R = R0 + Pos, row(R), col(C).

% No conflicts: if two placements assign different letters to the same cell, it's invalid
:- grid_letter(R, C, L1), grid_letter(R, C, L2), L1 != L2.

% Define which cells are occupied
occupied(R, C) :- grid_letter(R, C, _).

% Define adjacency for connectivity
adjacent(R1, C1, R2, C2) :- occupied(R1, C1), occupied(R2, C2), |R1-R2| + |C1-C2| = 1.

% Reachability: start from any occupied cell
reached(R, C) :- occupied(R, C), R = 0, C = 0, occupied(0,0).
reached(R2, C2) :- reached(R1, C1), adjacent(R1, C1, R2, C2).

% All occupied cells must be reachable (connected crossword)
:- occupied(R, C), not reached(R, C).

% A word intersects another if they share a cell with the same letter
has_intersection(W) :- 
    placement(W, R, C, D),
    placement(W2, R2, C2, D2),
    W != W2,
    char_pos(W, Pos, L),
    char_pos(W2, Pos2, L),
    ((D = "horizontal", D2 = "horizontal", R = R2, C + Pos = C2 + Pos2);
     (D = "horizontal", D2 = "vertical", R = R2 + Pos2, C + Pos = C2);
     (D = "vertical", D2 = "horizontal", R + Pos = R2, C = C2 + Pos2);
     (D = "vertical", D2 = "vertical", C = C2, R + Pos = R2 + Pos2)).

% Each word must intersect with at least one other word
:- word(W, _), placement(W, _, _, _), not has_intersection(W).

% Show the grid and placements
#show grid_letter/3.
#show placement/4.