% Define the domain
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Assign each clue to exactly one chapter
{ clue_in_chapter(C, Ch) : chapter(Ch) } = 1 :- clue(C).
{ clue_in_chapter(C, Ch) : clue(C) } = 1 :- chapter(Ch).

% Constraints
% 1. T cannot be in chapter 1
:- clue_in_chapter(t, 1).

% 2. T must be before W with exactly two chapters separating them
% If T is in chapter Ch, then W must be in chapter Ch+3
:- clue_in_chapter(t, Ch), clue_in_chapter(w, WCh), WCh != Ch + 3.

% 3. S and Z cannot be adjacent
:- clue_in_chapter(s, Ch), clue_in_chapter(z, Ch+1).
:- clue_in_chapter(s, Ch), clue_in_chapter(z, Ch-1).
:- clue_in_chapter(z, Ch), clue_in_chapter(s, Ch+1).
:- clue_in_chapter(z, Ch), clue_in_chapter(s, Ch-1).

% 4. W and X cannot be adjacent
:- clue_in_chapter(w, Ch), clue_in_chapter(x, Ch+1).
:- clue_in_chapter(w, Ch), clue_in_chapter(x, Ch-1).
:- clue_in_chapter(x, Ch), clue_in_chapter(w, Ch+1).
:- clue_in_chapter(x, Ch), clue_in_chapter(w, Ch-1).

% 5. U and X must be adjacent
:- clue_in_chapter(u, UCh), clue_in_chapter(x, XCh), abs(UCh - XCh) != 1.

% Given condition: X is in chapter 1
:- not clue_in_chapter(x, 1).

% Map options to conditions
% A: R is mentioned in chapter 3
option(a) :- clue_in_chapter(r, 3).

% B: R is mentioned in chapter 7
option(b) :- clue_in_chapter(r, 7).

% C: S is mentioned in chapter 2
option(c) :- clue_in_chapter(s, 2).

% D: W is mentioned in chapter 5
option(d) :- clue_in_chapter(w, 5).

% E: Z is mentioned in chapter 3
option(e) :- clue_in_chapter(z, 3).

#show option/1.

% Optional: Add a sentinel to ensure a model is returned if one exists
solution_exists :- option(_).
#show solution_exists/0.