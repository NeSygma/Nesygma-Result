% Students and plays
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Each student reviews one or more plays (from the three allowed)
{ reviews(S, P) : play(P) } 1 :- student(S).

% Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Count plays per student
num_plays(S, N) :- N = #count{ P : reviews(S, P) }.

% Kramer and Lopez each review fewer plays than Megregian
:- num_plays(megregian, N1), num_plays(kramer, N2), N1 =< N2.
:- num_plays(megregian, N1), num_plays(lopez, N2), N1 =< N2.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(lopez, P), reviews(jiang, P).
:- reviews(megregian, P), reviews(jiang, P).

% Define identical review sets - two students have the same set if they review exactly the same plays
same_reviews(S1, S2) :- student(S1), student(S2), S1 < S2,
                        num_plays(S1, N), num_plays(S2, N),
                        P1 = #count{ P : reviews(S1, P), reviews(S2, P) },
                        P1 = N.

% Count pairs with identical review sets
same_pair_count(N) :- N = #count{ S1, S2 : same_reviews(S1, S2) }.

% Exactly one pair (so exactly two students share the same set)
:- same_pair_count(N), N != 1.

% Question context: Jiang does not review Tamerlane
:- reviews(jiang, tamerlane).

% Map answer choices
option(a) :- reviews(jiang, sunset).
option(b) :- reviews(lopez, undulation).
option(c) :- reviews(megregian, sunset).
option(d) :- reviews(megregian, tamerlane).
option(e) :- reviews(oneill, undulation).

#show option/1.