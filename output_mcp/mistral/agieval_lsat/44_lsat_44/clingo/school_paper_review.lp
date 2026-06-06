% Students and plays
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Each student reviews at least one play, at most three
1 { reviews(S, P) : play(P) } 3 :- student(S).

% Count plays per student
count_plays(S, N) :- N = #count{ P : reviews(S, P) }, student(S).

% Kramer and Lopez each review fewer plays than Megregian
:- count_plays(kramer, N), count_plays(megregian, K), N >= K.
:- count_plays(lopez, N), count_plays(megregian, K), N >= K.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Kramer and O'Neill both review Tamerlane
:- not reviews(kramer, tamerlane).
:- not reviews(oneill, tamerlane).

% Define a review set identifier for each student
% Two students have the same review set if they review exactly the same plays
same_reviews(S1, S2) :- student(S1), student(S2), S1 < S2,
                        reviews(S1, sunset) = reviews(S2, sunset),
                        reviews(S1, tamerlane) = reviews(S2, tamerlane),
                        reviews(S1, undulation) = reviews(S2, undulation).

% There must be exactly one pair of students with same reviews
:- student(S1), student(S2), S1 < S2, not same_reviews(S1, S2), not (student(S3), student(S4), S3 < S4, S3 != S1, S3 != S2, S4 != S1, S4 != S2, same_reviews(S3, S4)).

% Count plays for each student
count_plays(jiang, J) :- J = #count{ P : reviews(jiang, P) }.
count_plays(kramer, K) :- K = #count{ P : reviews(kramer, P) }.
count_plays(lopez, L) :- L = #count{ P : reviews(lopez, P) }.
count_plays(megregian, M) :- M = #count{ P : reviews(megregian, P) }.
count_plays(oneill, O) :- O = #count{ P : reviews(oneill, P) }.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- count_plays(jiang, J), count_plays(lopez, L), J > L.
option(b) :- count_plays(megregian, M), count_plays(jiang, J), M > J.
option(c) :- count_plays(megregian, M), count_plays(oneill, O), M > O.
option(d) :- count_plays(oneill, O), count_plays(jiang, J), O > J.
option(e) :- count_plays(oneill, O), count_plays(kramer, K), O > K.

#show option/1.