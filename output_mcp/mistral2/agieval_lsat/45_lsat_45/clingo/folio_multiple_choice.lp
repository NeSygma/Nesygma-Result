% Domain: Students and Plays
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Helper predicate: student S reviews play P
reviews(S, P) :- student(S), play(P).

% Constraint: Each student reviews at least one play
:- student(S), not reviews(S, _).

% Constraint: Each student reviews only the three specified plays
:- reviews(S, P), not play(P).

% Condition: Kramer and Lopez each review fewer plays than Megregian
% (i.e., |reviews(kramer)| < |reviews(megregian)| and |reviews(lopez)| < |reviews(megregian)|)
num_reviews(S, N) :- N = #count{P : reviews(S, P)}, student(S).
:- num_reviews(kramer, NK), num_reviews(megregian, NM), NK >= NM.
:- num_reviews(lopez, NL), num_reviews(megregian, NM), NL >= NM.

% Condition: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition: Exactly two of the students review exactly the same play or plays as each other
% (i.e., there exists a unique pair of students with identical review sets)

% Helper: Define the set of plays reviewed by each student
reviews_set(S, P) :- reviews(S, P).

% Count how many students review each subset of plays
% We will use a helper predicate to represent the subset of plays reviewed by a student
% Since #set is not supported in standard Clingo, we will use a different approach

% Instead of using #set, we will define a predicate for each possible subset of plays
% and count how many students review that subset.

% Define all possible subsets of plays (non-empty, since each student reviews at least one play)
subset(S, sunset) :- student(S), reviews(S, sunset).
subset(S, tamerlane) :- student(S), reviews(S, tamerlane).
subset(S, undulation) :- student(S), reviews(S, undulation).
subset(S, sunset_tamerlane) :- student(S), reviews(S, sunset), reviews(S, tamerlane).
subset(S, sunset_undulation) :- student(S), reviews(S, sunset), reviews(S, undulation).
subset(S, tamerlane_undulation) :- student(S), reviews(S, tamerlane), reviews(S, undulation).
subset(S, all) :- student(S), reviews(S, sunset), reviews(S, tamerlane), reviews(S, undulation).

% Count the number of students for each subset
count_subset(sunset, N) :- N = #count{S : subset(S, sunset), not subset(S, tamerlane), not subset(S, undulation)}.
count_subset(tamerlane, N) :- N = #count{S : subset(S, tamerlane), not subset(S, sunset), not subset(S, undulation)}.
count_subset(undulation, N) :- N = #count{S : subset(S, undulation), not subset(S, sunset), not subset(S, tamerlane)}.
count_subset(sunset_tamerlane, N) :- N = #count{S : subset(S, sunset_tamerlane), not subset(S, undulation)}.
count_subset(sunset_undulation, N) :- N = #count{S : subset(S, sunset_undulation), not subset(S, tamerlane)}.
count_subset(tamerlane_undulation, N) :- N = #count{S : subset(S, tamerlane_undulation), not subset(S, sunset)}.
count_subset(all, N) :- N = #count{S : subset(S, all)}.

% Exactly one subset is reviewed by exactly two students
:- count_subset(_, 2), not exactly_two_subset.

% Helper to identify the subset reviewed by exactly two students
exactly_two_subset :-
    count_subset(Subset, 2),
    #count{S : subset(S, Subset)} = 2.

% Additional constraint: Exactly three of the students review Undulation
num_undulation_reviews(N) :- N = #count{S : student(S), reviews(S, undulation)}.
:- num_undulation_reviews(N), N != 3.

% --- Multiple Choice Options ---
% (A) Megregian does not review Undulation.
% (B) O'Neill does not review Undulation.
% (C) Jiang reviews Undulation.
% (D) Lopez reviews Tamerlane.
% (E) O'Neill reviews Sunset.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- student(megregian), not reviews(megregian, undulation).
option(b) :- student(oneill), not reviews(oneill, undulation).
option(c) :- student(jiang), reviews(jiang, undulation).
option(d) :- student(lopez), reviews(lopez, tamerlane).
option(e) :- student(oneill), reviews(oneill, sunset).

#show option/1.