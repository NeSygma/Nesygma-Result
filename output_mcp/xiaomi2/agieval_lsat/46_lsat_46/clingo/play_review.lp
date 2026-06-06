% Domain: students and plays
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Each student reviews at least one play, at most 3
1 { reviews(S, P) : play(P) } 3 :- student(S).

% Condition: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Count reviews per student
num_reviews(S, N) :- student(S), N = #count{P : reviews(S, P)}.

% Condition: Kramer and Lopez each review fewer plays than Megregian
:- num_reviews(kramer, NK), num_reviews(megregian, NM), NK >= NM.
:- num_reviews(lopez, NL), num_reviews(megregian, NM), NL >= NM.

% Condition: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition: Exactly two students review exactly the same plays
% Define "not same" - S1 and S2 differ if one reviews a play the other doesn't
not_same(S1, S2) :- student(S1), student(S2), S1 < S2, play(P), reviews(S1, P), not reviews(S2, P).
not_same(S1, S2) :- student(S1), student(S2), S1 < S2, play(P), reviews(S2, P), not reviews(S1, P).

same_set(S1, S2) :- student(S1), student(S2), S1 < S2, not not_same(S1, S2).

% Exactly one pair of students has the same set
1 { same_set(S1, S2) : student(S1), student(S2), S1 < S2 } 1.

% Determine which students review Tamerlane
tamerlane_reviewer(S) :- student(S), reviews(S, tamerlane).

% Check each option
% (A) Jiang, Kramer
option(a) :- tamerlane_reviewer(jiang), tamerlane_reviewer(kramer),
             not tamerlane_reviewer(lopez), not tamerlane_reviewer(megregian), not tamerlane_reviewer(oneill).

% (B) Kramer, O'Neill
option(b) :- not tamerlane_reviewer(jiang), tamerlane_reviewer(kramer),
             not tamerlane_reviewer(lopez), not tamerlane_reviewer(megregian), tamerlane_reviewer(oneill).

% (C) Kramer, Lopez, O'Neill
option(c) :- not tamerlane_reviewer(jiang), tamerlane_reviewer(kramer),
             tamerlane_reviewer(lopez), not tamerlane_reviewer(megregian), tamerlane_reviewer(oneill).

% (D) Kramer, Megregian, O'Neill
option(d) :- not tamerlane_reviewer(jiang), tamerlane_reviewer(kramer),
             not tamerlane_reviewer(lopez), tamerlane_reviewer(megregian), tamerlane_reviewer(oneill).

% (E) Lopez, Megregian, O'Neill
option(e) :- not tamerlane_reviewer(jiang), not tamerlane_reviewer(kramer),
             tamerlane_reviewer(lopez), tamerlane_reviewer(megregian), tamerlane_reviewer(oneill).

#show option/1.