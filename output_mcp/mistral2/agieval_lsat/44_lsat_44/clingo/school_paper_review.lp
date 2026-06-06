% Define the students and plays
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Each student reviews one or more of exactly three plays
% We represent the reviews as a relation: reviews(Student, Play)

% Base facts: Each student reviews at least one play
% (This will be enforced by the constraints below)

% Constraints:

% 1. Kramer and Lopez each review fewer of the plays than Megregian.
% We need to count the number of plays each student reviews.

% Helper predicate: count the number of plays reviewed by a student
num_plays_reviewed(S, N) :-
    student(S),
    N = #count { P : play(P), reviews(S, P) }.

% Kramer reviews fewer plays than Megregian
:- num_plays_reviewed(kramer, NK), num_plays_reviewed(megregian, NM), NK >= NM.

% Lopez reviews fewer plays than Megregian
:- num_plays_reviewed(lopez, NL), num_plays_reviewed(megregian, NM), NL >= NM.

% 2. Neither Lopez nor Megregian reviews any play Jiang reviews.
% This means: If Jiang reviews a play, Lopez and Megregian do not review it.
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% 3. Kramer and O'Neill both review Tamerlane.
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% 4. Exactly two of the students review exactly the same play or plays as each other.
% We need to find pairs of students who review the same set of plays.

% Helper predicate: same_plays(S1, S2) means S1 and S2 review the same set of plays
same_plays(S1, S2) :-
    student(S1),
    student(S2),
    S1 != S2,
    num_plays_reviewed(S1, N1),
    num_plays_reviewed(S2, N2),
    N1 = N2,
    #count { P : reviews(S1, P) } = N1,
    #count { P : reviews(S2, P) } = N2,
    #count { P : reviews(S1, P), reviews(S2, P) } = N1.

% Exactly two students review the same set of plays
% We count the number of pairs (S1, S2) with S1 < S2 and same_plays(S1, S2)
% and ensure there is exactly one such pair (since each pair is counted once).

% Count the number of pairs with same_plays
num_same_pairs(N) :-
    N = #count { S1, S2 : student(S1), student(S2), S1 < S2, same_plays(S1, S2) }.

:- num_same_pairs(N), N != 1.

% Generate possible reviews for each student (one or more plays)
% We allow each student to review any subset of the three plays
{ reviews(S, P) : play(P) } :- student(S).

% Ensure each student reviews at least one play
:- student(S), not reviews(S, _).

% Map the correct answer to option/1 (MANDATORY)
% We need to evaluate the conditions for each option and see which one must be true

% Option A: Jiang reviews more plays than Lopez
option(a) :- num_plays_reviewed(jiang, NJ), num_plays_reviewed(lopez, NL), NJ > NL.

% Option B: Megregian reviews more plays than Jiang
option(b) :- num_plays_reviewed(megregian, NM), num_plays_reviewed(jiang, NJ), NM > NJ.

% Option C: Megregian reviews more plays than O'Neill
option(c) :- num_plays_reviewed(megregian, NM), num_plays_reviewed(oneill, NO), NM > NO.

% Option D: O'Neill reviews more plays than Jiang
option(d) :- num_plays_reviewed(oneill, NO), num_plays_reviewed(jiang, NJ), NO > NJ.

% Option E: O'Neill reviews more plays than Kramer
option(e) :- num_plays_reviewed(oneill, NO), num_plays_reviewed(kramer, NK), NO > NK.

#show option/1.