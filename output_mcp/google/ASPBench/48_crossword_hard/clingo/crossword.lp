% Grid and Domain
row(0..5). col(0..5).
black(0,0). black(0,5). black(5,0). black(5,5).

% Words and Letters
word(cat; ace; tea; ear; ate; rat; car; tar).
word_letter(cat, 0, "C"). word_letter(cat, 1, "A"). word_letter(cat, 2, "T").
word_letter(ace, 0, "A"). word_letter(ace, 1, "C"). word_letter(ace, 2, "E").
word_letter(tea, 0, "T"). word_letter(tea, 1, "E"). word_letter(tea, 2, "A").
word_letter(ear, 0, "E"). word_letter(ear, 1, "A"). word_letter(ear, 2, "R").
word_letter(ate, 0, "A"). word_letter(ate, 1, "T"). word_letter(ate, 2, "E").
word_letter(rat, 0, "R"). word_letter(rat, 1, "A"). word_letter(rat, 2, "T").
word_letter(car, 0, "C"). word_letter(car, 1, "A"). word_letter(car, 2, "R").
word_letter(tar, 0, "T"). word_letter(tar, 1, "A"). word_letter(tar, 2, "R").

% Placement
direction(horizontal; vertical).
{ place(W, R, C, D) : row(R), col(C), direction(D) } = 1 :- word(W).

% Constraints: Bounds
:- place(W, R, C, horizontal), C + 2 >= 6.
:- place(W, R, C, vertical), R + 2 >= 6.

% Constraints: Black Squares
:- place(W, R, C, _), black(R, C).
cell_letter(R, C, L, W) :- place(W, R, C, horizontal), word_letter(W, I, L), C + I < 6, R < 6, C + I >= 0, R >= 0, I = 0..2.
cell_letter(R, C, L, W) :- place(W, R, C, vertical), word_letter(W, I, L), R + I < 6, C < 6, R + I >= 0, C >= 0, I = 0..2.

:- cell_letter(R, C, _, W), black(R, C).

% Constraints: No Conflicts
:- cell_letter(R, C, L1, W1), cell_letter(R, C, L2, W2), W1 != W2, L1 != L2.

% Constraints: Intersections
intersection(R, C, W1, W2) :- cell_letter(R, C, L, W1), cell_letter(R, C, L, W2), W1 < W2.
num_intersections(N) :- N = #count { R, C, W1, W2 : intersection(R, C, W1, W2) }.
:- num_intersections(N), N < 3.

% Constraints: Connectivity
occupied(R, C) :- cell_letter(R, C, _, _).
% Pick an arbitrary occupied cell to start connectivity check
start_cell(R, C) :- occupied(R, C), R = #min { R1 : occupied(R1, _) }, C = #min { C1 : occupied(R1, C1) }.
reachable(R, C) :- start_cell(R, C).
reachable(R, C) :- reachable(R1, C1), occupied(R, C), |R-R1| + |C-C1| = 1.
:- occupied(R, C), not reachable(R, C).

#show place/4.