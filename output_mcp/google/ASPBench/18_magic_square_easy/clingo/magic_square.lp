% --- Domains ---
cell(1..3, 1..3).
value(1..9).

% --- Generation ---
% Each cell must contain exactly one number from 1 to 9
1 { assign(R, C, V) : value(V) } 1 :- cell(R, C).

% Each number 1-9 must appear exactly once
1 { assign(R, C, V) : cell(R, C) } 1 :- value(V).

% --- Constraints ---
% Target sum
magic_sum(15).

% Rows must sum to 15
:- cell(R, _), not row_sum_ok(R).
row_sum_ok(R) :- R=1..3, magic_sum(S), S = #sum { V, C : assign(R, C, V) }.

% Columns must sum to 15
:- cell(_, C), not col_sum_ok(C).
col_sum_ok(C) :- C=1..3, magic_sum(S), S = #sum { V, R : assign(R, C, V) }.

% Diagonals must sum to 15
:- not diag1_sum_ok.
diag1_sum_ok :- magic_sum(S), S = #sum { V, I : assign(I, I, V) }.

:- not diag2_sum_ok.
diag2_sum_ok :- magic_sum(S), S = #sum { V, I : assign(I, 4-I, V) }.

% --- Output ---
#show assign/3.