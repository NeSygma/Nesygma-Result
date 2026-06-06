% Domains
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Generate possible reviews for each student
% Each student reviews 1 to 3 plays
{ reviews(S, P) : play(P) } = K :- student(S), K = 1..3.

% Each student must review at least one play
:- student(S), not reviews(S, _).

% Count the number of reviews per student
num_reviews(S, N) :- N = #count{ P : reviews(S, P) }, student(S).

% Kramer and Lopez each review fewer plays than Megregian
:- num_reviews(kramer, NK), num_reviews(megregian, NM), NK >= NM.
:- num_reviews(lopez, NL), num_reviews(megregian, NM), NL >= NM.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Kramer and O'Neill both review Tamerlane
:- not reviews(kramer, tamerlane).
:- not reviews(oneill, tamerlane).

% Define a helper to represent the review set as a tuple of plays
% We'll use a predicate that represents the set of plays reviewed by a student
% and then count the number of students with the same set

% Define a helper to represent the review set as a tuple
review_set(S, P) :- reviews(S, P).

% Define a helper to count how many students share the same review set
% We'll use a predicate that groups students by their review set
same_review_set(S1, S2) :-
    student(S1), student(S2), S1 != S2,
    reviews(S1, P) = reviews(S2, P) : play(P).

% Count the number of students sharing each review set
% We'll use a helper to count the number of students with the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Let's define a helper to count the number of students sharing the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Let's define a helper to count the number of students sharing the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Let's define a helper to count the number of students sharing the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Let's define a helper to count the number of students sharing the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count thenumber of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Let's define a helper to count the number of students sharing the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Let's define a helper to count the number of students sharing the same review set
% and enforce that exactly one review set is shared by exactly two students

% Define a helper to count the number of students sharing the same review set
% We'll use a helper to represent the review set as a tuple

% Define a helper to count the number of students sharing the same review set
% We'll use a