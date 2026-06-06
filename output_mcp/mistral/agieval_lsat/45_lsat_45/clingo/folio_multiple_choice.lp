% Domain
student(jiang; kramer; lopez; megregian; o_neill).
play(sunset; tamerlane; undulation).

% Base facts: each student reviews at least one play
1 { reviews(S, P) : play(P) } 1 :- student(S).

% Each student reviews only the three specified plays (implicit from domain)

% Helper: number of plays each student reviews
num_plays_reviewed(S, N) :-
    student(S),
    N = #count{P : reviews(S, P)}.

% Kramer and Lopez each review fewer plays than Megregian
:- student(S), S = kramer, num_plays_reviewed(megregian, NM), num_plays_reviewed(kramer, NK), NM <= NK.
:- student(S), S = lopez, num_plays_reviewed(megregian, NM), num_plays_reviewed(lopez, NL), NM <= NL.

% Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

% Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(o_neill, tamerlane).

% Exactly three students review Undulation
:- #count{S : reviews(S, undulation)} != 3.

% Define a unique identifier for the set of plays each student reviews
% We will use the sorted list of plays as a key for comparison

% Helper to represent the set of plays each student reviews
plays_set(S, P) :- reviews(S, P).

% Define a unique key for each set of plays
% We will use the sorted list of plays as a key
set_key(S, 1) :- student(S), not reviews(S, sunset), not reviews(S, tamerlane), reviews(S, undulation).
set_key(S, 2) :- student(S), not reviews(S, sunset), reviews(S, tamerlane), not reviews(S, undulation).
set_key(S, 3) :- student(S), not reviews(S, sunset), reviews(S, tamerlane), reviews(S, undulation).
set_key(S, 4) :- student(S), reviews(S, sunset), not reviews(S, tamerlane), not reviews(S, undulation).
set_key(S, 5) :- student(S), reviews(S, sunset), not reviews(S, tamerlane), reviews(S, undulation).
set_key(S, 6) :- student(S), reviews(S, sunset), reviews(S, tamerlane), not reviews(S, undulation).
set_key(S, 7) :- student(S), reviews(S, sunset), reviews(S, tamerlane), reviews(S, undulation).

% Ensure each student has exactly one set_key
:- student(S), #count{K : set_key(S, K)} != 1.

% Count how many students share each set_key
count_set_key(K, C) :- C = #count{S : set_key(S, K)}.

% Exactly one set_key is shared by exactly two students, and all others are unique
:- count_set_key(K, 2), #count{K2 : count_set_key(K2, 2)} != 1.
:- count_set_key(K, C), C != 2, C != 1.

% --- Multiple Choice Options ---
% We need to determine which option COULD be true
% Since the problem states there is a single correct answer, we derive exactly one option/1

% Option A: Megregian does not review Undulation
% This is possible if reviews(megregian, undulation) is false
option(a) :- not reviews(megregian, undulation).

% Option B: O'Neill does not review Undulation
% This is possible if reviews(o_neill, undulation) is false
option(b) :- not reviews(o_neill, undulation).

% Option C: Jiang reviews Undulation
% This is possible if reviews(jiang, undulation) is true
option(c) :- reviews(jiang, undulation).

% Option D: Lopez reviews Tamerlane
% This is possible if reviews(lopez, tamerlane) is true
option(d) :- reviews(lopez, tamerlane).

% Option E: O'Neill reviews Sunset
% This is possible if reviews(o_neill, sunset) is true
option(e) :- reviews(o_neill, sunset).

#show option/1.