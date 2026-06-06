% Define the time positions and compositions
position(1..8).
composition(f;h;l;o;p;r;s;t).

% Each position has exactly one composition
1 { performed(C, P) : composition(C) } 1 :- position(P).

% Each composition is performed exactly once
1 { performed(C, P) : position(P) } 1 :- composition(C).

% Given scenario constraints
performed(p, 3).
performed(s, 6).

% Constraint 1: T is performed either immediately before F or immediately after R
% This means: (T at P and F at P+1) OR (R at P and T at P+1)
:- performed(t, P), performed(f, P+1), P+1 <= 8.
:- performed(r, P), performed(t, P+1), P+1 <= 8.

% Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
% This means: |position(F) - position(R)| >= 3
:- performed(f, P1), performed(r, P2), abs(P1 - P2) < 3, P1 != P2.

% Constraint 3: O is performed either first or fifth
:- performed(o, P), P != 1, P != 5.

% Constraint 4: The eighth composition performed is either L or H
:- performed(C, 8), C != l, C != h.

% Constraint 5: P is performed at some time before S
:- performed(p, P1), performed(s, P2), P1 >= P2.

% Constraint 6: At least one composition is performed either after O and before S, or after S and before O
% This means: |position(O) - position(S)| >= 2
:- performed(o, P1), performed(s, P2), abs(P1 - P2) < 2, P1 != P2.

% Derive what must be at position 5
% If position 5 is F, then we need to check consistency
% If position 5 is H, then we need to check consistency
% If position 5 is L, then we need to check consistency
% If position 5 is O, then we need to check consistency
% If position 5 is R, then we need to check consistency
% If position 5 is S, then we need to check consistency
% If position 5 is T, then we need to check consistency

% Let's define what it means for each option to be correct
% We need to find which option(s) are possible for position 5

% Option A: position 5 is F or H
possible_a :- performed(f, 5).
possible_a :- performed(h, 5).

% Option B: position 5 is F or O
possible_b :- performed(f, 5).
possible_b :- performed(o, 5).

% Option C: position 5 is F or T
possible_c :- performed(f, 5).
possible_c :- performed(t, 5).

% Option D: position 5 is H or L
possible_d :- performed(h, 5).
possible_d :- performed(l, 5).

% Option E: position 5 is O or R
possible_e :- performed(o, 5).
possible_e :- performed(r, 5).

% Only one option can be the correct answer
% We need to determine which option is necessarily true

% Since we want to find which option MUST be correct (i.e., position 5 must be one of the pairs),
% we need to check which options are satisfied by ALL valid models

% Let's find the unique solution first

% Additional constraint: enforce uniqueness by finding the stable model

% Map the correct answer to option/1
% We need to determine which option is correct based on the constraints

% Let's derive the answer by checking which option is satisfied
answer(a) :- possible_a, not possible_b, not possible_c, not possible_d, not possible_e.
answer(b) :- possible_b, not possible_a, not possible_c, not possible_d, not possible_e.
answer(c) :- possible_c, not possible_a, not possible_b, not possible_d, not possible_e.
answer(d) :- possible_d, not possible_a, not possible_b, not possible_c, not possible_e.
answer(e) :- possible_e, not possible_a, not possible_b, not possible_c, not possible_d.

% If multiple are possible, we need to refine
% If none are possible, we need to refine

#show answer/1.