% Define the grid size
size(3).

% Define the numbers to place
number(1..9).

% Define the magic sum
magic_sum(15).

% Define the grid positions
cell(X, Y) :- size(N), X = 1..N, Y = 1..N.

% Each cell must contain a number from 1 to 9
1 { value(X, Y, N) : number(N) } 1 :- cell(X, Y).

% Each number must appear exactly once
:- number(N), not exactly_once(N).
exactly_once(N) :- number(N), cell(X, Y), value(X, Y, N), not has_duplicate(N).
has_duplicate(N) :- number(N), cell(X, Y), value(X, Y, N), cell(X1, Y1), value(X1, Y1, N), X != X1, Y != Y1.

% All rows must sum to 15
:- cell(X, _), magic_sum(S), S != #sum { N : cell(_, Y), value(X, Y, N) }.

% All columns must sum to 15
:- cell(_, Y), magic_sum(S), S != #sum { N : cell(X, _), value(X, Y, N) }.

% Both diagonals must sum to 15
:- magic_sum(S), S != #sum { N : cell(X, X), value(X, X, N) }.
:- magic_sum(S), S != #sum { N : cell(X, 4-X), value(X, 4-X, N) }.

% Show the solution
#show value/3.