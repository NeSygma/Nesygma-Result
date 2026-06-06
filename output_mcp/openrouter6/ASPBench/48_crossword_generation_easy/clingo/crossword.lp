% Crossword puzzle on 5x5 grid with technology theme
% Words: CODE, DATA, TECH, CHIP, BYTE, NET

% Domains
row(0..4).
col(0..4).
dir(horizontal; vertical).

% Words
word(1). word(2). word(3). word(4). word(5). word(6).
word_name(1, "CODE"). word_name(2, "DATA"). word_name(3, "TECH"). 
word_name(4, "CHIP"). word_name(5, "BYTE"). word_name(6, "NET").
word_length(1, 4). word_length(2, 4). word_length(3, 4). 
word_length(4, 4). word_length(5, 4). word_length(6, 3).

% Letters for each word (0-indexed positions)
letter(1, 0, "C"). letter(1, 1, "O"). letter(1, 2, "D"). letter(1, 3, "E").
letter(2, 0, "D"). letter(2, 1, "A"). letter(2, 2, "T"). letter(2, 3, "A").
letter(3, 0, "T"). letter(3, 1, "E"). letter(3, 2, "C"). letter(3, 3, "H").
letter(4, 0, "C"). letter(4, 1, "H"). letter(4, 2, "I"). letter(4, 3, "P").
letter(5, 0, "B"). letter(5, 1, "Y"). letter(5, 2, "T"). letter(5, 3, "E").
letter(6, 0, "N"). letter(6, 1, "E"). letter(6, 2, "T").

% Choice rule: each word placed exactly once with a starting position and direction
{ placed(W, R, C, D) : row(R), col(C), dir(D) } 1 :- word(W).

% Bounds constraints
:- placed(W, R, C, horizontal), word_length(W, Len), C + Len - 1 > 4.
:- placed(W, R, C, vertical), word_length(W, Len), R + Len - 1 > 4.

% Define which cells each word occupies
occupies(W, R, C+Pos, Pos) :- placed(W, R, C, horizontal), word_length(W, Len), Pos = 0..Len-1.
occupies(W, R+Pos, C, Pos) :- placed(W, R, C, vertical), word_length(W, Len), Pos = 0..Len-1.

% Letter matching constraint: if two words occupy same cell, letters must match
:- occupies(W1, R, C, Pos1), occupies(W2, R, C, Pos2), W1 != W2, 
   letter(W1, Pos1, Char1), letter(W2, Pos2, Char2), Char1 != Char2.

% Each word must intersect with at least one other word
intersects(W) :- occupies(W, R, C, _), occupies(W2, R, C, _), W != W2.
:- word(W), not intersects(W).

% Derive grid cells (if multiple words occupy same cell, they have same letter)
grid_cell(R, C, Char) :- occupies(W, R, C, Pos), letter(W, Pos, Char).

% Intersections: pairs of words that share a cell
intersection(W1, W2, Pos1, Pos2, Char) :- occupies(W1, R, C, Pos1), occupies(W2, R, C, Pos2), 
                                           W1 < W2, letter(W1, Pos1, Char), letter(W2, Pos2, Char).

% Output
#show placed/4.
#show grid_cell/3.
#show intersection/5.
#show word_name/2.