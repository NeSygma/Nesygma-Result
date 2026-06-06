% Base facts
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Given constraint: Z is mentioned in chapter 7
assigned(z, 7).

% Each clue in exactly one chapter
{ assigned(C, Ch) : chapter(Ch) } 1 :- clue(C).

% Each chapter has exactly one clue
{ assigned(C, Ch) : clue(C) } 1 :- chapter(Ch).

% Ensure all chapters and clues are assigned
:- chapter(Ch), not assigned(_, Ch).
:- clue(C), not assigned(C, _).

% T cannot be in chapter 1
:- assigned(t, 1).

% T must be before W with exactly 2 chapters separating them
% If T is in chapter ChT, W must be in chapter ChT + 3
:- assigned(t, ChT), assigned(w, ChW), ChW != ChT + 3.
:- assigned(t, ChT), assigned(w, ChW), ChT >= ChW.

% S and Z cannot be adjacent (Z is fixed in chapter 7)
:- assigned(s, ChS), abs(ChS - 7) = 1.

% W and X cannot be adjacent
:- assigned(w, ChW), assigned(x, ChX), abs(ChW - ChX) = 1.

% U and X must be adjacent
:- assigned(u, ChU), assigned(x, ChX), abs(ChU - ChX) != 1.

% Define which options are possible based on the constraints
% Option A: R is mentioned in chapter 3
possible_a :- assigned(r, 3).

% Option B: S is mentioned in chapter 3
possible_b :- assigned(s, 3).

% Option C: T is mentioned in chapter 4
possible_c :- assigned(t, 4).

% Option D: U is mentioned in chapter 1
possible_d :- assigned(u, 1).

% Option E: X is mentioned in chapter 5
possible_e :- assigned(x, 5).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- possible_a.
option(b) :- possible_b.
option(c) :- possible_c.
option(d) :- possible_d.
option(e) :- possible_e.

#show option/1.