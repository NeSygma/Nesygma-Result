% Magic Square 3x3
% Numbers 1-9, each used once, rows/cols/diagonals sum to 15.

% Domains
cell(1..3, 1..3).
number(1..9).

% Each cell gets exactly one number
1 { value(R, C, N) : number(N) } 1 :- cell(R, C).

% Each number used exactly once
1 { value(R, C, N) : cell(R, C) } 1 :- number(N).

% Row sums
row_sum(R, S) :- S = #sum{ N, C : value(R, C, N) }, cell(R, _).
:- row_sum(R, S), S != 15.

% Column sums
col_sum(C, S) :- S = #sum{ N, R : value(R, C, N) }, cell(_, C).
:- col_sum(C, S), S != 15.

% Diagonal cells
main_diag(1,1). main_diag(2,2). main_diag(3,3).
anti_diag(1,3). anti_diag(2,2). anti_diag(3,1).

% Diagonal sums
diag_sum(main, S) :- S = #sum{ N, R, C : value(R, C, N), main_diag(R, C) }.
diag_sum(anti, S) :- S = #sum{ N, R, C : value(R, C, N), anti_diag(R, C) }.
:- diag_sum(main, S), S != 15.
:- diag_sum(anti, S), S != 15.

% Show the solution
#show value/3.
#show cell/2.
#show number/1.