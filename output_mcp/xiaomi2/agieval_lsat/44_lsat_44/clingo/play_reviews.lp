% Domains
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Each student reviews 1 to 3 plays
1 { review(S, P) : play(P) } 3 :- student(S).

% Constraint 3: Kramer and O'Neill both review Tamerlane
review(kramer, tamerlane).
review(oneill, tamerlane).

% Constraint 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- review(jiang, P), review(lopez, P).
:- review(jiang, P), review(megregian, P).

% Count reviews per student
count(S, N) :- student(S), N = #count{P : play(P), review(S, P)}.

% Constraint 1: Kramer and Lopez each review fewer plays than Megregian
:- count(kramer, Nk), count(megregian, Nm), Nk >= Nm.
:- count(lopez, Nl), count(megregian, Nm), Nl >= Nm.

% Constraint 4: Exactly two students review the same set of plays
% Define "different set" - exists a play where they disagree
diff(S1, S2) :- student(S1), student(S2), S1 < S2, play(P), review(S1, P), not review(S2, P).
diff(S1, S2) :- student(S1), student(S2), S1 < S2, play(P), not review(S1, P), review(S2, P).
% Same set = no differences
same(S1, S2) :- student(S1), student(S2), S1 < S2, not diff(S1, S2).

% Exactly one pair has the same set
:- #count{S1,S2 : same(S1,S2)} != 1.

% Check each option
holds_a :- count(jiang, Nj), count(lopez, Nl), Nj > Nl.
holds_b :- count(megregian, Nm), count(jiang, Nj), Nm > Nj.
holds_c :- count(megregian, Nm), count(oneill, No), Nm > No.
holds_d :- count(oneill, No), count(jiang, Nj), No > Nj.
holds_e :- count(oneill, No), count(kramer, Nk), No > Nk.

#show review/2.
#show count/2.
#show holds_a/0.
#show holds_b/0.
#show holds_c/0.
#show holds_d/0.
#show holds_e/0.