% ===== DOMAINS =====
row(0..5).
col(0..5).
pos(0..2).
dir(h). dir(v).

% ===== BLACK SQUARES =====
black(0,0). black(0,5). black(5,0). black(5,5).

% ===== WORDS =====
word(cat). word(ace). word(tea). word(ear). word(ate). word(rat). word(car). word(tar).

% ===== LETTERS IN EACH WORD =====
letter(cat, 0, c). letter(cat, 1, a). letter(cat, 2, t).
letter(ace, 0, a). letter(ace, 1, c). letter(ace, 2, e).
letter(tea, 0, t). letter(tea, 1, e). letter(tea, 2, a).
letter(ear, 0, e). letter(ear, 1, a). letter(ear, 2, r).
letter(ate, 0, a). letter(ate, 1, t). letter(ate, 2, e).
letter(rat, 0, r). letter(rat, 1, a). letter(rat, 2, t).
letter(car, 0, c). letter(car, 1, a). letter(car, 2, r).
letter(tar, 0, t). letter(tar, 1, a). letter(tar, 2, r).

% ===== CHOICE: PLACE EACH WORD EXACTLY ONCE =====
{ place(W, R, C, D) : row(R), col(C), dir(D) } 1 :- word(W).

% ===== GRID BOUNDS =====
% Horizontal: C + 2 <= 5 => C <= 3
:- place(W, R, C, h), C > 3.
% Vertical: R + 2 <= 5 => R <= 3
:- place(W, R, C, v), R > 3.

% ===== BLACK SQUARE CONSTRAINTS =====
% Horizontal words cannot touch black squares
:- place(W, R, C, h), black(R, C).
:- place(W, R, C, h), black(R, C+1).
:- place(W, R, C, h), black(R, C+2).
% Vertical words cannot touch black squares
:- place(W, R, C, v), black(R, C).
:- place(W, R, C, v), black(R+1, C).
:- place(W, R, C, v), black(R+2, C).

% ===== CELL POSITIONS FOR HORIZONTAL WORDS =====
hcell(W, R, C, 0) :- place(W, R, C, h).
hcell(W, R, C1, 1) :- place(W, R, C, h), C1 = C + 1.
hcell(W, R, C2, 2) :- place(W, R, C, h), C2 = C + 2.

% ===== CELL POSITIONS FOR VERTICAL WORDS =====
vcell(W, R, C, 0) :- place(W, R, C, v).
vcell(W, R1, C, 1) :- place(W, R, C, v), R1 = R + 1.
vcell(W, R2, C, 2) :- place(W, R, C, v), R2 = R + 2.

% ===== CELL LETTER ASSIGNMENT =====
cell(R, C, L) :- hcell(W, R, C, P), letter(W, P, L).
cell(R, C, L) :- vcell(W, R, C, P), letter(W, P, L).

% ===== NO CONFLICTS: SAME CELL CANNOT HAVE DIFFERENT LETTERS =====
:- cell(R, C, L1), cell(R, C, L2), L1 != L2.

% ===== NO OVERLAP IN SAME DIRECTION =====
:- hcell(W1, R, C, _), hcell(W2, R, C, _), W1 != W2.
:- vcell(W1, R, C, _), vcell(W2, R, C, _), W1 != W2.

% ===== HAS LETTER =====
has_letter(R, C) :- cell(R, C, _).

% ===== INTERSECTIONS =====
intersection(R, C) :- hcell(_, R, C, _), vcell(_, R, C, _).

% At least 3 intersections required
int_count(N) :- N = #count { R, C : intersection(R, C) }.
:- int_count(N), N < 3.

% ===== CONNECTIVITY =====
% Adjacency (only positive direction to avoid duplicates)
adj(R1, C, R2, C) :- has_letter(R1, C), has_letter(R2, C), R2 = R1 + 1.
adj(R, C1, R, C2) :- has_letter(R, C1), has_letter(R, C2), C2 = C1 + 1.

% Root: lexicographically smallest cell with a letter
root(R, C) :- has_letter(R, C), not has_earlier(R, C).
has_earlier(R, C) :- has_letter(R, C), has_letter(R2, C2), R2 < R.
has_earlier(R, C) :- has_letter(R, C), has_letter(R2, C2), R2 = R, C2 < C.

% Reachability from root (both directions)
reachable(R, C) :- root(R, C).
reachable(R2, C2) :- reachable(R1, C1), adj(R1, C1, R2, C2).
reachable(R1, C1) :- reachable(R2, C2), adj(R1, C1, R2, C2).

% All cells with letters must be reachable
:- has_letter(R, C), not reachable(R, C).

% ===== THEME =====
theme("three_letter_words").

% ===== OUTPUT =====
#show place/4.
#show cell/3.
#show intersection/2.
#show theme/1.