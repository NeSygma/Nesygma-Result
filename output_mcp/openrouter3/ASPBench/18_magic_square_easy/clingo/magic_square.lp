% Magic Square 3x3 Problem
% Numbers 1-9 must be placed so all rows, columns, and diagonals sum to 15

% Domain declarations
row(1..3).
col(1..3).
number(1..9).
magic_sum(15).

% Each cell gets exactly one number from 1-9
1 { value(R, C, N) : number(N) } 1 :- cell(R, C).
cell(R, C) :- row(R), col(C).

% Each number appears exactly once
1 { value(R, C, N) : cell(R, C) } 1 :- number(N).

% Row sums must equal 15
row_sum(R, 15) :- row(R), 
    15 = #sum { N, R, C : value(R, C, N) }.

% Column sums must equal 15  
col_sum(C, 15) :- col(C),
    15 = #sum { N, R, C : value(R, C, N) }.

% Diagonal sums must equal 15
% Main diagonal: (1,1), (2,2), (3,3)
diag_sum(1, 15) :- 
    15 = #sum { N, R : value(R, R, N) }.

% Anti-diagonal: (1,3), (2,2), (3,1)
diag_sum(2, 15) :-
    15 = #sum { N, R : value(R, 4-R, N) }.

% Show the solution
#show value/3.
#show magic_sum/1.