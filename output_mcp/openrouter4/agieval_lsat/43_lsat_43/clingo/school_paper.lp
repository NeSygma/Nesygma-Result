% Students and Plays
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Each student reviews one or more plays (choice rule with at least 1)
{ reviews(S, P) : play(P) } :- student(S).
% Each student reviews at least 1 play
:- student(S), #count{P : reviews(S, P)} < 1.

% Condition 2: Kramer and Lopez each review fewer plays than Megregian
review_count(S, N) :- student(S), N = #count{P : reviews(S, P)}.
:- review_count(kramer, Nk), review_count(megregian, Nm), Nk >= Nm.
:- review_count(lopez, Nl), review_count(megregian, Nm), Nl >= Nm.

% Condition 3: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition 4: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition 5: Exactly two students review exactly the same play(s) as each other
% Helper: S1's plays are a subset of S2's plays
subset(S1, S2) :- student(S1), student(S2),
    #count{P : reviews(S1, P), not reviews(S2, P)} = 0.

% Same set: mutual subset
same_set(S1, S2) :- student(S1), student(S2), S1 < S2,
    subset(S1, S2), subset(S2, S1).

% Students who have the same set as at least one other student
has_match(S) :- same_set(S, _).
has_match(S) :- same_set(_, S).

% Exactly 2 students have a match
:- #count{S : has_match(S)} != 2.

% --- Now evaluate each option ---
% Only Sunset reviewers
only_sunset(S) :- student(S), reviews(S, sunset), not reviews(S, tamerlane), not reviews(S, undulation).

option_a_possible :- #count{S : only_sunset(S)} = 1, only_sunset(lopez).

option_b_possible :- #count{S : only_sunset(S)} = 1, only_sunset(oneill).

option_c_possible :- #count{S : only_sunset(S)} = 2, only_sunset(jiang), only_sunset(lopez).

option_d_possible :- #count{S : only_sunset(S)} = 2, only_sunset(kramer), only_sunset(oneill).

option_e_possible :- #count{S : only_sunset(S)} = 2, only_sunset(lopez), only_sunset(megregian).

% Determine which option is correct
option(a) :- option_a_possible.
option(b) :- option_b_possible.
option(c) :- option_c_possible.
option(d) :- option_d_possible.
option(e) :- option_e_possible.

#show option/1.