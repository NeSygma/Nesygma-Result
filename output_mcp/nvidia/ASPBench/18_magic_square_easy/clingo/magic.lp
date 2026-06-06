% domain
num(1). num(2). num(3). num(4). num(5). num(6). num(7). num(8). num(9).

% coordinates
r(1). r(2). r(3). c(1). c(2). c(3).

% each cell gets exactly one number
1 { cell(R,C,N) : num(N) } 1 :- r(R), c(C).

% each number used exactly once
1 { cell(R,C,N) : r(R), c(C) } 1 :- num(N).

% row sums = 15
:- #sum { N : cell(1,C,N) } != 15.
:- #sum { N : cell(2,C,N) } != 15.
:- #sum { N : cell(3,C,N) } != 15.

% column sums = 15
:- #sum { N : cell(R,1,N) } != 15.
:- #sum { N : cell(R,2,N) } != 15.
:- #sum { N : cell(R,3,N) } != 15.

% diagonal sums = 15
diag1(N) :- cell(1,1,N).
diag1(N) :- cell(2,2,N).
diag1(N) :- cell(3,3,N).
:- #sum { N : diag1(N) } != 15.

diag2(N) :- cell(1,3,N).
diag2(N) :- cell(2,2,N).
diag2(N) :- cell(3,1,N).
:- #sum { N : diag2(N) } != 15.

% show solution
#show cell/3.