% Crossword Puzzle Generator
% 6x6 grid with 8 three-letter words

% Grid dimensions
row(0..5).
col(0..5).

% Black squares at corners
black(0,0). black(0,5). black(5,0). black(5,5).

% Words to place
word("CAT"). word("ACE"). word("TEA"). word("EAR").
word("ATE"). word("RAT"). word("CAR"). word("TAR").

% Letters in each word
letter("CAT", 0, "C"). letter("CAT", 1, "A"). letter("CAT", 2, "T").
letter("ACE", 0, "A"). letter("ACE", 1, "C"). letter("ACE", 2, "E").
letter("TEA", 0, "T"). letter("TEA", 1, "E"). letter("TEA", 2, "A").
letter("EAR", 0, "E"). letter("EAR", 1, "A"). letter("EAR", 2, "R").
letter("ATE", 0, "A"). letter("ATE", 1, "T"). letter("ATE", 2, "E").
letter("RAT", 0, "R"). letter("RAT", 1, "A"). letter("RAT", 2, "T").
letter("CAR", 0, "C"). letter("CAR", 1, "A"). letter("CAR", 2, "R").
letter("TAR", 0, "T"). letter("TAR", 1, "A"). letter("TAR", 2, "R").

% Directions
direction("horizontal"). direction("vertical").

% Each word placed exactly once in one direction
{ placement(W, R, C, D) : row(R), col(C), direction(D) } 1 :- word(W).

% Grid bounds: word must fit within 6x6 grid
:- placement(W, R, C, "horizontal"), word(W), C + 2 > 5.
:- placement(W, R, C, "vertical"), word(W), R + 2 > 5.

% Black squares: words cannot start on or cross through black squares
% Cannot start on black square
:- placement(W, R, C, _), black(R, C).

% Cannot cross through black squares (horizontal)
:- placement(W, R, C, "horizontal"), black(R, C+1).
:- placement(W, R, C, "horizontal"), black(R, C+2).

% Cannot cross through black squares (vertical)
:- placement(W, R, C, "vertical"), black(R+1, C).
:- placement(W, R, C, "vertical"), black(R+2, C).

% Cell content: letter at (R,C) from a word placement
cell_letter(R, C, L) :- placement(W, R, C, "horizontal"), letter(W, 0, L).
cell_letter(R, C+1, L) :- placement(W, R, C, "horizontal"), letter(W, 1, L).
cell_letter(R, C+2, L) :- placement(W, R, C, "horizontal"), letter(W, 2, L).
cell_letter(R, C, L) :- placement(W, R, C, "vertical"), letter(W, 0, L).
cell_letter(R+1, C, L) :- placement(W, R, C, "vertical"), letter(W, 1, L).
cell_letter(R+2, C, L) :- placement(W, R, C, "vertical"), letter(W, 2, L).

% No conflicts: same cell cannot contain different letters
:- cell_letter(R, C, L1), cell_letter(R, C, L2), L1 != L2.

% A cell is occupied if it has a letter
occupied(R, C) :- cell_letter(R, C, _).

% Intersection: a cell where both a horizontal and vertical word pass through
% A cell is a horizontal cell if it's part of a horizontal placement
h_cell(R, C) :- placement(W, R, C, "horizontal"), letter(W, 0, _).
h_cell(R, C+1) :- placement(W, R, C, "horizontal"), letter(W, 1, _).
h_cell(R, C+2) :- placement(W, R, C, "horizontal"), letter(W, 2, _).

% A cell is a vertical cell if it's part of a vertical placement
v_cell(R, C) :- placement(W, R, C, "vertical"), letter(W, 0, _).
v_cell(R+1, C) :- placement(W, R, C, "vertical"), letter(W, 1, _).
v_cell(R+2, C) :- placement(W, R, C, "vertical"), letter(W, 2, _).

% Intersection point
intersection(R, C) :- h_cell(R, C), v_cell(R, C).

% At least 3 intersection points
:- #count { R,C : intersection(R,C) } < 3.

% Connectivity: all placed letters must form a single connected component
% Use adjacency (4-directional) to define connectivity
adjacent(R1, C1, R2, C2) :- occupied(R1, C1), occupied(R2, C2),
                             |R1-R2| + |C1-C2| = 1.

% Reachability: start from any occupied cell
reached(R, C) :- occupied(R, C), not unreached(R, C).
% Actually, let's use a proper connected component approach.

% Define reachable from a seed cell
% Pick the first occupied cell (by row, then col) as seed
seed_cell(R, C) :- occupied(R, C), 
                   R = #min { R1 : occupied(R1, _) },
                   C = #min { C1 : occupied(R1, C1), R1 = R }.

% Reachable via adjacency
reachable(R, C) :- seed_cell(R, C).
reachable(R2, C2) :- reachable(R1, C1), adjacent(R1, C1, R2, C2).

% All occupied cells must be reachable
:- occupied(R, C), not reachable(R, C).

% Show results
#show placement/4.
#show cell_letter/3.
#show intersection/2.