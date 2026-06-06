% Crossword Puzzle Solver
% 6x6 grid with 8 three-letter words

% ===== DOMAIN DECLARATION =====
% Grid cells
grid(0..5, 0..5).

% Black squares at corners
black(0,0). black(0,5). black(5,0). black(5,5).

% Words
word("CAT"). word("ACE"). word("TEA"). word("EAR"). word("ATE"). word("RAT"). word("CAR"). word("TAR").

% Letter positions in words (0,1,2 for three-letter words)
position(0). position(1). position(2).

% Directions
direction("horizontal"). direction("vertical").

% ===== LETTER DEFINITIONS =====
% Define letters for each word at each position
letter("CAT", "C", 0). letter("CAT", "A", 1). letter("CAT", "T", 2).
letter("ACE", "A", 0). letter("ACE", "C", 1). letter("ACE", "E", 2).
letter("TEA", "T", 0). letter("TEA", "E", 1). letter("TEA", "A", 2).
letter("EAR", "E", 0). letter("EAR", "A", 1). letter("EAR", "R", 2).
letter("ATE", "A", 0). letter("ATE", "T", 1). letter("ATE", "E", 2).
letter("RAT", "R", 0). letter("RAT", "A", 1). letter("RAT", "T", 2).
letter("CAR", "C", 0). letter("CAR", "A", 1). letter("CAR", "R", 2).
letter("TAR", "T", 0). letter("TAR", "A", 1). letter("TAR", "R", 2).

% ===== WORD PLACEMENT =====
% Each word placed exactly once in one direction
1 { placed(W, R, C, D) : grid(R, C), direction(D) } 1 :- word(W).

% ===== PLACEMENT CONSTRAINTS =====
% 1. Grid bounds: Words must fit within 0-5 range
% Horizontal: C + 2 <= 5
:- placed(W, R, C, "horizontal"), C > 3.
% Vertical: R + 2 <= 5
:- placed(W, R, C, "vertical"), R > 3.

% 2. Black squares: Words cannot start on black squares
:- placed(W, R, C, _), black(R, C).

% 3. Black squares: Words cannot cross through black squares
% For horizontal words
:- placed(W, R, C, "horizontal"), C1 = C+1, grid(R, C1), black(R, C1).
:- placed(W, R, C, "horizontal"), C2 = C+2, grid(R, C2), black(R, C2).
% For vertical words
:- placed(W, R, C, "vertical"), R1 = R+1, grid(R1, C), black(R1, C).
:- placed(W, R, C, "vertical"), R2 = R+2, grid(R2, C), black(R2, C).

% 4. No cell conflicts: Each cell can have at most one letter
% First, derive cell letters from placements
cell_letter(R, C, L) :- placed(W, R, C, "horizontal"), letter(W, L, 0).
cell_letter(R, C, L) :- placed(W, R, C, "horizontal"), letter(W, L, 1), C1 = C+1, grid(R, C1).
cell_letter(R, C, L) :- placed(W, R, C, "horizontal"), letter(W, L, 2), C2 = C+2, grid(R, C2).
cell_letter(R, C, L) :- placed(W, R, C, "vertical"), letter(W, L, 0).
cell_letter(R, C, L) :- placed(W, R, C, "vertical"), letter(W, L, 1), R1 = R+1, grid(R1, C).
cell_letter(R, C, L) :- placed(W, R, C, "vertical"), letter(W, L, 2), R2 = R+2, grid(R2, C).

% No two different letters in same cell
:- cell_letter(R, C, L1), cell_letter(R, C, L2), L1 != L2.

% ===== INTERSECTIONS =====
% Intersection: cell where horizontal and vertical words cross
intersection(R, C) :- placed(W1, R, C1, "horizontal"), placed(W2, R2, C, "vertical"),
                       C >= C1, C <= C1+2, R >= R2, R <= R2+2.

% At least 3 intersections
:- #count{R, C : intersection(R, C)} < 3.

% ===== CONNECTIVITY =====
% Define connected components using union-find approach
% First, mark all cells with letters
has_letter(R, C) :- cell_letter(R, C, _).

% For connectivity constraint, we'll ensure all letter cells are connected
% Use a simple approach: ensure there's a path between any two letter cells
% This is complex in ASP, so we'll use a simpler approach: ensure no isolated words
% An isolated word would be a word whose cells are not adjacent to any other word's cells

% Check if a word's cells are isolated
word_cells(W, R, C, "horizontal", R, C).      % First cell
word_cells(W, R, C, "horizontal", R, C+1).    % Second cell
word_cells(W, R, C, "horizontal", R, C+2).    % Third cell
word_cells(W, R, C, "vertical", R, C).        % First cell
word_cells(W, R, C, "vertical", R+1, C).      % Second cell
word_cells(W, R, C, "vertical", R+2, C).      % Third cell

% A word is isolated if none of its cells are adjacent to cells of other words
% For each word, check if at least one of its cells is adjacent to another word's cell
:- placed(W, R, C, D), word_cells(W, R, C, D, WR, WC),
   not (has_letter(R2, C2), (WR = R2, WC = C2+1; WR = R2, WC = C2-1; WR = R2+1, WC = C2; WR = R2-1, WC = C2),
        (R2 != WR; C2 != WC)).

% ===== SHOW DIRECTIVES =====
#show solution_exists/0.
#show placed/4.
#show cell_letter/3.
#show intersection/2.

% ===== FINAL CHECK =====
% Ensure solution exists
solution_exists :- placed(_, _, _, _), #count{R, C : intersection(R, C)} >= 3.