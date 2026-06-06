% Base facts: chapters and clues
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Assign exactly one clue to each chapter
1 { assigned(Chapter, Clue) : clue(Clue) } 1 :- chapter(Chapter).

% Each clue is mentioned exactly once
:- clue(Clue), not 1 { assigned(Chapter, Clue) : chapter(Chapter) } 1.

% Constraints:
% 1. T cannot be mentioned in chapter 1
:- assigned(1, t).

% 2. T must be mentioned before W, with exactly two chapters separating them
:- assigned(T_chapter, t), assigned(W_chapter, w), T_chapter >= W_chapter.
:- assigned(T_chapter, t), assigned(W_chapter, w), W_chapter - T_chapter != 3.

% 3. S and Z cannot be mentioned in adjacent chapters
:- assigned(S_chapter, s), assigned(Z_chapter, z), abs(S_chapter - Z_chapter) = 1.

% 4. W and X cannot be mentioned in adjacent chapters
:- assigned(W_chapter, w), assigned(X_chapter, x), abs(W_chapter - X_chapter) = 1.

% 5. U and X must be mentioned in adjacent chapters
:- assigned(U_chapter, u), assigned(X_chapter, x), abs(U_chapter - X_chapter) != 1.

% Additional constraint: U is mentioned in chapter 3
:- not assigned(3, u).

% Map the correct answer to option/1 (MANDATORY)
% (A) R is mentioned in chapter 1
option(a) :- assigned(1, r).

% (B) R is mentioned in chapter 5
option(b) :- assigned(5, r).

% (C) S is mentioned in chapter 7
option(c) :- assigned(7, s).

% (D) W is mentioned in chapter 6
option(d) :- assigned(6, w).

% (E) X is mentioned in chapter 4
option(e) :- assigned(4, x).

#show option/1.