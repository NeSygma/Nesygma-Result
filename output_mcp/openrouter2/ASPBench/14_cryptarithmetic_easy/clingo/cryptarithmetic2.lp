digit(0). digit(1). digit(2). digit(3). digit(4). digit(5). digit(6). digit(7). digit(8). digit(9).
letter(s). letter(e). letter(n). letter(d). letter(m). letter(o). letter(r). letter(y).

1 { assignment(L,D) : digit(D) } 1 :- letter(L).

:- assignment(L1,D), assignment(L2,D), L1 != L2.
:- assignment(s,0).
:- assignment(m,0).

:- assignment(s,S), assignment(e,E), assignment(n,N), assignment(d,D),
   assignment(m,M), assignment(o,O), assignment(r,R), assignment(y,Y),
   1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E !=
   10000*M + 1000*O + 100*N + 10*E + Y.

equation(Num1,Num2,Num3) :-
   assignment(s,S), assignment(e,E), assignment(n,N), assignment(d,D),
   assignment(m,M), assignment(o,O), assignment(r,R), assignment(y,Y),
   Num1 = 1000*S + 100*E + 10*N + D,
   Num2 = 1000*M + 100*O + 10*R + E,
   Num3 = 10000*M + 1000*O + 100*N + 10*E + Y.

valid :- assignment(s,_).

#show assignment/2.
#show equation/3.
#show valid.