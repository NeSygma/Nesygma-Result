% Base facts: chapters and clues
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Assign exactly one clue to each chapter
1 { assigned(Chapter, Clue) : clue(Clue) } 1 :- chapter(Chapter).

% Ensure each clue is assigned to exactly one chapter
1 { assigned(Chapter, Clue) : chapter(Chapter) } 1 :- clue(Clue).

% Constraints from the problem statement

% T cannot be mentioned in chapter 1
:- assigned(1, t).

% T must be mentioned before W, with exactly two chapters separating them
:- assigned(T_chapter, t), assigned(W_chapter, w), T_chapter >= W_chapter.
:- assigned(T_chapter, t), assigned(W_chapter, w), W_chapter - T_chapter != 3.

% S and Z cannot be mentioned in adjacent chapters
:- assigned(S_chapter, s), assigned(Z_chapter, z), abs(S_chapter - Z_chapter) = 1.
:- assigned(S_chapter, z), assigned(Z_chapter, s), abs(S_chapter - Z_chapter) = 1.

% W and X cannot be mentioned in adjacent chapters
:- assigned(W_chapter, w), assigned(X_chapter, x), abs(W_chapter - X_chapter) = 1.
:- assigned(W_chapter, x), assigned(X_chapter, w), abs(W_chapter - X_chapter) = 1.

% U and X must be mentioned in adjacent chapters
:- assigned(U_chapter, u), assigned(X_chapter, x), abs(U_chapter - X_chapter) != 1.
:- assigned(U_chapter, x), assigned(X_chapter, u), abs(U_chapter - X_chapter) != 1.

% Substitute the constraint "T cannot be mentioned in chapter 1" with one of the options (A-E)
% We will evaluate each option by checking if it enforces the same ordering constraints as the original problem.

% Option A: U cannot be mentioned in chapter 2
option(a) :- not has_u_in_chapter_2.
has_u_in_chapter_2 :- assigned(2, u).

% Option B: W cannot be mentioned in chapter 4
option(b) :- not has_w_in_chapter_4.
has_w_in_chapter_4 :- assigned(4, w).

% Option C: X cannot be mentioned in chapter 6
option(c) :- not has_x_in_chapter_6.
has_x_in_chapter_6 :- assigned(6, x).

% Option D: U must be mentioned in an earlier chapter than T
option(d) :- u_before_t.
u_before_t :- assigned(U_chapter, u), assigned(T_chapter, t), U_chapter < T_chapter.

% Option E: X must be mentioned in an earlier chapter than W
option(e) :- x_before_w.
x_before_w :- assigned(X_chapter, x), assigned(W_chapter, w), X_chapter < W_chapter.

% Ensure only one option is selected
:- option(A), option(B), A != B.
:- option(A), option(C), A != C.
:- option(A), option(D), A != D.
:- option(A), option(E), A != E.
:- option(B), option(C), B != C.
:- option(B), option(D), B != D.
:- option(B), option(E), B != E.
:- option(C), option(D), C != D.
:- option(C), option(E), C != E.
:- option(D), option(E), D != E.

% Show the selected option
#show option/1.