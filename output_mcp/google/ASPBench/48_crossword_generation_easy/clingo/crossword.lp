% Grid dimensions
row(0..4).
col(0..4).

% Word definitions
word(1, "CODE", 4).
word(2, "DATA", 4).
word(3, "TECH", 4).
word(4, "CHIP", 4).
word(5, "BYTE", 4).
word(6, "NET", 3).

% Character definitions
char_at(1, 0, "C"). char_at(1, 1, "O"). char_at(1, 2, "D"). char_at(1, 3, "E").
char_at(2, 0, "D"). char_at(2, 1, "A"). char_at(2, 2, "T"). char_at(2, 3, "A").
char_at(3, 0, "T"). char_at(3, 1, "E"). char_at(3, 2, "C"). char_at(3, 3, "H").
char_at(4, 0, "C"). char_at(4, 1, "H"). char_at(4, 2, "I"). char_at(4, 3, "P").
char_at(5, 0, "B"). char_at(5, 1, "Y"). char_at(5, 2, "T"). char_at(5, 3, "E").
char_at(6, 0, "N"). char_at(6, 1, "E"). char_at(6, 2, "T").

% Directions
direction(horizontal; vertical).

% Choice rule: Place each word exactly once
1 { place(W, R, C, D) : row(R), col(C), direction(D) } 1 :- word(W, _, _).

% Bounds constraints
:- place(W, R, C, horizontal), word(W, _, L), C + L > 5.
:- place(W, R, C, vertical), word(W, _, L), R + L > 5.

% Map word characters to grid positions
grid_pos(W, I, R, C) :- place(W, R, C, horizontal), char_at(W, I, Char), R = R, C = C + I.
grid_pos(W, I, R, C) :- place(W, R, C, vertical), char_at(W, I, Char), R = R + I, C = C.

% Helper to get character at grid position
char_at_grid(R, C, Char, W) :- grid_pos(W, I, R, C), char_at(W, I, Char).

% No conflicts: If two words share a cell, they must have the same letter
:- char_at_grid(R, C, Char1, W1), char_at_grid(R, C, Char2, W2), W1 < W2, Char1 != Char2.

% Intersection requirement: At least some words must intersect
% Let's relax the connectivity constraint for now to see if any placement exists
% and then enforce it if needed.
% Actually, the problem says "proper intersections". Let's enforce at least one intersection.
intersection(W1, W2, R, C) :- char_at_grid(R, C, _, W1), char_at_grid(R, C, _, W2), W1 < W2.
:- not intersection(_, _, _, _).

% Output
#show place/4.
#show intersection/4.