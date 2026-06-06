% --- Grid and Black Squares ---
cell(0..5, 0..5).
black_square(0, 0).
black_square(0, 5).
black_square(5, 0).
black_square(5, 5).

% --- Words and Their Letters ---
word("CAT", "C", "A", "T").
word("ACE", "A", "C", "E").
word("TEA", "T", "E", "A").
word("EAR", "E", "A", "R").
word("ATE", "A", "T", "E").
word("RAT", "R", "A", "T").
word("CAR", "C", "A", "R").
word("TAR", "T", "A", "R").

% Directions
direction(horizontal).
direction(vertical).

% --- Placement Choice Rule ---
1 { placement(Word, Row, Col, Dir) :
    word(Word, _, _, _),
    direction(Dir),
    Dir = horizontal,
    Row = 0..5,
    Col = 0..3,
    not black_square(Row, Col),
    not black_square(Row, Col+1),
    not black_square(Row, Col+2)
 } 1 :- word(Word, _, _, _).

1 { placement(Word, Row, Col, Dir) :
    word(Word, _, _, _),
    direction(Dir),
    Dir = vertical,
    Row = 0..3,
    Col = 0..5,
    not black_square(Row, Col),
    not black_square(Row+1, Col),
    not black_square(Row+2, Col)
 } 1 :- word(Word, _, _, _).

% --- Grid Bounds and Black Squares ---
:- placement(Word, Row, Col, horizontal),
   (Col + 2) > 5.
:- placement(Word, Row, Col, vertical),
   (Row + 2) > 5.
:- placement(Word, Row, Col, horizontal),
   black_square(Row, Col).
:- placement(Word, Row, Col, horizontal),
   black_square(Row, Col+1).
:- placement(Word, Row, Col, horizontal),
   black_square(Row, Col+2).
:- placement(Word, Row, Col, vertical),
   black_square(Row, Col).
:- placement(Word, Row, Col, vertical),
   black_square(Row+1, Col).
:- placement(Word, Row, Col, vertical),
   black_square(Row+2, Col).

% --- Letter Placement ---
% Horizontal placement
letter(X, Y, L0) :-
    placement(Word, X, Y, horizontal),
    word(Word, L0, L1, L2).
letter(X, Y+1, L1) :-
    placement(Word, X, Y, horizontal),
    word(Word, L0, L1, L2).
letter(X, Y+2, L2) :-
    placement(Word, X, Y, horizontal),
    word(Word, L0, L1, L2).

% Vertical placement
letter(X, Y, L0) :-
    placement(Word, X, Y, vertical),
    word(Word, L0, L1, L2).
letter(X+1, Y, L1) :-
    placement(Word, X, Y, vertical),
    word(Word, L0, L1, L2).
letter(X+2, Y, L2) :-
    placement(Word, X, Y, vertical),
    word(Word, L0, L1, L2).

% --- No Conflicts ---
:- letter(X, Y, L1), letter(X, Y, L2), L1 != L2.

% --- Intersections ---
intersection(WordH, WordV, X, Y) :-
    placement(WordH, X, Y, horizontal),
    placement(WordV, X, Y, vertical).

% At least 3 intersections
:- #count { X, Y : intersection(_, _, X, Y) } < 3.

% Letter matching at intersections
:- intersection(WordH, WordV, X, Y),
   letter(X, Y, LH),
   letter(X, Y, LV),
   LH != LV.

% --- Connectivity ---
adjacent(X1, Y1, X2, Y2) :-
    (X2 = X1 + 1; X2 = X1 - 1),
    Y2 = Y1,
    cell(X2, Y2).
adjacent(X1, Y1, X2, Y2) :-
    (Y2 = Y1 + 1; Y2 = Y1 - 1),
    X2 = X1,
    cell(X2, Y2).

% Direct connectivity between letters
connected(X1, Y1, X2, Y2) :-
    letter(X1, Y1, _),
    letter(X2, Y2, _),
    adjacent(X1, Y1, X2, Y2).

% Transitive closure for connectivity
reachable(X1, Y1, X2, Y2) :-
    connected(X1, Y1, X2, Y2).
reachable(X1, Y1, X2, Y2) :-
    connected(X1, Y1, X3, Y3),
    reachable(X3, Y3, X2, Y2).

% Ensure all letters are reachable from each other
:- letter(X1, Y1, _),
   letter(X2, Y2, _),
   not reachable(X1, Y1, X2, Y2).

% --- Show the grid and placements ---
#show letter/3.
#show placement/4.