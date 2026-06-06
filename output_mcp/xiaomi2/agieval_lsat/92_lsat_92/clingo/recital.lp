% Domains
solo(1..5).
pianist(wayne). pianist(zara).
ptype(modern). ptype(traditional).

% Assign exactly one pianist and one piece type per solo
1 { play(P, S) : pianist(P) } 1 :- solo(S).
1 { piece(T, S) : ptype(T) } 1 :- solo(S).

% Condition 1: Third solo is traditional
piece(traditional, 3).

% Given: Fifth solo is Wayne performing traditional
play(wayne, 5).
piece(traditional, 5).

% Condition 2: Exactly two traditional pieces are performed consecutively
adj(I, J) :- solo(I), solo(J), J = I+1.
trad_pair(I, J) :- adj(I, J), piece(traditional, I), piece(traditional, J).
n_trad_pairs(N) :- N = #count { I,J : trad_pair(I,J) }.
:- n_trad_pairs(N), N != 1.

% Condition 3: Solo 4: Wayne performs traditional OR Zara performs modern
cond3 :- play(wayne, 4), piece(traditional, 4).
cond3 :- play(zara, 4), piece(modern, 4).
:- not cond3.

% Condition 4: Pianist of solo 2 does not perform solo 5
:- play(P, 2), play(P, 5).

% Condition 5: No traditional piece until Wayne performs at least one modern piece
wayne_modern_before(S) :- play(wayne, T), piece(modern, T), T < S, solo(S).
:- piece(traditional, S), not wayne_modern_before(S).

% Check each option
opt_a :- play(zara, 1).
opt_b :- play(wayne, 2).
opt_c :- play(zara, 3).
opt_d :- piece(modern, 2).
opt_e :- piece(traditional, 4).

option(a) :- opt_a.
option(b) :- opt_b.
option(c) :- opt_c.
option(d) :- opt_d.
option(e) :- opt_e.

#show option/1.