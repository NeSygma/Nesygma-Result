% Students and plays
student(jiang). student(kramer). student(lopez). student(megregian). student(oneill).
play(sunset). play(tamerlane). play(undulation).

% Define total order for unordered pairs (less)
less(jiang,kramer). less(jiang,lopez). less(jiang,megregian). less(jiang,oneill).
less(kramer,lopez). less(kramer,megregian). less(kramer,oneill).
less(lopez,megregian). less(lopez,oneill).
less(megregian,oneill).

% ---------- World (rev) ----------
% Each student reviews at least one and at most three plays
1 { rev(S,P) : play(P) } 3 :- student(S).

% Fixed reviews
rev(kramer, tamerlane).
rev(oneill, tamerlane).

% Assumption: Jiang does not review Tamerlane
:- rev(jiang, tamerlane).

% Count reviews per student (safe)
cnt(S,N) :- student(S), N = #count { P : rev(S,P) }.

% Kramer and Lopez each review fewer plays than Megregian
:- cnt(kramer, K), cnt(megregian, M), K >= M.
:- cnt(lopez, L), cnt(megregian, M2), L >= M2.

% Lopez and Megregian do not review any play Jiang reviews
:- rev(lopez, P), rev(jiang, P).
:- rev(megregian, P), rev(jiang, P).

% Exactly one pair of students have identical review sets
identical(S1,S2) :- less(S1,S2), not diff(S1,S2).

diff(S1,S2) :- student(S1), student(S2), rev(S1,P), not rev(S2,P).

diff(S1,S2) :- student(S1), student(S2), rev(S2,P), not rev(S1,P).

% Ensure exactly one identical pair
:- #count { S1,S2 : identical(S1,S2) } != 1.

% ---------- Options (must hold in all possible worlds) ----------
% Option A: Jiang reviews Sunset
option(a) :- not exists_without_A.
exists_without_A :- not rev(jiang, sunset).

% Option B: Lopez reviews Undulation
option(b) :- not exists_without_B.
exists_without_B :- not rev(lopez, undulation).

% Option C: Megregian reviews Sunset
option(c) :- not exists_without_C.
exists_without_C :- not rev(megregian, sunset).

% Option D: Megregian reviews Tamerlane
option(d) :- not exists_without_D.
exists_without_D :- not rev(megregian, tamerlane).

% Option E: O'Neill reviews Undulation
option(e) :- not exists_without_E.
exists_without_E :- not rev(oneill, undulation).

#show option/1.