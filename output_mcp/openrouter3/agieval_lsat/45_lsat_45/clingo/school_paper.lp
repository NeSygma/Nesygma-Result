% Students and plays
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Each student reviews one or more plays (choice rule)
{ reviews(Student, Play) : play(Play) } >= 1 :- student(Student).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
count_reviews(Student, N) :- N = #count{Play : reviews(Student, Play)}, student(Student).
:- count_reviews(kramer, K), count_reviews(megregian, M), K >= M.
:- count_reviews(lopez, L), count_reviews(megregian, M), L >= M.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(lopez, Play), reviews(jiang, Play).
:- reviews(megregian, Play), reviews(jiang, Play).

% Condition 3: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition 4: Exactly two students review exactly the same set of plays
% Create a unique identifier for each student's play set
% We'll use a helper predicate to check if two students have identical play sets
same_set(S1, S2) :- S1 != S2, student(S1), student(S2),
    reviews(S1, P) : play(P) == reviews(S2, P) : play(P).

% Count how many pairs have the same set
same_set_count(N) :- N = #count{S1, S2 : same_set(S1, S2)}.

% Exactly two students share the same set (i.e., exactly one pair)
:- same_set_count(N), N != 1.

% Additional constraint: Exactly three students review Undulation
count_undulation(N) :- N = #count{Student : reviews(Student, undulation)}, student(Student).
:- count_undulation(N), N != 3.

% Evaluate answer choices
% (A) Megregian does not review Undulation
answer_a :- not reviews(megregian, undulation).

% (B) O'Neill does not review Undulation
answer_b :- not reviews(oneill, undulation).

% (C) Jiang reviews Undulation
answer_c :- reviews(jiang, undulation).

% (D) Lopez reviews Tamerlane
answer_d :- reviews(lopez, tamerlane).

% (E) O'Neill reviews Sunset
answer_e :- reviews(oneill, sunset).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

#show option/1.