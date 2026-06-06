% Domain declarations
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Each student reviews one or more of the three plays
{ reviews(S, P) : play(P) } >= 1 :- student(S).

% Helper to count reviews per student
reviews_count(S, C) :- student(S), C = #count { P : reviews(S, P) }.

% Kramer and Lopez each review fewer plays than Megregian
% Megregian must review strictly more plays than Kramer and Lopez
:- student(S), S = kramer, reviews_count(S, C), reviews_count(megregian, M), C >= M.
:- student(S), S = lopez, reviews_count(S, C), reviews_count(megregian, M), C >= M.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Kramer and O'Neill both review Tamerlane
:- not reviews(kramer, tamerlane).
:- not reviews(oneill, tamerlane).

% Define same_reviews/2: two students have the same set of reviews
same_reviews(S1, S2) :- student(S1), student(S2), S1 < S2,
                        #count { P : reviews(S1, P), reviews(S2, P) } = C1,
                        #count { P : reviews(S1, P) } = C2,
                        #count { P : reviews(S2, P) } = C3,
                        C1 = C2, C1 = C3.

% Exactly two students share the same review set
:- { same_reviews(S1, S2) : student(S1), student(S2), S1 < S2 } != 1.

% Map the correct answer to option/1 (MANDATORY)
% We need to check which option correctly lists students who review Tamerlane

% Option A: Jiang, Kramer
option(a) :- reviews(jiang, tamerlane), reviews(kramer, tamerlane),
             not reviews(lopez, tamerlane), not reviews(megregian, tamerlane), not reviews(oneill, tamerlane).

% Option B: Kramer, O'Neill
option(b) :- reviews(kramer, tamerlane), reviews(oneill, tamerlane),
             not reviews(jiang, tamerlane), not reviews(lopez, tamerlane), not reviews(megregian, tamerlane).

% Option C: Kramer, Lopez, O'Neill
option(c) :- reviews(kramer, tamerlane), reviews(lopez, tamerlane), reviews(oneill, tamerlane),
             not reviews(jiang, tamerlane), not reviews(megregian, tamerlane).

% Option D: Kramer, Megregian, O'Neill
option(d) :- reviews(kramer, tamerlane), reviews(megregian, tamerlane), reviews(oneill, tamerlane),
             not reviews(jiang, tamerlane), not reviews(lopez, tamerlane).

% Option E: Lopez, Megregian, O'Neill
option(e) :- reviews(lopez, tamerlane), reviews(megregian, tamerlane), reviews(oneill, tamerlane),
             not reviews(jiang, tamerlane), not reviews(kramer, tamerlane).

#show option/1.