% Crossword Puzzle Generator - 6x6 Grid with 8 Three-Letter Words
% Simplified version - focus on core constraints first

% ============ DOMAIN DEFINITIONS ============

% Grid dimensions
row(0..5).
col(0..5).

% Words (8 three-letter words)
word(cat). word(ace). word(tea). word(ear). word(ate). word(rat). word(car). word(tar).

% Letter positions within words (0, 1, 2 for three-letter words)
pos(0). pos(1). pos(2).

% Directions
dir(h). dir(v).  % h = horizontal, v = vertical

% ============ WORD LETTER DATA ============

% Define letters for each word at each position
letter(cat, 0, "C"). letter(cat, 1, "A"). letter(cat, 2, "T").
letter(ace, 0, "A"). letter(ace, 1, "C"). letter(ace, 2, "E").
letter(tea, 0, "T"). letter(tea, 1, "E"). letter(tea, 2, "A").
letter(ear, 0, "E"). letter(ear, 1, "A"). letter(ear, 2, "R").
letter(ate, 0, "A"). letter(ate, 1, "T"). letter(ate, 2, "E").
letter(rat, 0, "R"). letter(rat, 1, "A"). letter(rat, 2, "T").
letter(car, 0, "C"). letter(car, 1, "A"). letter(car, 2, "R").
letter(tar, 0, "T"). letter(tar, 1, "A"). letter(tar, 2, "R").

% ============ BLACK SQUARES ============

% Black squares at corners
black(0,0). black(0,5). black(5,0). black(5,5).

% ============ PLACEMENT CHOICE ============

% Each word must be placed exactly once
1 { placed(W, R, C, D) : row(R), col(C), dir(D) } 1 :- word(W).

% ============ GRID BOUNDS CONSTRAINT ============

% Horizontal words must fit: starting col + 2 <= 5
:- placed(W, R, C, h), C + 2 > 5.

% Vertical words must fit: starting row + 2 <= 5
:- placed(W, R, C, v), R + 2 > 5.

% ============ BLACK SQUARE CONSTRAINTS ============

% Words cannot start on black squares
:- placed(W, R, C, D), black(R, C).

% Horizontal words cannot cross black squares
:- placed(W, R, C, h), black(R, C+1).
:- placed(W, R, C, h), black(R, C+2).

% Vertical words cannot cross black squares
:- placed(W, R, C, v), black(R+1, C).
:- placed(W, R, C, v), black(R+2, C).

% ============ CELL OCCUPATION ============

% A cell is occupied by a specific letter from a placed word
cell_letter(W, R, C, L) :- placed(W, R0, C0, h), letter(W, P, L), R = R0, C = C0 + P.
cell_letter(W, R, C, L) :- placed(W, R0, C0, v), letter(W, P, L), R = R0 + P, C = C0.

% ============ NO CONFLICTS ============

% Same cell cannot have different letters from different words
:- cell_letter(W1, R, C, L1), cell_letter(W2, R, C, L2), W1 != W2, L1 != L2.

% ============ INTERSECTIONS ============

% An intersection is a cell occupied by both a horizontal and vertical word
intersection(R, C) :- cell_letter(W1, R, C, _), cell_letter(W2, R, C, _), 
                       placed(W1, _, _, h), placed(W2, _, _, v), W1 != W2.

% At least 3 intersections required
:- #count { R, C : intersection(R, C) } < 3.

% ============ CONNECTIVITY (simplified) ============

% Define which cells are occupied (not black, have a letter)
occupied(R, C) :- cell_letter(_, R, C, _), not black(R, C).

% Adjacency (horizontal and vertical neighbors)
adjacent(R1, C1, R2, C2) :- occupied(R1, C1), occupied(R2, C2), R1 = R2, C2 = C1 + 1.
adjacent(R1, C1, R2, C2) :- occupied(R1, C1), occupied(R2, C2), R1 = R2, C1 = C2 + 1.
adjacent(R1, C1, R2, C2) :- occupied(R1, C1), occupied(R2, C2), C1 = C2, R2 = R1 + 1.
adjacent(R1, C1, R2, C2) :- occupied(R1, C1), occupied(R2, C2), C1 = C2, R1 = R2 + 1.

% Reachability for connectivity (BFS-like)
reachable(R, C) :- occupied(R, C), not any_reachable.
reachable(R2, C2) :- reachable(R1, C1), adjacent(R1, C1, R2, C2).

any_reachable :- reachable(_, _).

% All occupied cells must be reachable from some starting point
:- occupied(R, C), not reachable(R, C).

% ============ OUTPUT ============

#show placed/4.
#show cell_letter/4.
#show intersection/2.