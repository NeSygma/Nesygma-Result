% Crossword Puzzle Solver
% 6x6 grid with black squares at corners
% 8 three-letter words: CAT, ACE, TEA, EAR, ATE, RAT, CAR, TAR

% ===== DOMAIN DEFINITIONS =====
% Grid coordinates
row(0..5).
col(0..5).

% Black squares at corners
black(0,0). black(0,5). black(5,0). black(5,5).

% ===== WORD DEFINITIONS =====
% Each word has 3 letters at positions 0,1,2
word("cat"). word("ace"). word("tea"). word("ear"). 
word("ate"). word("rat"). word("car"). word("tar").

% Letter positions for each word
letter("cat", 0, "c"). letter("cat", 1, "a"). letter("cat", 2, "t").
letter("ace", 0, "a"). letter("ace", 1, "c"). letter("ace", 2, "e").
letter("tea", 0, "t"). letter("tea", 1, "e"). letter("tea", 2, "a").
letter("ear", 0, "e"). letter("ear", 1, "a"). letter("ear", 2, "r").
letter("ate", 0, "a"). letter("ate", 1, "t"). letter("ate", 2, "e").
letter("rat", 0, "r"). letter("rat", 1, "a"). letter("rat", 2, "t").
letter("car", 0, "c"). letter("car", 1, "a"). letter("car", 2, "r").
letter("tar", 0, "t"). letter("tar", 1, "a"). letter("tar", 2, "r").

% ===== PLACEMENT GENERATION =====
% Horizontal placement: word starts at (R,C) and goes right
% Valid if: fits in grid (C+2 <= 5), doesn't cross black squares
{ placed_h(W, R, C) } :- 
    word(W), row(R), col(C), 
    C + 2 <= 5,  % fits horizontally
    not black(R, C), not black(R, C+1), not black(R, C+2).

% Vertical placement: word starts at (R,C) and goes down
% Valid if: fits in grid (R+2 <= 5), doesn't cross black squares
{ placed_v(W, R, C) } :- 
    word(W), row(R), col(C), 
    R + 2 <= 5,  % fits vertically
    not black(R, C), not black(R+1, C), not black(R+2, C).

% ===== CONSTRAINTS =====
% Each word must be placed exactly once (either horizontal or vertical)
% Use a unified placement predicate
placed(W, R, C, "horizontal") :- placed_h(W, R, C).
placed(W, R, C, "vertical") :- placed_v(W, R, C).

% Each word placed exactly once
1 { placed(W, R, C, D) : row(R), col(C), direction(D) } 1 :- word(W).

% Direction domain
direction("horizontal"). direction("vertical").

% ===== CELL LETTER DERIVATION =====
% For each placement, derive the letters in each cell
cell_letter(R, C, L) :- placed(W, R, C, "horizontal"), letter(W, 0, L).
cell_letter(R, C+1, L) :- placed(W, R, C, "horizontal"), letter(W, 1, L).
cell_letter(R, C+2, L) :- placed(W, R, C, "horizontal"), letter(W, 2, L).
cell_letter(R, C, L) :- placed(W, R, C, "vertical"), letter(W, 0, L).
cell_letter(R+1, C, L) :- placed(W, R, C, "vertical"), letter(W, 1, L).
cell_letter(R+2, C, L) :- placed(W, R, C, "vertical"), letter(W, 2, L).

% Conflict constraint: no cell can have two different letters
:- cell_letter(R, C, L1), cell_letter(R, C, L2), L1 != L2.

% ===== INTERSECTION CONSTRAINTS =====
% Intersection: where horizontal and vertical words share a cell
intersection(R, C) :-
    placed(W1, R1, C1, "horizontal"), placed(W2, R2, C2, "vertical"),
    R = R1, C >= C1, C <= C1 + 2,  % horizontal covers (R,C)
    R >= R2, R <= R2 + 2, C = C2.  % vertical covers (R,C)

% At least 3 intersections
intersection_count(N) :- N = #count { R, C : intersection(R, C) }.
:- intersection_count(N), N < 3.

% ===== CONNECTIVITY CONSTRAINTS =====
% All placed letters must form a single connected component
% First, define which cells have letters
has_letter(R, C) :- cell_letter(R, C, _).

% Connected component using BFS-like approach
% Start from any letter cell and mark all reachable cells
% We need to find one starting point
start_cell(R, C) :- has_letter(R, C), R = #min { R1 : has_letter(R1, _) }.
start_cell(R, C) :- has_letter(R, C), C = #min { C1 : has_letter(R, C1) }.

% Mark connected cells using iterative approach
connected(R, C) :- has_letter(R, C), start_cell(R, C).
connected(R, C) :- has_letter(R, C), connected(R-1, C), has_letter(R-1, C).
connected(R, C) :- has_letter(R, C), connected(R+1, C), has_letter(R+1, C).
connected(R, C) :- has_letter(R, C), connected(R, C-1), has_letter(R, C-1).
connected(R, C) :- has_letter(R, C), connected(R, C+1), has_letter(R, C+1).

% All letter cells must be connected
:- has_letter(R, C), not connected(R, C).

% ===== OUTPUT =====
% Show the grid
#show grid/3.  % grid(R, C, Letter) or grid(R, C, "#") for black
grid(R, C, "#") :- black(R, C).
grid(R, C, L) :- cell_letter(R, C, L), not black(R, C).
grid(R, C, " ") :- row(R), col(C), not black(R, C), not cell_letter(R, C, _).

% Show placements
#show placed/4.

% Show intersection count
#show intersection_count/1.