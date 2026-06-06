% Domain definitions
row(0..5).
col(0..5).
dir(hor).
dir(ver).

% Words
word(cat).
word(ace).
word(tea).
word(ear).
word(ate).
word(rat).
word(car).
word(tar).

% Word letters (using double quotes for constants)
word_letter(cat,1,"C").
word_letter(cat,2,"A").
word_letter(cat,3,"T").
word_letter(ace,1,"A").
word_letter(ace,2,"C").
word_letter(ace,3,"E").
word_letter(tea,1,"T").
word_letter(tea,2,"E").
word_letter(tea,3,"A").
word_letter(ear,1,"E").
word_letter(ear,2,"A").
word_letter(ear,3,"R").
word_letter(ate,1,"A").
word_letter(ate,2,"T").
word_letter(ate,3,"E").
word_letter(rat,1,"R").
word_letter(rat,2,"A").
word_letter(rat,3,"T").
word_letter(car,1,"C").
word_letter(car,2,"A").
word_letter(car,3,"R").
word_letter(tar,1,"T").
word_letter(tar,2,"A").
word_letter(tar,3,"R").

% Black squares
black(0,0).
black(0,5).
black(5,0).
black(5,5).

% Exactly one placement per word
1 { placement(W,R,C,D) : row(R), col(C), dir(D) } 1 :- word(W).

% Bounds: word length 3
:- placement(W,R,C,hor), C > 3.
:- placement(W,R,C,ver), R > 3.

% No start on black square
:- placement(W,R,C,hor), black(R,C).
:- placement(W,R,C,ver), black(R,C).

% Cell positions for horizontal words
cell(W,R0,C0,1) :- placement(W,R0,C0,hor).
cell(W,R0,C1,2) :- placement(W,R0,C0,hor), C1 = C0+1, col(C1).
cell(W,R0,C2,3) :- placement(W,R0,C0,hor), C2 = C0+2, col(C2).

% Cell positions for vertical words
cell(W,R1,C0,1) :- placement(W,R0,C0,ver), R1 = R0+1, row(R1).
cell(W,R2,C0,2) :- placement(W,R0,C0,ver), R2 = R0+2, row(R2).
cell(W,R3,C0,3) :- placement(W,R0,C0,ver), R3 = R0+3, row(R3).

% No cell on black square
:- cell(W,R,C,Pos), black(R,C).

% Letter assignment
letter(R,C,L) :- cell(W,R,C,Pos), word_letter(W,Pos,L).

% Conflict: same cell different letters
:- letter(R,C,L1), letter(R,C,L2), L1 != L2.

% Direction predicates for later use
hor_dir(W) :- placement(W,_,_,hor).
ver_dir(W) :- placement(W,_,_,ver).

% Horizontal and vertical cell markers
horiz_cell(R,C) :- cell(W,R,C,Pos), hor_dir(W).
vert_cell(R,C) :- cell(W,R,C,Pos), ver_dir(W).

% Intersection detection
intersection(R,C) :- horiz_cell(R,C), vert_cell(R,C).

% At least 3 intersections
:- #count{R,C : intersection(R,C)} < 3.

% Adjacency for connectivity
adjacent(R,C,R2,C2) :- row(R), col(C), row(R2), col(C2), R2 = R+1, C2 = C, R < 5.
adjacent(R,C,R2,C2) :- row(R), col(C), row(R2), col(C2), R2 = R-1, C2 = C, R > 0.
adjacent(R,C,R2,C2) :- row(R), col(C), row(R2), col(C2), R2 = R, C2 = C+1, C < 5.
adjacent(R,C,R2,C2) :- row(R), col(C), row(R2), col(C2), R2 = R, C2 = C-1, C > 0.

% Letter cells
letter_cell(R,C) :- letter(R,C,_).

% Choose a root cell for connectivity
1 { root(R,C) : letter_cell(R,C) } 1.

% Reachability
reachable(R,C) :- root(R,C).
reachable(R2,C2) :- reachable(R,C), adjacent(R,C,R2,C2), letter_cell(R2,C2).

% All letter cells must be reachable
:- letter_cell(R,C), not reachable(R,C).

#show placement/4.