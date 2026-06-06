% Domain definitions
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Each student reviews one or more plays
{ reviews(S, P) : play(P) } :- student(S).

% At least one play per student
:- student(S), not reviewed_any(S).
reviewed_any(S) :- reviews(S, _).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
num_reviews(S, N) :- student(S), N = #count { P : reviews(S, P) }.
:- num_reviews(kramer, Nk), num_reviews(megregian, Nm), Nk >= Nm.
:- num_reviews(lopez, Nl), num_reviews(megregian, Nm), Nl >= Nm.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition 3: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition 4: Exactly two students review exactly the same play or plays
% Helper to check if two students have identical review sets
same_set(S1, S2) :- student(S1), student(S2), S1 < S2,
                     num_reviews(S1, N), num_reviews(S2, N),
                     common(S1, S2, N).

common(S1, S2, N) :- student(S1), student(S2), S1 < S2,
                      N = #count { P : reviews(S1, P), reviews(S2, P) }.

% Count pairs with same set
pair_count(N) :- N = #count { S1, S2 : same_set(S1, S2) }.
:- pair_count(N), N != 1.  % Exactly one pair (two students)

% Evaluate answer choices
% A: Jiang reviews more plays than Lopez
option(a) :- num_reviews(jiang, Nj), num_reviews(lopez, Nl), Nj > Nl.

% B: Megregian reviews more plays than Jiang
option(b) :- num_reviews(megregian, Nm), num_reviews(jiang, Nj), Nm > Nj.

% C: Megregian reviews more plays than O'Neill
option(c) :- num_reviews(megregian, Nm), num_reviews(oneill, No), Nm > No.

% D: O'Neill reviews more plays than Jiang
option(d) :- num_reviews(oneill, No), num_reviews(jiang, Nj), No > Nj.

% E: O'Neill reviews more plays than Kramer
option(e) :- num_reviews(oneill, No), num_reviews(kramer, Nk), No > Nk.

#show option/1.
#show reviews/2.
#show num_reviews/2.