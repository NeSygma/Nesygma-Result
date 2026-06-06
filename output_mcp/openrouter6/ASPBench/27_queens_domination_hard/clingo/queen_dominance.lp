% 9x9 Chessboard Queen Dominance Problem
% Find minimum number of queens to dominate all squares

% Board definition
square(R, C) :- R = 0..8, C = 0..8.

% Queen placement choice: each square can have at most one queen
{ queen(R, C) } :- square(R, C).

% Count queens for minimization
queen_count(N) :- N = #count { R, C : queen(R, C) }.

% Domination: a square is dominated if there's a queen in same row, column, or diagonal
% Queen dominates its own square
dominated(R, C) :- queen(R, C).

% Same row (different column)
dominated(R, C) :- square(R, C), queen(R, QC), QC != C.

% Same column (different row)  
dominated(R, C) :- square(R, C), queen(QR, C), QR != R.

% Same diagonal (main diagonal: QR - R = QC - C)
dominated(R, C) :- square(R, C), queen(QR, QC), 
                   QR - R == QC - C, (QR != R or QC != C).

% Same diagonal (anti-diagonal: QR - R = -(QC - C))
dominated(R, C) :- square(R, C), queen(QR, QC), 
                   QR - R == -(QC - C), (QR != R or QC != C).

% All squares must be dominated
:- square(R, C), not dominated(R, C).

% Minimize number of queens
#minimize { 1, R, C : queen(R, C) }.

% Show the solution
#show queen/2.
#show queen_count/1.