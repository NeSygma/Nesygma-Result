% Define domain
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Choice: each student may review each play
{ reviews(S,P) } :- student(S), play(P).

% Each student reviews at least one play
:- student(S), #count{ P : reviews(S,P) } < 1.

% Constraint: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane) :- true.
reviews(oneill, tamerlane) :- true.

% Constraint: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Constraint: Kramer and Lopez each review fewer plays than Megregian
count_reviews(S, N) :- student(S), N = #count{ P : reviews(S,P) }.
:- count_reviews(kramer, K), count_reviews(megregian, M), K >= M.
:- count_reviews(lopez, L), count_reviews(megregian, M), L >= M.

% Constraint: Exactly two students (one pair) have exactly the same review set
% Define when two students differ (there exists a play one reviews and the other doesn't)
different(S1, S2) :- student(S1), student(S2), S1 != S2, play(P), reviews(S1,P), not reviews(S2,P).
different(S1, S2) :- student(S1), student(S2), S1 != S2, play(P), not reviews(S1,P), reviews(S2,P).

% Same reviews if not different
same_reviews(S1, S2) :- student(S1), student(S2), S1 < S2, not different(S1, S2), not different(S2, S1).

% Exactly one pair has same reviews
pair_count(N) :- N = #count{ S1,S2 : same_reviews(S1,S2) }.
:- pair_count(N), N != 1.

% Given condition: Jiang does NOT review Tamerlane
:- reviews(jiang, tamerlane).

% Show results
#show reviews/2.
#show same_reviews/2.