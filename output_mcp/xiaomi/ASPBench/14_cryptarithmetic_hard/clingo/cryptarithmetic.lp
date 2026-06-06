% Cryptarithmetic: DONALD + GERALD = ROBERT

% Letters involved
letter(d). letter(o). letter(n). letter(a). letter(l).
letter(g). letter(e). letter(r). letter(b). letter(t).

% Digits 0-9
digit(0). digit(1). digit(2). digit(3). digit(4).
digit(5). digit(6). digit(7). digit(8). digit(9).

% Assign each letter a digit (choice rule)
1 { assign(L, D) : digit(D) } 1 :- letter(L).

% All letters must have different digits (all-different constraint)
:- assign(L1, D), assign(L2, D), L1 != L2.

% Leading zeros constraint: D, G, R cannot be 0
:- assign(d, 0).
:- assign(g, 0).
:- assign(r, 0).

% Columnar addition with carries
% Columns from right to left (position 1 = units, position 6 = hundred-thousands)
% DONALD: D(6) O(5) N(4) A(3) L(2) D(1)
% GERALD: G(6) E(5) R(4) A(3) L(2) D(1)
% ROBERT: R(6) O(5) B(4) E(3) R(2) T(1)

% Carry variables for each column (carry into column i)
carry(0..2).  % Carries can be 0, 1, or 2

% Define carry for each column position
{ c1(0..2) } 1.  % Carry from column 1 to column 2
{ c2(0..2) } 1.  % Carry from column 2 to column 3
{ c3(0..2) } 1.  % Carry from column 3 to column 4
{ c4(0..2) } 1.  % Carry from column 4 to column 5
{ c5(0..2) } 1.  % Carry from column 5 to column 6

% Column 1 (units): D + D = T + 10*c1
:- assign(d, D1), assign(t, T1), 
   D1 + D1 != T1 + 10 * c1(C1), c1(C1).

% Column 2 (tens): L + L + C1 = R + 10*c2
:- assign(l, L2), assign(r, R2), c1(C1), c2(C2),
   L2 + L2 + C1 != R2 + 10 * C2.

% Column 3 (hundreds): A + A + C2 = E + 10*c3
:- assign(a, A3), assign(e, E3), c2(C2), c3(C3),
   A3 + A3 + C2 != E3 + 10 * C3.

% Column 4 (thousands): N + R + C3 = B + 10*c4
:- assign(n, N4), assign(r, R4), assign(b, B4), c3(C3), c4(C4),
   N4 + R4 + C3 != B4 + 10 * C4.

% Column 5 (ten-thousands): O + E + C4 = O + 10*c5
:- assign(o, O5), assign(e, E5), c4(C4), c5(C5),
   O5 + E5 + C4 != O5 + 10 * C5.

% Column 6 (hundred-thousands): D + G + C5 = R
:- assign(d, D6), assign(g, G6), assign(r, R6), c5(C5),
   D6 + G6 + C5 != R6.

% Show the assignment
#show assign/2.