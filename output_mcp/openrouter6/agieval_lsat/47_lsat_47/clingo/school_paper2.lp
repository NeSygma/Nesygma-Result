% Students and plays
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Each student reviews at least one play (and only these three)
1 { reviews(S, P) : play(P) } :- student(S).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
count(S, N) :- N = #count{ P : reviews(S, P) }, student(S).
:- count(kramer, Nk), count(megregian, Nm), Nk >= Nm.
:- count(lopez, Nl), count(megregian, Nm), Nl >= Nm.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition 3: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition 4: Exactly two students review exactly the same set of plays
same_set(S1, S2) :- student(S1), student(S2), S1 != S2,
    #count{ P : reviews(S1, P), not reviews(S2, P) } = 0,
    #count{ P : reviews(S2, P), not reviews(S1, P) } = 0.
pair_count(N) :- N = #count{ S1, S2 : same_set(S1, S2), S1 < S2 }.
:- pair_count(N), N != 1.

% Extra condition: Jiang does not review Tamerlane
:- reviews(jiang, tamerlane).

% Answer choices
answer_a :- reviews(jiang, sunset).
answer_b :- reviews(lopez, undulation).
answer_c :- reviews(megregian, sunset).
answer_d :- reviews(megregian, tamerlane).
answer_e :- reviews(oneill, undulation).

% Show the answer choices
#show answer_a.
#show answer_b.
#show answer_c.
#show answer_d.
#show answer_e.

% Show reviews for debugging
#show reviews/2.