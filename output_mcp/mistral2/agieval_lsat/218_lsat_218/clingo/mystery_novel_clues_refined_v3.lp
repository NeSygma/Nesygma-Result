% Base facts: chapters and clues
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Assign exactly one clue to each chapter
1 { assigned(Chapter, Clue) : clue(Clue) } 1 :- chapter(Chapter).
1 { assigned(Chapter, Clue) : chapter(Chapter) } 1 :- clue(Clue).

% Constraints from the problem statement
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

% Original constraint: T cannot be mentioned in chapter 1
:- assigned(1, t).

% Define a predicate to check if the original constraint is satisfied
original_constraint_satisfied :- not assigned(1, t).

% Option A: U cannot be mentioned in chapter 2
option_a :- not has_u_in_chapter_2.
has_u_in_chapter_2 :- assigned(2, u).

% Option B: W cannot be mentioned in chapter 4
option_b :- not has_w_in_chapter_4.
has_w_in_chapter_4 :- assigned(4, w).

% Option C: X cannot be mentioned in chapter 6
option_c :- not has_x_in_chapter_6.
has_x_in_chapter_6 :- assigned(6, x).

% Option D: U must be mentioned in an earlier chapter than T
option_d :- u_before_t.
u_before_t :- assigned(U_chapter, u), assigned(T_chapter, t), U_chapter < T_chapter.

% Option E: X must be mentioned in an earlier chapter than W
option_e :- x_before_w.
x_before_w :- assigned(X_chapter, x), assigned(W_chapter, w), X_chapter < W_chapter.

% Replace the original constraint with the option's constraint and check for equivalence
% Option A: Replace ":- assigned(1, t)" with ":- assigned(2, u)"
:- option_a, assigned(2, u).

% Option B: Replace ":- assigned(1, t)" with ":- assigned(4, w)"
:- option_b, assigned(4, w).

% Option C: Replace ":- assigned(1, t)" with ":- assigned(6, x)"
:- option_c, assigned(6, x).

% Option D: Replace ":- assigned(1, t)" with ":- not u_before_t"
:- option_d, not u_before_t.

% Option E: Replace ":- assigned(1, t)" with ":- not x_before_w"
:- option_e, not x_before_w.

% Check if the option enforces the same constraint as the original problem
% If the option is correct, the resulting program should be satisfiable and produce the same orderings as the original constraint
equivalent_to_original(option_a) :- option_a, not has_u_in_chapter_2.
equivalent_to_original(option_b) :- option_b, not has_w_in_chapter_4.
equivalent_to_original(option_c) :- option_c, not has_x_in_chapter_6.
equivalent_to_original(option_d) :- option_d, u_before_t.
equivalent_to_original(option_e) :- option_e, x_before_w.

% Ensure only one option is selected as equivalent
1 { correct_option(Opt) : equivalent_to_original(Opt) } 1.

% Show the correct option
#show correct_option/1.