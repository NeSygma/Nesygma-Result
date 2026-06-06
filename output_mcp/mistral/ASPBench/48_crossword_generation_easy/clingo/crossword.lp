% Define the grid size
row(0..4).
col(0..4).

% Define the words and their lengths
word(code; data; tech; chip; byte; net).
word_length(code, 4).
word_length(data, 4).
word_length(tech, 4).
word_length(chip, 4).
word_length(byte, 4).
word_length(net, 3).

% Directions
direction(horizontal; vertical).

% Place each word exactly once
1 { placed(Word, Dir, Row, Col) : direction(Dir), row(Row), col(Col) } 1 :- word(Word).

% Ensure each word is placed exactly once (cardinality constraint)
:- word(Word), not 1 { placed(Word, Dir, Row, Col) : direction(Dir), row(Row), col(Col) } 1.

% Define the letters for each word as facts
word_letter(code, 0, "C").
word_letter(code, 1, "O").
word_letter(code, 2, "D").
word_letter(code, 3, "E").

word_letter(data, 0, "D").
word_letter(data, 1, "A").
word_letter(data, 2, "T").
word_letter(data, 3, "A").

word_letter(tech, 0, "T").
word_letter(tech, 1, "E").
word_letter(tech, 2, "C").
word_letter(tech, 3, "H").

word_letter(chip, 0, "C").
word_letter(chip, 1, "H").
word_letter(chip, 2, "I").
word_letter(chip, 3, "P").

word_letter(byte, 0, "B").
word_letter(byte, 1, "Y").
word_letter(byte, 2, "T").
word_letter(byte, 3, "E").

word_letter(net, 0, "N").
word_letter(net, 1, "E").
word_letter(net, 2, "T").

% Define grid positions for placed words (horizontal placement)
grid(Row, Col, Letter) :-
    placed(Word, horizontal, Row, Col),
    word_letter(Word, 0, Letter).

grid(Row, Col+1, Letter) :-
    placed(Word, horizontal, Row, Col),
    word_letter(Word, 1, Letter),
    col(Col+1).

grid(Row, Col+2, Letter) :-
    placed(Word, horizontal, Row, Col),
    word_letter(Word, 2, Letter),
    col(Col+2).

grid(Row, Col+3, Letter) :-
    placed(Word, horizontal, Row, Col),
    word_letter(Word, 3, Letter),
    col(Col+3).

% Define grid positions for placed words (vertical placement)
grid(Row, Col, Letter) :-
    placed(Word, vertical, Row, Col),
    word_letter(Word, 0, Letter).

grid(Row+1, Col, Letter) :-
    placed(Word, vertical, Row, Col),
    word_letter(Word, 1, Letter),
    row(Row+1).

grid(Row+2, Col, Letter) :-
    placed(Word, vertical, Row, Col),
    word_letter(Word, 2, Letter),
    row(Row+2).

grid(Row+3, Col, Letter) :-
    placed(Word, vertical, Row, Col),
    word_letter(Word, 3, Letter),
    row(Row+3).

% For the 3-letter word NET (horizontal placement)
grid(Row, Col, Letter) :-
    placed(net, horizontal, Row, Col),
    word_letter(net, 0, Letter).

grid(Row, Col+1, Letter) :-
    placed(net, horizontal, Row, Col),
    word_letter(net, 1, Letter),
    col(Col+1).

grid(Row, Col+2, Letter) :-
    placed(net, horizontal, Row, Col),
    word_letter(net, 2, Letter),
    col(Col+2).

% For the 3-letter word NET (vertical placement)
grid(Row, Col, Letter) :-
    placed(net, vertical, Row, Col),
    word_letter(net, 0, Letter).

grid(Row+1, Col, Letter) :-
    placed(net, vertical, Row, Col),
    word_letter(net, 1, Letter),
    row(Row+1).

grid(Row+2, Col, Letter) :-
    placed(net, vertical, Row, Col),
    word_letter(net, 2, Letter),
    row(Row+2).

% Ensure no two different letters at the same grid position
:- grid(Row, Col, Letter1), grid(Row, Col, Letter2), Letter1 != Letter2.

% Ensure all words fit within the grid bounds
% For horizontal placement
:- placed(Word, horizontal, Row, Col), word_length(Word, Len),
   Len = 4, not col(Col+3).
:- placed(Word, horizontal, Row, Col), word_length(Word, Len),
   Len = 3, not col(Col+2).

% For vertical placement
:- placed(Word, vertical, Row, Col), word_length(Word, Len),
   Len = 4, not row(Row+3).
:- placed(Word, vertical, Row, Col), word_length(Word, Len),
   Len = 3, not row(Row+2).

% Show the grid
#show grid/3.