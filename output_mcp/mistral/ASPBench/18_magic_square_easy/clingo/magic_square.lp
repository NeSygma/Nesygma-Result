% Define the grid size
row(1..3).
col(1..3).
number(1..9).

% Each cell must contain exactly one number
1 { cell(R, C, N) : number(N) } 1 :- row(R), col(C).

% Each number must appear exactly once
exactly_once(N) :- number(N), 1 { cell(_, _, N) } 1.
:- number(N), not exactly_once(N).

% All rows sum to 15
:- row(R), 15 != #sum { N : cell(R, C, N) }.

% All columns sum to 15
:- col(C), 15 != #sum { N : cell(R, C, N) }.

% Diagonals sum to 15
main_diagonal_sum(S) :- S = #sum { N : cell(1,1,N) ; N : cell(2,2,N) ; N : cell(3,3,N) }.
:- main_diagonal_sum(S), S != 15.

anti_diagonal_sum(S) :- S = #sum { N : cell(1,3,N) ; N : cell(2,2,N) ; N : cell(3,1,N) }.
:- anti_diagonal_sum(S), S != 15.

% Show the solution
#show cell/3.