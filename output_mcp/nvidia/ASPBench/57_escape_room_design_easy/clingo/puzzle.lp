puzzle(1). puzzle(2). puzzle(3). puzzle(4). puzzle(5). puzzle(6).
difficulty(1,1). difficulty(2,1). difficulty(3,2). difficulty(4,2). difficulty(5,3). difficulty(6,3).
needs(2,1). needs(3,2). needs(3,4). needs(4,1). needs(5,3). needs(6,5).

1 { pos(P, Pos) : Pos = 1..6 } :- puzzle(P).
1 { pos(P, N) : puzzle(P), N = 1..6 } :- .

:- pos(P, Ppos), pos(Q, Qpos), Ppos <= Qpos, needs(P, Q).

diff_at(Pos, Diff) :- pos(P, Pos), difficulty(P, Diff).

#show pos/2.
#show diff_at/2.