% Domain
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Each student reviews 1 to 3 plays
1 { reviews(S, P) : play(P) } 3 :- student(S).

% Condition 4: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Count of plays each student reviews
review_count(S, N) :- student(S), N = #count { P : play(P), reviews(S, P) }.

% Condition 1: Kramer reviews fewer plays than Megregian
:- review_count(kramer, N1), review_count(megregian, N2), N1 >= N2.

% Condition 2: Lopez reviews fewer plays than Megregian
:- review_count(lopez, N1), review_count(megregian, N2), N1 >= N2.

% Condition 3: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition 5: Exactly one pair of students has the same review set
same_set(S1, S2) :- student(S1), student(S2), S1 < S2, not diff(S1, S2).
diff(S1, S2) :- student(S1), student(S2), S1 < S2, play(P), reviews(S1, P), not reviews(S2, P).
diff(S1, S2) :- student(S1), student(S2), S1 < S2, play(P), not reviews(S1, P), reviews(S2, P).
:- #count { S1, S2 : same_set(S1, S2) } != 1.

% Question condition: Exactly 3 students review Undulation
:- #count { S : reviews(S, undulation) } != 3.

% Check each option
cond_a :- not reviews(megregian, undulation).
cond_b :- not reviews(oneill, undulation).
cond_c :- reviews(jiang, undulation).
cond_d :- reviews(lopez, tamerlane).
cond_e :- reviews(oneill, sunset).

option(a) :- cond_a.
option(b) :- cond_b.
option(c) :- cond_c.
option(d) :- cond_d.
option(e) :- cond_e.

#show option/1.
#show reviews/2.