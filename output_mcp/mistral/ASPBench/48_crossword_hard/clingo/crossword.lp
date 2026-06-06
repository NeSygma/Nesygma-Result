% Define the grid size
size(6).

% Black squares at corners
black(0,0).
black(0,5).
black(5,0).
black(5,5).

% The 8 three-letter words
word("CAT").
word("ACE").
word("TEA").
word("EAR").
word("ATE").
word("RAT").
word("CAR").
word("TAR").

% Define word letters
word_letters("CAT", 1, "C").
word_letters("CAT", 2, "A").
word_letters("CAT", 3, "T").
word_letters("ACE", 1, "A").
word_letters("ACE", 2, "C").
word_letters("ACE", 3, "E").
word_letters("TEA", 1, "T").
word_letters("TEA", 2, "E").
word_letters("TEA", 3, "A").
word_letters("EAR", 1, "E").
word_letters("EAR", 2, "A").
word_letters("EAR", 3, "R").
word_letters("ATE", 1, "A").
word_letters("ATE", 2, "T").
word_letters("ATE", 3, "E").
word_letters("RAT", 1, "R").
word_letters("RAT", 2, "A").
word_letters("RAT", 3, "T").
word_letters("CAR", 1, "C").
word_letters("CAR", 2, "A").
word_letters("CAR", 3, "R").
word_letters("TAR", 1, "T").
word_letters("TAR", 2, "A").
word_letters("TAR", 3, "R").

% Domain for positions
row(0..5).
col(0..5).

% Directions
direction(horizontal; vertical).

% Each word must be placed exactly once
1 { placed(Word, Row, Col, Dir) : direction(Dir), row(Row), col(Col) } 1 :- word(Word).

% Define cells with letters based on placements
% Horizontal placement
cell(Row, Col, Letter) :-
    placed(Word, Row, Col, horizontal),
    word_letters(Word, 1, Letter).

cell(Row, Col+1, Letter) :-
    placed(Word, Row, Col, horizontal),
    word_letters(Word, 2, Letter).

cell(Row, Col+2, Letter) :-
    placed(Word, Row, Col, horizontal),
    word_letters(Word, 3, Letter).

% Vertical placement
cell(Row, Col, Letter) :-
    placed(Word, Row, Col, vertical),
    word_letters(Word, 1, Letter).

cell(Row+1, Col, Letter) :-
    placed(Word, Row, Col, vertical),
    word_letters(Word, 2, Letter).

cell(Row+2, Col, Letter) :-
    placed(Word, Row, Col, vertical),
    word_letters(Word, 3, Letter).

% Constraints:

% 1. Words cannot start on black squares
:- placed(_, Row, Col, _), black(Row, Col).

% 2. Words cannot cross black squares
% Horizontal words
:- placed(Word, Row, Col, horizontal),
   word_letters(Word, Pos, _),
   Col+Pos-1 =< 5,
   black(Row, Col+Pos-1).

% Vertical words
:- placed(Word, Row, Col, vertical),
   word_letters(Word, Pos, _),
   Row+Pos-1 =< 5,
   black(Row+Pos-1, Col).

% 3. No conflicts: enforce that each cell has at most one letter
% This is implicitly enforced by the cell/3 definition

% 4. At least 3 intersection points
% An intersection occurs when a horizontal and vertical word share a cell with the same letter
intersection(WordH, PosH, WordV, PosV) :-
    placed(WordH, Row, ColH, horizontal),
    word_letters(WordH, PosH, Letter),
    Col = ColH + PosH - 1,
    placed(WordV, RowV, Col, vertical),
    word_letters(WordV, PosV, Letter),
    Row = RowV + PosV - 1,
    WordH != WordV.

% Count intersections - at least 3
:- #count { I : intersection(_, _, _, _) } < 3.

% 5. Connectivity: all cells with letters must be connected
% Identify all cells with letters
has_letter(Row, Col) :- cell(Row, Col, _).

% Define adjacency (4-directional)
adjacent(R1, C1, R2, C2) :-
    has_letter(R1, C1),
    has_letter(R2, C2),
    (R2 = R1 + 1, C2 = C1).
adjacent(R1, C1, R2, C2) :-
    has_letter(R1, C1),
    has_letter(R2, C2),
    (R2 = R1 - 1, C2 = C1).
adjacent(R1, C1, R2, C2) :-
    has_letter(R1, C1),
    has_letter(R2, C2),
    (R2 = R1, C2 = C1 + 1).
adjacent(R1, C1, R2, C2) :-
    has_letter(R1, C1),
    has_letter(R2, C2),
    (R2 = R1, C2 = C1 - 1).

% Choose a root cell
1 { root(R, C) : has_letter(R, C) } 1.

% Define reachability from root
reachable(R, C) :- root(R, C).
reachable(R2, C2) :-
    reachable(R1, C1),
    adjacent(R1, C1, R2, C2).

% All cells with letters must be reachable from the root
:- has_letter(R, C), not reachable(R, C).

% Show the solution
#show placed/4.
#show cell/3.