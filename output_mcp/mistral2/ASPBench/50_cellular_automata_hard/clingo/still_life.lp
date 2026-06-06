% Grid size: 14x14
row(0..13).
col(0..13).
grid(X, Y) :- row(X), col(Y).

% Pattern definitions
% Block: 2x2 square
pattern_cell(block, 0, 0).
pattern_cell(block, 0, 1).
pattern_cell(block, 1, 0).
pattern_cell(block, 1, 1).

% Boat: 5 cells
pattern_cell(boat, 0, 0).
pattern_cell(boat, 0, 1).
pattern_cell(boat, 1, 0).
pattern_cell(boat, 1, 2).
pattern_cell(boat, 2, 1).

% Loaf: 7 cells
pattern_cell(loaf, 0, 1).
pattern_cell(loaf, 0, 2).
pattern_cell(loaf, 1, 0).
pattern_cell(loaf, 1, 3).
pattern_cell(loaf, 2, 1).
pattern_cell(loaf, 2, 3).
pattern_cell(loaf, 3, 2).

% Place exactly one instance of each pattern
{ pattern(block, X, Y) : grid(X, Y) } 1.
{ pattern(boat, X, Y) : grid(X, Y) } 1.
{ pattern(loaf, X, Y) : grid(X, Y) } 1.

% Derive live cells from placed patterns
live(X, Y) :- pattern(P, X0, Y0), pattern_cell(P, DX, DY),
              X = X0 + DX, Y = Y0 + DY, grid(X, Y).

% Ensure no overlapping cells between patterns
:- pattern(P1, X1, Y1), pattern(P2, X2, Y2), P1 != P2,
   live(X, Y), pattern(P1, X1, Y1), pattern_cell(P1, DX1, DY1),
   X = X1 + DX1, Y = Y1 + DY1,
   pattern(P2, X2, Y2), pattern_cell(P2, DX2, DY2),
   X = X2 + DX2, Y = Y2 + DY2.

% Neighbor definition (Moore neighborhood)
neighbor(X, Y, XN, YN) :- grid(X, Y), grid(XN, YN),
                          -1 <= XN - X <= 1, -1 <= YN - Y <= 1,
                          (XN, YN) != (X, Y).

% Count live neighbors for each cell
live_neighbor_count(X, Y, N) :- live(X, Y),
                                N = #count { XN, YN : neighbor(X, Y, XN, YN), live(XN, YN) }.

% Still life conditions:
% 1. Every live cell must have exactly 2 or 3 live neighbors
:- live(X, Y), live_neighbor_count(X, Y, N), N != 2, N != 3.

% 2. Every dead cell must not have exactly 3 live neighbors
:- not live(X, Y), live_neighbor_count(X, Y, 3).

% Show the pattern placements and live cells
#show pattern/3.
#show live/2.