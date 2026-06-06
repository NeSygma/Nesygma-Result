% Domains
row(1..8).
col(1..8).
num(1..8).

% Pre-filled cells
grid(1,1,1).
grid(1,8,8).
grid(2,2,6).
grid(3,3,4).
grid(4,4,5).
grid(5,5,7).
grid(6,6,4).
grid(7,7,6).
grid(8,8,3).
grid(8,1,8).

% Choice: assign numbers to empty cells
{ grid(R,C,N) : num(N) } 1 :- row(R), col(C), not grid(R,C,_).

% Latin Square: each row has each number exactly once
:- row(R), num(N), C1 != C2, grid(R,C1,N), grid(R,C2,N).

% Latin Square: each column has each number exactly once
:- col(C), num(N), R1 != R2, grid(R1,C,N), grid(R2,C,N).

% Adjacent Pair Sum: horizontally adjacent cells sum > 5
:- row(R), col(C), C < 8, grid(R,C,N1), grid(R,C+1,N2), N1 + N2 <= 5.

% Quadrant Parity: top-left (rows 1-4, cols 1-4) has exactly 8 even numbers
even(N) :- num(N), N mod 2 = 0.
odd(N) :- num(N), N mod 2 = 1.

% Count even numbers in top-left quadrant
even_count(E) :- E = #count{R,C : row(R), col(C), R <= 4, C <= 4, grid(R,C,N), even(N)}.
:- even_count(E), E != 8.

% Count odd numbers in bottom-right quadrant
odd_count(O) :- O = #count{R,C : row(R), col(C), R >= 5, C >= 5, grid(R,C,N), odd(N)}.
:- odd_count(O), O != 8.

% Partial Sum: first four cells in row 1 sum to 14
:- grid(1,1,N1), grid(1,2,N2), grid(1,3,N3), grid(1,4,N4), N1+N2+N3+N4 != 14.

% Partial Sum: first four cells in column 1 sum to 10
:- grid(1,1,N1), grid(2,1,N2), grid(3,1,N3), grid(4,1,N4), N1+N2+N3+N4 != 10.

#show grid/3.