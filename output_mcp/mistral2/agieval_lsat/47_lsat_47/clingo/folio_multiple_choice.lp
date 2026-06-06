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
% We represent this as a relation: reviews(Student, Play)

% Base constraints:
% 1. Each student reviews at least one play
{reviews(Student, Play) : play(Play)} 1 :- student(Student).

% 2. Each student reviews at most three plays (implicitly enforced by the choice rule)

% Condition 1: Kramer and Lopez each review fewer of the plays than Megregian
% This means the number of plays reviewed by Kramer < number reviewed by Megregian
% and the number of plays reviewed by Lopez < number reviewed by Megregian
num_plays_reviewed(S, N) :- N = #count{Play : reviews(S, Play)}, student(S).
:- student(kramer), student(megregian), num_plays_reviewed(kramer, N1), num_plays_reviewed(megregian, N2), N1 >= N2.
:- student(lopez), student(megregian), num_plays_reviewed(lopez, N1), num_plays_reviewed(megregian, N2), N1 >= N2.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, Play), reviews(lopez, Play).
:- reviews(jiang, Play), reviews(megregian, Play).

% Condition 3: Kramer and O'Neill both review Tamerlane
:- student(kramer), not reviews(kramer, tamerlane).
:- student(oneill), not reviews(oneill, tamerlane).

% Condition 4: Exactly two of the students review exactly the same play or plays as each other
% We need to find a pair of students who review exactly the same set of plays
% and ensure that exactly one such pair exists.

% Helper: same_reviews(S1, S2) means S1 and S2 review exactly the same plays
same_reviews(S1, S2) :- student(S1), student(S2), S1 != S2,
                        num_plays_reviewed(S1, N), num_plays_reviewed(S2, N),
                        #count{Play : reviews(S1, Play), reviews(S2, Play)} = N.

% Exactly one pair of students reviews the same set of plays
:- {same_reviews(S1, S2) : student(S1), student(S2), S1 < S2} != 1.

% Additional constraint: Jiang does not review Tamerlane
:- reviews(jiang, tamerlane).

% --- Answer mapping ---
% Now, we need to determine which of the options (A-E) must be true given the constraints.

% We will define conditions for each option and map them to option/1.

% (A) Jiang reviews Sunset
option(a) :- reviews(jiang, sunset).

% (B) Lopez reviews Undulation
option(b) :- reviews(lopez, undulation).

% (C) Megregian reviews Sunset
option(c) :- reviews(megregian, sunset).

% (D) Megregian reviews Tamerlane
option(d) :- reviews(megregian, tamerlane).

% (E) O'Neill reviews Undulation
option(e) :- reviews(oneill, undulation).

#show option/1.