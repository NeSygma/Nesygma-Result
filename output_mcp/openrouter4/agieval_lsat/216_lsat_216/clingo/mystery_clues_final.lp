% chapters
chapter(1..7).

% clues
clue(r; s; t; u; w; x; z).

% each clue exactly one chapter
1 { pos(C, Ch) : chapter(Ch) } 1 :- clue(C).

% each chapter exactly one clue
1 { pos(C, Ch) : clue(C) } 1 :- chapter(Ch).

% constraint 1: T not in ch1
:- pos(t, 1).

% constraint 2: T before W, exactly two chapters between
:- pos(t, Tch), pos(w, Wch), Tch >= Wch.
:- pos(t, Tch), pos(w, Wch), Wch - Tch != 3.

% constraint 3: S and Z not adjacent
:- pos(s, Sch), pos(z, Zch), Sch = Zch + 1.
:- pos(s, Sch), pos(z, Zch), Zch = Sch + 1.

% constraint 4: W and X not adjacent
:- pos(w, Wch), pos(x, Xch), Wch = Xch + 1.
:- pos(w, Wch), pos(x, Xch), Xch = Wch + 1.

% constraint 5: U and X adjacent
:- pos(u, Uch), pos(x, Xch), Uch != Xch + 1, Xch != Uch + 1.

% Given: Z in chapter 7
pos(z, 7).

% Evaluate the possibility of option D: U in chapter 1
% If the program is satisfiable with U=1, then D is the answer.
:- not pos(u, 1).

option(d).

#show option/1.