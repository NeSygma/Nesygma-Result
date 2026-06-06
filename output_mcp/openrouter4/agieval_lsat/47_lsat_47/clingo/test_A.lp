% Define domain
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Choice: each student may review each play
{ reviews(S,P) } :- student(S), play(P).

% Each student reviews at least one play
:- student(S), #count{ P : reviews(S,P) } < 1.

% Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Kramer and Lopez each review fewer plays than Megregian
count_reviews(S, N) :- student(S), N = #count{ P : reviews(S,P) }.
:- count_reviews(kramer, K), count_reviews(megregian, M), K >= M.
:- count_reviews(lopez, L), count_reviews(megregian, M), L >= M.

% Exactly two students have exactly the same review set
different(S1, S2) :- student(S1), student(S2), S1 != S2, play(P), reviews(S1,P), not reviews(S2,P).
different(S1, S2) :- student(S1), student(S2), S1 != S2, play(P), not reviews(S1,P), reviews(S2,P).

same_reviews(S1, S2) :- student(S1), student(S2), S1 < S2, not different(S1, S2), not different(S2, S1).

pair_count(N) :- N = #count{ S1,S2 : same_reviews(S1,S2) }.
:- pair_count(N), N != 1.

% Given: Jiang does NOT review Tamerlane
:- reviews(jiang, tamerlane).

% Test A negation: Jiang does NOT review Sunset
:- not reviews(jiang, sunset).

#show reviews/2.