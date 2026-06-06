% Grid dimensions
row(0..5).
col(0..5).

% Black squares at corners
black(0,0). black(0,5). black(5,0). black(5,5).

% Words (8 three-letter words)
word("CAT"). word("ACE"). word("TEA"). word("EAR").
word("ATE"). word("RAT"). word("CAR"). word("TAR").

% Letters in each word: word(Word, Position, Letter)
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

% --- Possible placements ---
% Horizontal: start (R,C) with C <= 3, all 3 cells not black
possible_placement(W, R, C, "horizontal") :- 
    word(W), row(R), col(C), C <= 3,
    not black(R, C), not black(R, C+1), not black(R, C+2).

% Vertical: start (R,C) with R <= 3, all 3 cells not black
possible_placement(W, R, C, "vertical") :- 
    word(W), row(R), col(C), R <= 3,
    not black(R, C), not black(R+1, C), not black(R+2, C).

% Each word placed exactly once
1 { placement(W, R, C, D) : possible_placement(W, R, C, D) } 1 :- word(W).

% --- Occupied cells ---
% Horizontal word: cells (R, C_start), (R, C_start+1), (R, C_start+2)
occupied(R, C, L) :- 
    placement(W, R, C_start, "horizontal"), 
    letter(W, Pos, L), 
    C = C_start + Pos.

% Vertical word: cells (R_start, C), (R_start+1, C), (R_start+2, C)
occupied(R, C, L) :- 
    placement(W, R_start, C, "vertical"), 
    letter(W, Pos, L), 
    R = R_start + Pos.

% Conflict: same cell cannot have two different letters
:- occupied(R, C, L1), occupied(R, C, L2), L1 != L2.

% Filled cells (cells with a letter)
filled(R, C) :- occupied(R, C, _).

% --- Intersections ---
% A cell (R,C) has a horizontal word passing through it
has_horizontal(R, C) :- 
    placement(_, R, C_start, "horizontal"), 
    col(C), C_start <= C, C <= C_start + 2.

% A cell (R,C) has a vertical word passing through it
has_vertical(R, C) :- 
    placement(_, R_start, C, "vertical"), 
    row(R), R_start <= R, R <= R_start + 2.

% Intersection cell
intersection(R, C) :- has_horizontal(R, C), has_vertical(R, C).

% At least 3 intersections
:- #count { R, C : intersection(R, C) } < 3.

% --- Connectivity: all filled cells must form one connected component ---
% Orthogonal adjacency between filled cells
adj(R1, C1, R2, C2) :- filled(R1, C1), filled(R2, C2), R1 = R2, C1 = C2 + 1.
adj(R1, C1, R2, C2) :- filled(R1, C1), filled(R2, C2), R1 = R2, C1 + 1 = C2.
adj(R1, C1, R2, C2) :- filled(R1, C1), filled(R2, C2), C1 = C2, R1 = R2 + 1.
adj(R1, C1, R2, C2) :- filled(R1, C1), filled(R2, C2), C1 = C2, R1 + 1 = R2.

% Find the root cell (lexicographically smallest filled cell)
not_min_root(R, C) :- filled(R, C), filled(R2, C2), R2 < R.
not_min_root(R, C) :- filled(R, C), filled(R, C2), C2 < C.
root(R, C) :- filled(R, C), not not_min_root(R, C).

% Reachability from root
reachable(R, C) :- root(R, C).
reachable(R2, C2) :- reachable(R1, C1), adj(R1, C1, R2, C2).

% All filled cells must be reachable
:- filled(R, C), not reachable(R, C).

% --- Output ---
#show occupied/3.
#show placement/4.
#show intersection/2.