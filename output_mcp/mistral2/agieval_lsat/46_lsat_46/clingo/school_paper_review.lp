% Base facts: students and plays
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Each student reviews one or more of the three plays (Sunset, Tamerlane, Undulation)
% We use a choice rule to allow Clingo to assign plays to students
{ reviews(Student, Play) : play(Play) } :- student(Student).

% Ensure each student reviews at least one play
:- student(Student), not reviews(Student, _).

% Megregian reviews all three plays (since Kramer and Lopez review fewer plays than Megregian)
reviews(megregian, sunset).
reviews(megregian, tamerlane).
reviews(megregian, undulation).

% Kramer reviews fewer plays than Megregian, so Kramer reviews at most 2 plays
:- reviews(kramer, sunset), reviews(kramer, tamerlane), reviews(kramer, undulation).

% Lopez reviews fewer plays than Megregian, so Lopez reviews at most 2 plays
:- reviews(lopez, sunset), reviews(lopez, tamerlane), reviews(lopez, undulation).

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, Play), reviews(lopez, Play).
:- reviews(jiang, Play), reviews(megregian, Play).

% Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Define a helper predicate to represent the set of plays reviewed by each student
% We use a sorted list of plays to represent the set
review_set(Student, sunset) :- reviews(Student, sunset), not reviews(Student, tamerlane), not reviews(Student, undulation).
review_set(Student, tamerlane) :- reviews(Student, tamerlane), not reviews(Student, sunset), not reviews(Student, undulation).
review_set(Student, undulation) :- reviews(Student, undulation), not reviews(Student, sunset), not reviews(Student, tamerlane).
review_set(Student, sunset_tamerlane) :- reviews(Student, sunset), reviews(Student, tamerlane), not reviews(Student, undulation).
review_set(Student, sunset_undulation) :- reviews(Student, sunset), reviews(Student, undulation), not reviews(Student, tamerlane).
review_set(Student, tamerlane_undulation) :- reviews(Student, tamerlane), reviews(Student, undulation), not reviews(Student, sunset).
review_set(Student, all) :- reviews(Student, sunset), reviews(Student, tamerlane), reviews(Student, undulation).

% Count the number of pairs of students who share the same set of plays reviewed
same_plays(Student1, Student2) :-
    student(Student1), student(Student2),
    Student1 != Student2,
    review_set(Student1, Set),
    review_set(Student2, Set).

% Ensure exactly one pair of students share the same set of plays reviewed
:- #count{ S1, S2 : same_plays(S1, S2) } != 1.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- reviews(jiang, tamerlane), reviews(kramer, tamerlane), not reviews(lopez, tamerlane), not reviews(megregian, tamerlane), not reviews(oneill, tamerlane).
option(b) :- not reviews(jiang, tamerlane), reviews(kramer, tamerlane), not reviews(lopez, tamerlane), not reviews(megregian, tamerlane), reviews(oneill, tamerlane).
option(c) :- not reviews(jiang, tamerlane), reviews(kramer, tamerlane), reviews(lopez, tamerlane), not reviews(megregian, tamerlane), reviews(oneill, tamerlane).
option(d) :- not reviews(jiang, tamerlane), reviews(kramer, tamerlane), not reviews(lopez, tamerlane), reviews(megregian, tamerlane), reviews(oneill, tamerlane).
option(e) :- not reviews(jiang, tamerlane), not reviews(kramer, tamerlane), reviews(lopez, tamerlane), reviews(megregian, tamerlane), reviews(oneill, tamerlane).

#show option/1.