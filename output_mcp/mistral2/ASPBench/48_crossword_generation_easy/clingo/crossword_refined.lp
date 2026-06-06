% Define the grid size
row(0..4).
col(0..4).

% Define the words and their lengths
word("CODE", 4).
word("DATA", 4).
word("TECH", 4).
word("CHIP", 4).
word("BYTE", 4).
word("NET", 3).

% Directions
direction(horizontal).
direction(vertical).

% Define the letters for each word
word_letters("CODE", 0, "C").
word_letters("CODE", 1, "O").
word_letters("CODE", 2, "D").
word_letters("CODE", 3, "E").

word_letters("DATA", 0, "D").
word_letters("DATA", 1, "A").
word_letters("DATA", 2, "T").
word_letters("DATA", 3, "A").

word_letters("TECH", 0, "T").
word_letters("TECH", 1, "E").
word_letters("TECH", 2, "C").
word_letters("TECH", 3, "H").

word_letters("CHIP", 0, "C").
word_letters("CHIP", 1, "H").
word_letters("CHIP", 2, "I").
word_letters("CHIP", 3, "P").

word_letters("BYTE", 0, "B").
word_letters("BYTE", 1, "Y").
word_letters("BYTE", 2, "T").
word_letters("BYTE", 3, "E").

word_letters("NET", 0, "N").
word_letters("NET", 1, "E").
word_letters("NET", 2, "T").

% Choice rule: Place each word in the grid
{ placed(W, R, C, D) : word(W, _), row(R), col(C), direction(D) } = 1 :- word(W, _).

% Ensure each word is placed exactly once
:- word(W, _), not placed(W, _, _, _).

% Ensure the word fits within the grid bounds
:- placed(W, R, C, horizontal), word(W, L), C + L - 1 > 4.
:- placed(W, R, C, vertical), word(W, L), R + L - 1 > 4.

% Define the letters in the grid based on word placements
letter_at(R, C, L) :-
    placed(W, R, C, horizontal),
    word(W, LEN),
    word_letters(W, P, L),
    C + P <= 4,
    C + P >= 0,
    0 <= P, P < LEN.

letter_at(R, C, L) :-
    placed(W, R, C, vertical),
    word(W, LEN),
    word_letters(W, P, L),
    R + P <= 4,
    R + P >= 0,
    0 <= P, P < LEN.

% Ensure no two words conflict at the same cell
:- letter_at(R, C, L1), letter_at(R, C, L2), L1 != L2.

% Show the grid and word placements
#show letter_at/3.
#show placed/4.