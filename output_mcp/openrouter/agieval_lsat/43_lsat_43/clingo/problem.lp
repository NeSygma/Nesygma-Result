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

% Fixed reviews
review(kramer,tamerlane).
review(oneill,tamerlane).

% Cardinality counts
cnt(S,N) :- N = #count{ P : review(S,P) }.

% Kramer and Lopez review fewer plays than Megregian
:- cnt(kramer,Nk), cnt(megregian,Nm), Nk >= Nm.
:- cnt(lopez,Nl), cnt(megregian,Nm), Nl >= Nm.

% Lopez and Megregian share no play with Jiang
:- review(lopez,P), review(jiang,P).
:- review(megregian,P), review(jiang,P).

% Define diff and same_set for identical review sets
diff(X,Y) :- review(X,P), not review(Y,P).
diff(X,Y) :- review(Y,P), not review(X,P).

same_set(X,Y) :- student(X), student(Y), X < Y, not diff(X,Y).

% Exactly one pair of students have identical review sets
pair_count(N) :- N = #count{ X,Y : same_set(X,Y), X<Y }.
:- pair_count(N), N != 1.

% Only Sunset predicate
only_sunset(S) :- review(S,sunset), not review(S,tamerlane), not review(S,undulation).

% Options conditions
option(a) :- only_sunset(lopez), not only_sunset(jiang), not only_sunset(kramer), not only_sunset(oneill), not only_sunset(megregian).
option(b) :- only_sunset(oneill), not only_sunset(jiang), not only_sunset(kramer), not only_sunset(lopez), not only_sunset(megregian).
option(c) :- only_sunset(jiang), only_sunset(lopez), not only_sunset(kramer), not only_sunset(oneill), not only_sunset(megregian).
option(d) :- only_sunset(kramer), only_sunset(oneill), not only_sunset(jiang), not only_sunset(lopez), not only_sunset(megregian).
option(e) :- only_sunset(lopez), only_sunset(megregian), not only_sunset(jiang), not only_sunset(kramer), not only_sunset(oneill).

% Exactly one option must hold
:- #count{ X : option(X) } != 1.

#show option/1.