% Domains
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Given condition: U is mentioned in chapter 3
assigned(u, 3).

% Each clue appears exactly once in one chapter
1 { assigned(C, Ch) : chapter(Ch) } 1 :- clue(C).

% Each chapter has exactly one clue
1 { assigned(C, Ch) : clue(C) } 1 :- chapter(Ch).

% Constraint 1: T cannot be mentioned in chapter 1
:- assigned(t, 1).

% Constraint 2: T must be before W with exactly two chapters separating them
% If T is in chapter T_ch, W must be in chapter T_ch + 3
:- assigned(t, T_ch), assigned(w, W_ch), W_ch != T_ch + 3.

% Constraint 3: S and Z cannot be mentioned in adjacent chapters
:- assigned(s, S_ch), assigned(z, Z_ch), abs(S_ch - Z_ch) = 1.

% Constraint 4: W and X cannot be mentioned in adjacent chapters
:- assigned(w, W_ch), assigned(x, X_ch), abs(W_ch - X_ch) = 1.

% Constraint 5: U and X must be mentioned in adjacent chapters
% U is in chapter 3, so X must be in chapter 2 or 4
:- assigned(x, X_ch), X_ch != 2, X_ch != 4.

% Option A: R is mentioned in chapter 1
% Option B: R is mentioned in chapter 5
% Option C: S is mentioned in chapter 7
% Option D: W is mentioned in chapter 6
% Option E: X is mentioned in chapter 4

% Map the correct answer to option/1
option(a) :- assigned(r, 1).
option(b) :- assigned(r, 5).
option(c) :- assigned(s, 7).
option(d) :- assigned(w, 6).
option(e) :- assigned(x, 4).

% Ensure only one option is true at a time (mutual exclusivity)
:- option(X), option(Y), X != Y.

#show option/1.