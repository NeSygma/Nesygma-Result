% Students and plays
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Each student reviews one or more plays
1 { reviews(Student, Play) : play(Play) } 3 :- student(Student).

% Condition 1: Kramer and Lopez each review fewer plays than Megregian
count_reviews(Student, N) :- N = #count{Play : reviews(Student, Play)}, student(Student).
:- count_reviews(kramer, K), count_reviews(megregian, M), K >= M.
:- count_reviews(lopez, L), count_reviews(megregian, M), L >= M.

% Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
:- reviews(lopez, Play), reviews(jiang, Play).
:- reviews(megregian, Play), reviews(jiang, Play).

% Condition 3: Kramer and O'Neill both review Tamerlane
reviews(kramer, tamerlane).
reviews(oneill, tamerlane).

% Condition 4: Exactly two students review exactly the same set of plays
% Define signature for each student (0/1 for each play)
sig_sunset(Student, 1) :- reviews(Student, sunset).
sig_sunset(Student, 0) :- student(Student), not reviews(Student, sunset).
sig_tamerlane(Student, 1) :- reviews(Student, tamerlane).
sig_tamerlane(Student, 0) :- student(Student), not reviews(Student, tamerlane).
sig_undulation(Student, 1) :- reviews(Student, undulation).
sig_undulation(Student, 0) :- student(Student), not reviews(Student, undulation).

% Count students with each signature
count_sig(S, T, U, N) :- 
    N = #count{Student : student(Student), sig_sunset(Student, S), sig_tamerlane(Student, T), sig_undulation(Student, U)},
    S = 0..1, T = 0..1, U = 0..1.

% Exactly two students share the same signature
% Count how many signatures have exactly 2 students
count_sig_2 = #count{S,T,U : count_sig(S,T,U,2)}.
:- count_sig_2 != 1.

% And ensure no signature has more than 2
:- count_sig(S,T,U,N), N > 2.

% Helper: Students who review ONLY Sunset (and no other plays)
reviews_only_sunset(Student) :- reviews(Student, sunset), not reviews(Student, tamerlane), not reviews(Student, undulation).

% Map the correct answer to option/1
% Option A: Lopez reviews only Sunset
option(a) :- reviews_only_sunset(lopez), not reviews_only_sunset(jiang), not reviews_only_sunset(kramer), not reviews_only_sunset(megregian), not reviews_only_sunset(oneill).

% Option B: O'Neill reviews only Sunset
option(b) :- reviews_only_sunset(oneill), not reviews_only_sunset(jiang), not reviews_only_sunset(kramer), not reviews_only_sunset(lopez), not reviews_only_sunset(megregian).

% Option C: Jiang and Lopez review only Sunset
option(c) :- reviews_only_sunset(jiang), reviews_only_sunset(lopez), not reviews_only_sunset(kramer), not reviews_only_sunset(megregian), not reviews_only_sunset(oneill).

% Option D: Kramer and O'Neill review only Sunset
option(d) :- reviews_only_sunset(kramer), reviews_only_sunset(oneill), not reviews_only_sunset(jiang), not reviews_only_sunset(lopez), not reviews_only_sunset(megregian).

% Option E: Lopez and Megregian review only Sunset
option(e) :- reviews_only_sunset(lopez), reviews_only_sunset(megregian), not reviews_only_sunset(jiang), not reviews_only_sunset(kramer), not reviews_only_sunset(oneill).

#show option/1.