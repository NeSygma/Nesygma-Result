% Domains
row(1..9).
col(1..9).
val(1..9).
box_id(1..9).

% Box mapping
box(R, C, B) :- row(R), col(C), B = ((R-1)/3)*3 + ((C-1)/3) + 1.

% Clues
clue(1, 1, 5). clue(1, 2, 3). clue(1, 5, 7).
clue(2, 1, 6). clue(2, 4, 1). clue(2, 5, 9). clue(2, 6, 5).
clue(3, 2, 9). clue(3, 3, 8). clue(3, 8, 6).
clue(4, 1, 8). clue(4, 5, 6). clue(4, 9, 3).
clue(5, 1, 4). clue(5, 4, 8). clue(5, 6, 3). clue(5, 9, 1).
clue(6, 1, 7). clue(6, 5, 2). clue(6, 9, 6).
clue(7, 2, 6). clue(7, 7, 2). clue(7, 8, 8).
clue(8, 4, 4). clue(8, 5, 1). clue(8, 6, 9). clue(8, 9, 5).
clue(9, 5, 8). clue(9, 8, 7). clue(9, 9, 9).

% Choice rule: Each cell must have exactly one value
1 { cell(R, C, V) : val(V) } 1 :- row(R), col(C).

% Clues must be satisfied
cell(R, C, V) :- clue(R, C, V).

% Constraints
% 1. Each row must contain all digits 1-9 exactly once
:- row(R), val(V), not 1 { cell(R, C, V) : col(C) } 1.

% 2. Each column must contain all digits 1-9 exactly once
:- col(C), val(V), not 1 { cell(R, C, V) : row(R) } 1.

% 3. Each 3x3 sub-box must contain all digits 1-9 exactly once
:- box_id(B), val(V), not 1 { cell(R, C, V) : box(R, C, B) } 1.

#show cell/3.