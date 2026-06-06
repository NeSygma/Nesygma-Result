%--- singers and positions ---
singer(kammer). singer(lugo). singer(trillo). singer(waite). singer(yoshida). singer(zinn).
position(1..6).

%--- each singer gets exactly one position, each position gets exactly one singer ---
1 { pos(S,P) : position(P) } 1 :- singer(S).
1 { pos(S,P) : singer(S) } 1 :- position(P).

%--- recorded singers ---
recorded(kammer). recorded(lugo).

%--- base constraints (excluding Waite condition) ---
% fourth audition cannot be recorded
:- pos(S,4), recorded(S).
% fifth audition must be recorded (i.e., position 5 occupied by a recorded singer)
:- not pos(kammer,5), not pos(lugo,5).
% Kammer earlier than Trillo
:- pos(kammer,K), pos(trillo,T), K >= T.
% Zinn earlier than Yoshida
:- pos(zinn,Z), pos(yoshida,Y), Z >= Y.

%--- original Waite condition (for reference) ---
ok_original :- pos(waite,W), pos(kammer,K), pos(lugo,L), W < K, W < L.

%--- alternative A: Zinn is the only singer who can be earlier than Waite ---
alt_a_cond :- pos(zinn,Z), pos(waite,W), Z < W,
    not (singer(S), S != waite, S != zinn, pos(S,P), P < W).
ok_a :- alt_a_cond.

%--- alternative B: Waite immediately before or after Zinn ---
ok_b :- pos(waite,W), pos(zinn,Z), W = Z + 1.
ok_b :- pos(waite,W), pos(zinn,Z), Z = W + 1.

%--- alternative C: Waite earlier than Lugo ---
ok_c :- pos(waite,W), pos(lugo,L), W < L.

%--- alternative D: Waite is first or second ---
ok_d :- pos(waite,1).
ok_d :- pos(waite,2).

%--- alternative E: first audition cannot be recorded ---
ok_e :- not (pos(S,1), recorded(S)).

%--- differences between original and each alternative ---
% A
diff_a :- #count{ 1 : ok_original, not ok_a } > 0.
diff_a :- #count{ 1 : ok_a, not ok_original } > 0.
% B
diff_b :- #count{ 1 : ok_original, not ok_b } > 0.
diff_b :- #count{ 1 : ok_b, not ok_original } > 0.
% C
diff_c :- #count{ 1 : ok_original, not ok_c } > 0.
diff_c :- #count{ 1 : ok_c, not ok_original } > 0.
% D
diff_d :- #count{ 1 : ok_original, not ok_d } > 0.
diff_d :- #count{ 1 : ok_d, not ok_original } > 0.
% E
diff_e :- #count{ 1 : ok_original, not ok_e } > 0.
diff_e :- #count{ 1 : ok_e, not ok_original } > 0.

%--- map the correct answer to option/1 (exactly one should be true) ---
option(a) :- not diff_a.
option(b) :- not diff_b.
option(c) :- not diff_c.
option(d) :- not diff_d.
option(e) :- not diff_e.

#show option/1.