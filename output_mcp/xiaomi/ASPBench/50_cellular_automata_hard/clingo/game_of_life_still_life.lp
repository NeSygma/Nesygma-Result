% Grid dimensions
#const n = 14.
row(0..n-1).
col(0..n-1).

% Cell coordinates
cell(R, C) :- row(R), col(C).

% Neighbor relation (Moore neighborhood)
neighbor(R, C, NR, NC) :- cell(R, C), NR = R-1, NC = C-1, cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R-1, NC = C,   cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R-1, NC = C+1, cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R,   NC = C-1, cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R,   NC = C+1, cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R+1, NC = C-1, cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R+1, NC = C,   cell(NR, NC).
neighbor(R, C, NR, NC) :- cell(R, C), NR = R+1, NC = C+1, cell(NR, NC).

% Pattern types
pattern_type(block).
pattern_type(boat).
pattern_type(loaf).

% Choose exactly one anchor for each pattern
1 { anchor(P, R, C) : cell(R, C) } 1 :- pattern_type(P).

% Block pattern cells (2x2 square): relative (0,0),(0,1),(1,0),(1,1)
pattern_cell(block, 0, 0).
pattern_cell(block, 0, 1).
pattern_cell(block, 1, 0).
pattern_cell(block, 1, 1).

% Boat pattern cells: relative (0,0),(0,1),(1,0),(1,2),(2,1)
pattern_cell(boat, 0, 0).
pattern_cell(boat, 0, 1).
pattern_cell(boat, 1, 0).
pattern_cell(boat, 1, 2).
pattern_cell(boat, 2, 1).

% Loaf pattern cells: relative (0,1),(0,2),(1,0),(1,3),(2,1),(2,3),(3,2)
pattern_cell(loaf, 0, 1).
pattern_cell(loaf, 0, 2).
pattern_cell(loaf, 1, 0).
pattern_cell(loaf, 1, 3).
pattern_cell(loaf, 2, 1).
pattern_cell(loaf, 2, 3).
pattern_cell(loaf, 3, 2).

% A cell is occupied by a pattern if it's within the pattern's footprint from its anchor
occupied_by(P, R+DR, C+DC) :- anchor(P, R, C), pattern_cell(P, DR, DC).

% Boundary constraint: all pattern cells must be within the grid
:- anchor(P, R, C), pattern_cell(P, DR, DC), R+DR < 0.
:- anchor(P, R, C), pattern_cell(P, DR, DC), R+DR >= n.
:- anchor(P, R, C), pattern_cell(P, DR, DC), C+DC < 0.
:- anchor(P, R, C), pattern_cell(P, DR, DC), C+DC >= n.

% No overlapping: a cell cannot be occupied by two different patterns
:- cell(R, C), occupied_by(P1, R, C), occupied_by(P2, R, C), P1 != P2.

% A cell is alive if it is occupied by any pattern
alive(R, C) :- occupied_by(_, R, C).

% Count live neighbors for each cell
live_neighbors(R, C, N) :- cell(R, C), N = #count { NR, NC : neighbor(R, C, NR, NC), alive(NR, NC) }.

% Still life constraints:
% 1. Every live cell must have exactly 2 or 3 live neighbors
:- alive(R, C), live_neighbors(R, C, N), N != 2, N != 3.

% 2. Every dead cell must NOT have exactly 3 live neighbors (no birth)
:- not alive(R, C), live_neighbors(R, C, 3).

% Show the grid
#show alive/2.
% Show pattern placements
#show anchor/3.