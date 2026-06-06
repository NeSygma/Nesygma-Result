% Students and plays
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Each student reviews one or more plays (choice rule)
{ reviews(Student, Play) : play(Play) } >= 1 :- student(Student).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
num_reviews(Student, N) :- N = #count{Play : reviews(Student, Play)}, student(Student).
:- num_reviews(kramer, K), num_reviews(megregian, M), K >= M.
:- num_reviews(lopez, L), num_reviews(megregian, M), L >= M.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(lopez, Play), reviews(jiang, Play).
:- reviews(megregian, Play), reviews(jiang, Play).

% Condition 3: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition 4: Exactly two students review exactly the same set of plays
% We'll use a simpler approach: enumerate all possible play sets and count students with each set
% Define all possible play sets (there are 2^3 - 1 = 7 non-empty subsets)
set(sunset). set(tamerlane). set(undulation).
set(sunset_tamerlane). set(sunset_undulation). set(tamerlane_undulation). set(all_three).

% Helper: check if a student's reviews match a set
matches_set(Student, sunset) :- reviews(Student, sunset), not reviews(Student, tamerlane), not reviews(Student, undulation).
matches_set(Student, tamerlane) :- reviews(Student, tamerlane), not reviews(Student, sunset), not reviews(Student, undulation).
matches_set(Student, undulation) :- reviews(Student, undulation), not reviews(Student, sunset), not reviews(Student, tamerlane).
matches_set(Student, sunset_tamerlane) :- reviews(Student, sunset), reviews(Student, tamerlane), not reviews(Student, undulation).
matches_set(Student, sunset_undulation) :- reviews(Student, sunset), reviews(Student, undulation), not reviews(Student, tamerlane).
matches_set(Student, tamerlane_undulation) :- reviews(Student, tamerlane), reviews(Student, undulation), not reviews(Student, sunset).
matches_set(Student, all_three) :- reviews(Student, sunset), reviews(Student, tamerlane), reviews(Student, undulation).

% Count students for each set
count_set(Set, N) :- N = #count{Student : matches_set(Student, Set)}, set(Set).

% Exactly two students share the same set
:- not 1 { count_set(Set, 2) : set(Set) } 1.

% Additional constraint: Jiang does not review Tamerlane
:- reviews(jiang, tamerlane).

% Map the correct answer to option/1
% A: Jiang reviews Sunset
option(a) :- reviews(jiang, sunset).

% B: Lopez reviews Undulation
option(b) :- reviews(lopez, undulation).

% C: Megregian reviews Sunset
option(c) :- reviews(megregian, sunset).

% D: Megregian reviews Tamerlane
option(d) :- reviews(megregian, tamerlane).

% E: O'Neill reviews Undulation
option(e) :- reviews(oneill, undulation).

#show option/1.