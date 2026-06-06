% Domains
pos(1..24).
row(R) :- pos(R).
col(C) :- pos(C).

% Row run facts: run(Row,Idx,Color,Len)
run(1,1,1,10). run(1,2,2,4). run(1,3,1,10).
run(2,1,1,10). run(2,2,2,4). run(2,3,1,10).
% rows 3-8
run(3,1,1,2). run(3,2,2,4). run(3,3,1,2).
run(4,1,1,2). run(4,2,2,4). run(4,3,1,2).
run(5,1,1,2). run(5,2,2,4). run(5,3,1,2).
run(6,1,1,2). run(6,2,2,4). run(6,3,1,2).
run(7,1,1,2). run(7,2,2,4). run(7,3,1,2).
run(8,1,1,2). run(8,2,2,4). run(8,3,1,2).
% rows 9-10
run(9,1,1,2). run(9,2,3,8). run(9,3,1,2).
run(10,1,1,2). run(10,2,3,8). run(10,3,1,2).
% rows 11-14 (five runs)
run(11,1,1,2). run(11,2,2,6). run(11,3,3,8). run(11,4,2,6). run(11,5,1,2).
run(12,1,1,2). run(12,2,2,6). run(12,3,3,8). run(12,4,2,6). run(12,5,1,2).
run(13,1,1,2). run(13,2,2,6). run(13,3,3,8). run(13,4,2,6). run(13,5,1,2).
run(14,1,1,2). run(14,2,2,6). run(14,3,3,8). run(14,4,2,6). run(14,5,1,2).
% rows 15-16 (three runs like 9-10)
run(15,1,1,2). run(15,2,3,8). run(15,3,1,2).
run(16,1,1,2). run(16,2,3,8). run(16,3,1,2).
% rows 17-22 (three runs like 3-8)
run(17,1,1,2). run(17,2,2,4). run(17,3,1,2).
run(18,1,1,2). run(18,2,2,4). run(18,3,1,2).
run(19,1,1,2). run(19,2,2,4). run(19,3,1,2).
run(20,1,1,2). run(20,2,2,4). run(20,3,1,2).
run(21,1,1,2). run(21,2,2,4). run(21,3,1,2).
run(22,1,1,2). run(22,2,2,4). run(22,3,1,2).
% rows 23-24 same as 1-2
run(23,1,1,10). run(23,2,2,4). run(23,3,1,10).
run(24,1,1,10). run(24,2,2,4). run(24,3,1,10).

% Column run facts: colrun(Col,Idx,Color,Len)
colrun(1,1,1,24).
colrun(2,1,1,24).
% columns 3-8 (three runs 1,2,1)
colrun(3,1,1,2). colrun(3,2,2,4). colrun(3,3,1,2).
colrun(4,1,1,2). colrun(4,2,2,4). colrun(4,3,1,2).
colrun(5,1,1,2). colrun(5,2,2,4). colrun(5,3,1,2).
colrun(6,1,1,2). colrun(6,2,2,4). colrun(6,3,1,2).
colrun(7,1,1,2). colrun(7,2,2,4). colrun(7,3,1,2).
colrun(8,1,1,2). colrun(8,2,2,4). colrun(8,3,1,2).
% columns 9-10 (1,3,1)
colrun(9,1,1,2). colrun(9,2,3,8). colrun(9,3,1,2).
colrun(10,1,1,2). colrun(10,2,3,8). colrun(10,3,1,2).
% columns 11-14 (2,3,2)
colrun(11,1,2,8). colrun(11,2,3,8). colrun(11,3,2,8).
colrun(12,1,2,8). colrun(12,2,3,8). colrun(12,3,2,8).
colrun(13,1,2,8). colrun(13,2,3,8). colrun(13,3,2,8).
colrun(14,1,2,8). colrun(14,2,3,8). colrun(14,3,2,8).
% columns 15-16 (1,3,1)
colrun(15,1,1,2). colrun(15,2,3,8). colrun(15,3,1,2).
colrun(16,1,1,2). colrun(16,2,3,8). colrun(16,3,1,2).
% columns 17-22 (1,2,1)
colrun(17,1,1,2). colrun(17,2,2,4). colrun(17,3,1,2).
colrun(18,1,1,2). colrun(18,2,2,4). colrun(18,3,1,2).
colrun(19,1,1,2). colrun(19,2,2,4). colrun(19,3,1,2).
colrun(20,1,1,2). colrun(20,2,2,4). colrun(20,3,1,2).
colrun(21,1,1,2). colrun(21,2,2,4). colrun(21,3,1,2).
colrun(22,1,1,2). colrun(22,2,2,4). colrun(22,3,1,2).
% columns 23-24 (full 24 of color 1)
colrun(23,1,1,24).
colrun(24,1,1,24).

