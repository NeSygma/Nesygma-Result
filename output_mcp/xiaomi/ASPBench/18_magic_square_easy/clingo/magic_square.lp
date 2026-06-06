% Domain definitions
row(1). row(2). row(3).
col(1). col(2). col(3).
num(1). num(2). num(3). num(4). num(5). num(6). num(7). num(8). num(9).

% Each cell gets exactly one number from 1-9
1 { square(R, C, N) : num(N) } 1 :- row(R), col(C).

% Each number appears exactly once in the grid
1 { square(R, C, N) : row(R), col(C) } 1 :- num(N).

% Row sum constraints: each row sums to 15
:- row(R), 15 != #sum{ N, C : square(R, C, N) }.

% Column sum constraints: each column sums to 15
:- col(C), 15 != #sum{ N, R : square(R, C, N) }.

% Main diagonal sum constraint (top-left to bottom-right): (1,1), (2,2), (3,3)
:- 15 != #sum{ N, R : square(R, R, N) }.

% Anti-diagonal sum constraint (top-right to bottom-left): (1,3), (2,2), (3,1)
:- 15 != #sum{ N, R : square(R, 4-R, N) }.

% Display the solution
#show square/3.