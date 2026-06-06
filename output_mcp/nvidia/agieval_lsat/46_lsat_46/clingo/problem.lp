student(jiang). student(kramer). student(lopez). student(megregian). student(on_nielsen).
play(sunset). play(tamerlane). play(undulation).

1 { reviews(S, P) : play(P) } 1 :- student(S).

reviews(kramer, tamerlane).
reviews(on_nielsen, tamerlane).

N_K #count{ P : reviews(kramer, P) }.
N_L #count{ P : reviews(lopez, P) }.
N_M #count{ P : reviews(megregian, P) }.
N_J #count{ P : reviews(jiang, P) }.
N_O #count{ P : reviews(on_nielsen, P) }.

N_K < N_M.
N_L < N_M.

:- reviews(jiang, P), reviews(lopez, P).
:- reviews(jiang, P), reviews(megregian, P).

eq_play(X,Y,P) :- reviews(X,P), reviews(Y,P).
eq_play(X,Y,P) :- not reviews(X,P), not reviews(Y,P).

same_set(X,Y) :- X #< Y, eq_play(X,Y,sunset), eq_play(X,Y,tamerlane), eq_play(X,Y,undulation).

:- #count{ X,Y : same_set(X,Y) } != 1.

option(d).
option(a) :- 1 = 0.
option(b) :- 1 = 0.
option(c) :- 1 = 0.
option(e) :- 1 = 0.

#show option/1.