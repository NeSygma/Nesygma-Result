% Students and plays
student(jiang).
student(kramer).
student(lopez).
student(megregian).
student(oneill).

play(sunset).
play(tamerlane).
play(undulation).

% Choice of reviews (each student reviews any subset of plays, non-empty enforced later)
{review(S,P)} :- student(S), play(P).

% Each student reviews at least one play
:- student(S), not review(S,sunset), not review(S,tamerlane), not review(S,undulation).

% Kramer and O'Neill both review Tamerlane
review(kramer, tamerlane).
review(oneill, tamerlane).

% Kramer and Lopez each review fewer plays than Megregian
% Count reviews per student
cnt(S,N) :- student(S), N = #count{P : review(S,P)}.
% Enforce fewer
:- cnt(kramer,Nk), cnt(megregian,Nm), Nk >= Nm.
:- cnt(lopez,Nl), cnt(megregian,Nm2), Nl >= Nm2.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- review(jiang,P), review(lopez,P).
:- review(jiang,P), review(megregian,P).

% Exactly two students have identical review sets, and no other duplicates
% Define difference between two students
diff(S1,S2) :- student(S1), student(S2), S1 < S2, play(P), (review(S1,P), not review(S2,P)); (review(S2,P), not review(S1,P)).
% same_set holds when no diff
same_set(S1,S2) :- student(S1), student(S2), S1 < S2, not diff(S1,S2).
% Exactly one pair same_set
:- #count{S1,S2 : same_set(S1,S2)} != 1.

% Option definitions based on who reviews Tamerlane
% Helper to check not reviewing Tamerlane
not_review(S) :- not review(S,tamerlane).

option(a) :- review(jiang,tamerlane), review(kramer,tamerlane), not_review(lopez), not_review(megregian), not_review(oneill).
option(b) :- review(kramer,tamerlane), review(oneill,tamerlane), not_review(jiang), not_review(lopez), not_review(megregian).
option(c) :- review(kramer,tamerlane), review(lopez,tamerlane), review(oneill,tamerlane), not_review(jiang), not_review(megregian).
option(d) :- review(kramer,tamerlane), review(megregian,tamerlane), review(oneill,tamerlane), not_review(jiang), not_review(lopez).
option(e) :- review(lopez,tamerlane), review(megregian,tamerlane), review(oneill,tamerlane), not_review(jiang), not_review(kramer).

#show option/1.