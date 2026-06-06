% Crossword Puzzle Generator - Technology Theme
% 5x5 grid with 6 technology-related words

% Grid domain
row(0..4).
col(0..4).
position(R,C) :- row(R), col(C).

% Word definitions with letters
word("CODE").
word("DATA").
word("TECH").
word("CHIP").
word("BYTE").
word("NET").

% Letter positions for each word (1-indexed for easier handling)
letter("CODE", 1, "C").
letter("CODE", 2, "O").
letter("CODE", 3, "D").
letter("CODE", 4, "E").

letter("DATA", 1, "D").
letter("DATA", 2, "A").
letter("DATA", 3, "T").
letter("DATA", 4, "A").

letter("TECH", 1, "T").
letter("TECH", 2, "E").
letter("TECH", 3, "C").
letter("TECH", 4, "H").

letter("CHIP", 1, "C").
letter("CHIP", 2, "H").
letter("CHIP", 3, "I").
letter("CHIP", 4, "P").

letter("BYTE", 1, "B").
letter("BYTE", 2, "Y").
letter("BYTE", 3, "T").
letter("BYTE", 4, "E").

letter("NET", 1, "N").
letter("NET", 2, "E").
letter("NET", 3, "T").

% Word lengths
length("CODE", 4).
length("DATA", 4).
length("TECH", 4).
length("CHIP", 4).
length("BYTE", 4).
length("NET", 3).

% Placement variables
% placed(word, start_row, start_col, direction)
% direction: 0 = horizontal, 1 = vertical
{ placed(W, R, C, D) } :- word(W), position(R,C), D in {0,1}.

% Constraint: Each word must be placed exactly once
1 { placed(W, R, C, D) : row(R), col(C), D in {0,1} } 1 :- word(W).

% Constraint: Words must fit within bounds
% Horizontal placement: C + length - 1 <= 4
:- placed(W, R, C, 0), length(W, L), C + L - 1 > 4.
% Vertical placement: R + length - 1 <= 4
:- placed(W, R, C, 1), length(W, L), R + L - 1 > 4.

% Helper: Calculate grid position for each letter in a word
% For horizontal placement
grid_pos_h(W, R, C, Pos, R, C1) :-
    placed(W, R, C, 0),
    length(W, Len),
    Pos >= 1, Pos <= Len,
    C1 = C + Pos - 1.

% For vertical placement
grid_pos_v(W, R, C, Pos, R1, C) :-
    placed(W, R, C, 1),
    length(W, Len),
    Pos >= 1, Pos <= Len,
    R1 = R + Pos - 1.

% Define letters at positions for each placement
letter_at(W, R, C, L, Pos) :-
    grid_pos_h(W, R, C, Pos, R, C1),
    letter(W, Pos, L),
    row(R), col(C1).

letter_at(W, R, C, L, Pos) :-
    grid_pos_v(W, R, C, Pos, R1, C),
    letter(W, Pos, L),
    row(R1), col(C).

% Grid cell content (first letter that occupies it)
grid_letter(R, C, L) :-
    position(R, C),
    letter_at(W, R, C, L, Pos).

% Conflict constraint: No two different letters at same position
:- grid_letter(R, C, L1), grid_letter(R, C, L2), L1 != L2.

% Intersection constraint: Words must intersect at matching letters
% For each pair of words, if they share a position, letters must match
intersection(W1, W2, R, C, L) :-
    placed(W1, R1, C1, D1),
    placed(W2, R2, C2, D2),
    W1 != W2,
    letter_at(W1, R, C, L, Pos1),
    letter_at(W2, R, C, L, Pos2).

% At least one intersection required (optional, but good for crossword)
% :- #count{W1,W2 : intersection(W1,W2,_,_,_)} < 1.

% Show directives for output
#show placed/4.
#show grid_letter/3.
#show intersection/5.

% Additional constraints to ensure proper crossword structure
% No isolated words (each word must intersect with at least one other)
% :- placed(W,_,_,_), #count{W2 : intersection(W,W2,_,_,_)} = 0.