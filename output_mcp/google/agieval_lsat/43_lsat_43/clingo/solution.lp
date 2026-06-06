% Students and Plays
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Each student reviews 1 or more plays
1 { reviews(S, P) : play(P) } 3 :- student(S).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
count_reviews(S, N) :- student(S), N = #count{P : reviews(S, P)}.
:- count_reviews(kramer, NK), count_reviews(megregian, NM), NK >= NM.
:- count_reviews(lopez, NL), count_reviews(megregian, NM), NL >= NM.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Condition 3: Kramer and O'Neill both review Tamerlane
:- not reviews(kramer, tamerlane).
:- not reviews(oneill, tamerlane).

% Condition 4: Exactly two of the students review exactly the same play or plays as each other
same_set(S1, S2) :- student(S1), student(S2), S1 < S2,
                    #count{P : reviews(S1, P), not reviews(S2, P)} = 0,
                    #count{P : reviews(S2, P), not reviews(S1, P)} = 0.
:- #count{ (S1, S2) : same_set(S1, S2) } != 1.

% Identify students who review ONLY Sunset
only_sunset(S) :- reviews(S, sunset), #count{P : reviews(S, P)} = 1.

% Check which students are in the only_sunset set
% We want to see which of the answer choices is possible.
% (A) Lopez
% (B) O'Neill
% (C) Jiang, Lopez
% (D) Kramer, O'Neill
% (E) Lopez, Megregian

% Define the sets for each option
set_a(S) :- S = lopez.
set_b(S) :- S = oneill.
set_c(S) :- S = jiang; S = lopez.
set_d(S) :- S = kramer; S = oneill.
set_e(S) :- S = lopez; S = megregian.

% Check if the set of students who review only sunset matches the option
matches(Option, Set) :- Option = a, #count{S : only_sunset(S), set_a(S)} = #count{S : set_a(S)}, #count{S : only_sunset(S)} = #count{S : set_a(S)}.
matches(Option, Set) :- Option = b, #count{S : only_sunset(S), set_b(S)} = #count{S : set_b(S)}, #count{S : only_sunset(S)} = #count{S : set_b(S)}.
matches(Option, Set) :- Option = c, #count{S : only_sunset(S), set_c(S)} = #count{S : set_c(S)}, #count{S : only_sunset(S)} = #count{S : set_c(S)}.
matches(Option, Set) :- Option = d, #count{S : only_sunset(S), set_d(S)} = #count{S : set_d(S)}, #count{S : only_sunset(S)} = #count{S : set_d(S)}.
matches(Option, Set) :- Option = e, #count{S : only_sunset(S), set_e(S)} = #count{S : set_e(S)}, #count{S : only_sunset(S)} = #count{S : set_e(S)}.

option(a) :- matches(a, _).
option(b) :- matches(b, _).
option(c) :- matches(c, _).
option(d) :- matches(d, _).
option(e) :- matches(e, _).

#show option/1.