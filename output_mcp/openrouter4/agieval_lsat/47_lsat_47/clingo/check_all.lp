% Define domain
student(jiang; kramer; lopez; megregian; oneill).
play(sunset; tamerlane; undulation).

% Choice: each student may review each play
{ reviews(S,P) } :- student(S), play(P).

% Each student reviews at least one play
:- student(S), #count{ P : reviews(S,P) } < 1.

% Constraint: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Constraint: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Constraint: Kramer and Lopez each review fewer plays than Megregian
count_reviews(S, N) :- student(S), N = #count{ P : reviews(S,P) }.
:- count_reviews(kramer, K), count_reviews(megregian, M), K >= M.
:- count_reviews(lopez, L), count_reviews(megregian, M), L >= M.

% Constraint: Exactly two students (one pair) have exactly the same review set
different(S1, S2) :- student(S1), student(S2), S1 != S2, play(P), reviews(S1,P), not reviews(S2,P).
different(S1, S2) :- student(S1), student(S2), S1 != S2, play(P), not reviews(S1,P), reviews(S2,P).

same_reviews(S1, S2) :- student(S1), student(S2), S1 < S2, not different(S1, S2), not different(S2, S1).

pair_count(N) :- N = #count{ S1,S2 : same_reviews(S1,S2) }.
:- pair_count(N), N != 1.

% Given condition: Jiang does NOT review Tamerlane
:- reviews(jiang, tamerlane).

% --- Test each option's negation ---

% Test A: Jiang does NOT review Sunset
% If satisfiable, then A is not necessarily true
% :- not reviews(jiang, sunset).  % uncomment to test

% Test B: Lopez does NOT review Undulation
% :- not reviews(lopez, undulation).  % uncomment to test

% Test C: Megregian does NOT review Sunset
% :- not reviews(megregian, sunset).  % uncomment to test

% Test D: Megregian does NOT review Tamerlane
% :- not reviews(megregian, tamerlane).  % uncomment to test

% Test E: O'Neill does NOT review Undulation
% :- not reviews(oneill, undulation).  % uncomment to test

% Show all reviews
#show reviews/2.