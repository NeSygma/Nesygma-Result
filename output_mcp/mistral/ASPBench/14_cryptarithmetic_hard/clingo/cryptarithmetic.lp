% Define the letters involved in the puzzle
letter(d;o;n;a;l;g;e;r;b;t).

% Digits 0-9
 digit(0..9).

% Each letter must be assigned a unique digit from 0-9
1 { assignment(L, D) : digit(D) } 1 :- letter(L).
:- assignment(L1, D), assignment(L2, D), L1 != L2.

% Leading zeros constraint: D, G, R cannot be 0
:- assignment(d, 0).
:- assignment(g, 0).
:- assignment(r, 0).

% R must be 1 (since DONALD + GERALD <= 1999998, so ROBERT starts with 1)
:- assignment(r, R), R != 1.

% Define carry variables (0 or 1)
carry(0..1).

% Column 0 (units place): D + D = T + 10*C1
:- assignment(d, D), assignment(t, T), carry(C1), 2*D - T - 10*C1 != 0.

% Column 1 (tens place): L + L + C1 = R + 10*C2
:- assignment(l, L), assignment(r, R), carry(C1;C2), 2*L + C1 - R - 10*C2 != 0.

% Column 2 (hundreds place): A + A + C2 = E + 10*C3
:- assignment(a, A), assignment(e, E), carry(C2;C3), 2*A + C2 - E - 10*C3 != 0.

% Column 3 (thousands place): N + R + C3 = B + 10*C4
:- assignment(n, N), assignment(r, R), assignment(b, B), carry(C3;C4), N + R + C3 - B - 10*C4 != 0.

% Column 4 (ten-thousands place): O + E + C4 = R + 10*C5
:- assignment(o, O), assignment(e, E), assignment(r, R), carry(C4;C5), O + E + C4 - R - 10*C5 != 0.

% Column 5 (hundred-thousands place): D + G + C5 = O + 10*C6
:- assignment(d, D), assignment(g, G), assignment(o, O), carry(C5;C6), D + G + C5 - O - 10*C6 != 0.

% Column 6 (millions place): C6 = R (final carry must equal R)
% Since R=1, C6 must be 1
:- carry(C6), C6 != 1.

% Show the assignment of digits to letters
#show assignment/2.