% Diagonal constraints
% Main diagonal
diag_main(1,1). diag_main(2,1). diag_main(3,0). diag_main(4,0). diag_main(5,0). diag_main(6,0). diag_main(7,0). diag_main(8,0).
diag_main(9,3). diag_main(10,3). diag_main(11,3). diag_main(12,3). diag_main(13,3). diag_main(14,3). diag_main(15,3). diag_main(16,3).
diag_main(17,0). diag_main(18,0). diag_main(19,0). diag_main(20,0). diag_main(21,0). diag_main(22,0). diag_main(23,1). diag_main(24,1).
% Anti-diagonal (same sequence)
anti(1,1). anti(2,1). anti(3,0). anti(4,0). anti(5,0). anti(6,0). anti(7,0). anti(8,0).
anti(9,3). anti(10,3). anti(11,3). anti(12,3). anti(13,3). anti(14,3). anti(15,3). anti(16,3).
anti(17,0). anti(18,0). anti(19,0). anti(20,0). anti(21,0). anti(22,0). anti(23,1). anti(24,1).

% Choice of start positions for row runs
1 { start(R,J,P) : pos(P) } 1 :- run(R,J,_,_).
% Ordering and fit constraints for rows
:- start(R,J,P), start(R,J1,P1), run(R,J,_,L), J1 = J+1, P1 < P + L + 1.
:- start(R,J,P), run(R,J,_,L), P + L - 1 > 24.

% Derive colored cells from row runs
grid(R,C,Color) :- start(R,J,P), run(R,J,Color,L), pos(C), C >= P, C <= P + L - 1.
% Define colored predicate
colored(R,C) :- grid(R,C,Color), Color != 0.
% White cells where not colored
grid(R,C,0) :- row(R), pos(C), not colored(R,C).
% Ensure each cell has exactly one color
:- grid(R,C,Color1), grid(R,C,Color2), Color1 != Color2.

% Choice of start positions for column runs
1 { startc(C,J,P) : pos(P) } 1 :- colrun(C,J,_,_).
% Ordering and fit constraints for columns
:- startc(C,J,P), startc(C,J1,P1), colrun(C,J,_,L), J1 = J+1, P1 < P + L + 1.
:- startc(C,J,P), colrun(C,J,_,L), P + L - 1 > 24.
% Cells required by column runs
needc(C,J,R,Color) :- startc(C,J,P), colrun(C,J,Color,L), pos(R), R >= P, R <= P + L - 1.
% Enforce column run colors
:- needc(C,J,R,Color), not grid(R,C,Color).
% Ensure every colored cell belongs to a column run
covered_by_col(R,C,Color) :- startc(C,J,P), colrun(C,J,Color,L), pos(R), R >= P, R <= P + L - 1.
:- grid(R,C,Color), Color != 0, not covered_by_col(R,C,Color).

% Diagonal constraints
:- grid(I,I,Col1), diag_main(I,Col2), Col1 != Col2.
% Anti-diagonal constraints (col = 25 - I)
:- grid(I,Col,Col1), anti(I,Col2), Col = 25 - I, Col1 != Col2.

#show grid/3.