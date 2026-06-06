pos(1). pos(2). pos(3). pos(4). pos(5). pos(6).

1 { face_A(I,V) : V = 0..6 } 1 :- pos(I).
1 { face_B(I,V) : V = 0..6 } 1 :- pos(I).
1 { face_C(I,V) : V = 0..6 } 1 :- pos(I).

win_AB(I,J) :- face_A(I,VA), face_B(J,VB), VA > VB.
win_BC(I,J) :- face_B(I,VB), face_C(J,VC), VB > VC.
win_CA(I,J) :- face_C(I,VC), face_A(J,VA), VC > VA.

:- #count{ I,J : win_AB(I,J) } < 19.
:- #count{ I,J : win_BC(I,J) } < 19.
:- #count{ I,J : win_CA(I,J) } < 19.

#show face_A/2, face_B/2, face_C/2.