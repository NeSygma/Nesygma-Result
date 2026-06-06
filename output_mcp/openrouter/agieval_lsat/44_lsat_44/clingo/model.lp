% Students
student(jiang).
student(kramer).
student(lopez).
student(meg).
student(oneill).

% Plays
play(sunset).
play(tamerlane).
play(undulation).

% Each student reviews at least one and at most three plays
1 { reviews(S,P) : play(P) } 3 :- student(S).

% Fixed reviews
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Size of review set for each student
size(S,N) :- student(S), N = #count { P : reviews(S,P) }.

% Kramer and Lopez each review fewer plays than Megregian
:- size(kramer,Nk), size(meg,Nm), Nk >= Nm.
:- size(lopez,Nl), size(meg,Nm), Nl >= Nm.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang,P), reviews(lopez,P).
:- reviews(jiang,P), reviews(meg,P).

% Define diff between two students (they differ on at least one play)
diff(A,B) :- student(A), student(B), A != B, reviews(A,P), not reviews(B,P).

% Ordering for unordered pairs (lexicographic)
less(jiang,kramer). less(jiang,lopez). less(jiang,meg). less(jiang,oneill).
less(kramer,lopez). less(kramer,meg). less(kramer,oneill).
less(lopez,meg). less(lopez,oneill).
less(meg,oneill).

% Equality of review sets for a pair
eq_pair(A,B) :- less(A,B), not diff(A,B).

% Exactly one pair of students have identical review sets (i.e., exactly two students share the same set)
:- #count { A,B : eq_pair(A,B) } != 1.

% Option conditions
option(a) :- size(jiang,Nj), size(lopez,Nl), Nj > Nl.
option(b) :- size(meg,Nm), size(jiang,Nj), Nm > Nj.
option(c) :- size(meg,Nm), size(oneill,No), Nm > No.
option(d) :- size(oneill,No), size(jiang,Nj), No > Nj.
option(e) :- size(oneill,No), size(kramer,Nk), No > Nk.

% Exactly one option must be true
:- not option(a), not option(b), not option(c), not option(d), not option(e).
:- #count { X : option(X) } > 1.

#show option/1.