% Students
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).

% Plays
play(sunset). play(tamerlane). play(undulation).

% Non-empty subsets of plays
subset(1..7).

% Which plays belong to each subset
in_subset(sunset, 1). in_subset(sunset, 4). in_subset(sunset, 5). in_subset(sunset, 7).
in_subset(tamerlane, 2). in_subset(tamerlane, 4). in_subset(tamerlane, 6). in_subset(tamerlane, 7).
in_subset(undulation, 3). in_subset(undulation, 5). in_subset(undulation, 6). in_subset(undulation, 7).

% Size of each subset
size(1, 1). size(2, 1). size(3, 1).
size(4, 2). size(5, 2). size(6, 2).
size(7, 3).

% Assign each student exactly one non-empty subset of plays
1 { assigns(S, Sub) : subset(Sub) } 1 :- student(S).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
:- assigns(kramer, K), assigns(megregian, M), size(K, KS), size(M, MS), KS >= MS.
:- assigns(lopez, L), assigns(megregian, M), size(L, LS), size(M, MS), LS >= MS.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- assigns(jiang, J), assigns(lopez, L), in_subset(P, J), in_subset(P, L).
:- assigns(jiang, J), assigns(megregian, M), in_subset(P, J), in_subset(P, M).

% Condition 3: Kramer and O'Neill both review Tamerlane
:- assigns(kramer, K), not in_subset(tamerlane, K).
:- assigns(oneill, O), not in_subset(tamerlane, O).

% Condition 4: Exactly two of the students review exactly the same play or plays
same_pair(S1, S2) :- assigns(S1, Sub), assigns(S2, Sub), S1 < S2, student(S1), student(S2).
:- 2 { same_pair(S1, S2) }.
:- not 1 { same_pair(S1, S2) }.

% Determine which students review ONLY Sunset (subset 1)
reviews_only_sunset(S) :- assigns(S, 1).

% (A) Lopez only
option(a) :- reviews_only_sunset(lopez),
             assigns(jiang, Jj), Jj != 1,
             assigns(kramer, Jk), Jk != 1,
             assigns(megregian, Jm), Jm != 1,
             assigns(oneill, Jo), Jo != 1.

% (B) O'Neill only
option(b) :- reviews_only_sunset(oneill),
             assigns(jiang, Jj), Jj != 1,
             assigns(kramer, Jk), Jk != 1,
             assigns(lopez, Jl), Jl != 1,
             assigns(megregian, Jm), Jm != 1.

% (C) Jiang and Lopez
option(c) :- reviews_only_sunset(jiang), reviews_only_sunset(lopez),
             assigns(kramer, Jk), Jk != 1,
             assigns(megregian, Jm), Jm != 1,
             assigns(oneill, Jo), Jo != 1.

% (D) Kramer and O'Neill
option(d) :- reviews_only_sunset(kramer), reviews_only_sunset(oneill),
             assigns(jiang, Jj), Jj != 1,
             assigns(lopez, Jl), Jl != 1,
             assigns(megregian, Jm), Jm != 1.

% (E) Lopez and Megregian
option(e) :- reviews_only_sunset(lopez), reviews_only_sunset(megregian),
             assigns(jiang, Jj), Jj != 1,
             assigns(kramer, Jk), Jk != 1,
             assigns(oneill, Jo), Jo != 1.

% Only show models where at least one option is derived
has_option :- option(_).
:- not has_option.

#show option/1.