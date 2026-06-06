% Students and plays
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Each student reviews at least one and at most three plays
1 { review(S,P) : play(P) } 3 :- student(S).

% Forced reviews
review(kramer, tamerlane).
review(oneill, tamerlane).

% Lopez and Megregian do not review any play Jiang reviews
:- review(jiang, P), review(lopez, P).
:- review(jiang, P), review(megregian, P).

% Count number of reviews per student
count_reviews(S,N) :- student(S), N = #count { P : review(S,P) }.

% Kramer and Lopez each review fewer plays than Megregian
:- count_reviews(kramer, K), count_reviews(megregian, M), K >= M.
:- count_reviews(lopez, L), count_reviews(megregian, M), L >= M.

% Define when two students have different review sets
diff(A,B) :- student(A), student(B), A != B, review(A,P), not review(B,P).

diff(A,B) :- student(A), student(B), A != B, review(B,P), not review(A,P).

% Same set (unordered pair)
same_set(A,B) :- student(A), student(B), A < B, not diff(A,B).

% Count number of pairs with same set
pair_count(N) :- N = #count { A,B : same_set(A,B) }.
:- pair_count(N), N != 1.

% Options for Tamerlane reviewers
option(a) :- review(jiang, tamerlane), review(kramer, tamerlane), not review(lopez, tamerlane), not review(megregian, tamerlane), not review(oneill, tamerlane).
option(b) :- review(kramer, tamerlane), review(oneill, tamerlane), not review(jiang, tamerlane), not review(lopez, tamerlane), not review(megregian, tamerlane).
option(c) :- review(kramer, tamerlane), review(lopez, tamerlane), review(oneill, tamerlane), not review(jiang, tamerlane), not review(megregian, tamerlane).
option(d) :- review(kramer, tamerlane), review(megregian, tamerlane), review(oneill, tamerlane), not review(jiang, tamerlane), not review(lopez, tamerlane).
option(e) :- review(lopez, tamerlane), review(megregian, tamerlane), review(oneill, tamerlane), not review(jiang, tamerlane), not review(kramer, tamerlane).

% Exactly one option must be true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.