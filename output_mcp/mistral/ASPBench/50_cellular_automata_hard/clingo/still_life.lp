% Grid size
size(14).
cell(X,Y) :- size(Max), X = 1..Max, Y = 1..Max.

% Pattern definitions (relative coordinates)
block_rel(0,0). block_rel(0,1). block_rel(1,0). block_rel(1,1).
boat_rel(0,0). boat_rel(0,1). boat_rel(1,0). boat_rel(1,2). boat_rel(2,1).
loaf_rel(0,1). loaf_rel(0,2). loaf_rel(1,0). loaf_rel(1,3). loaf_rel(2,1). loaf_rel(2,3). loaf_rel(3,2).

% Exactly one placement for each pattern
1 { placed(block, R, C) : R = 1..13, C = 1..13 } 1.
1 { placed(boat, R, C) : R = 1..12, C = 1..12 } 1.
1 { placed(loaf, R, C) : R = 1..11, C = 1..11 } 1.

% Derive cells for block
block_cell(X,Y) :- placed(block, R, C), block_rel(DR, DC), X = R + DR, Y = C + DC, X <= 14, Y <= 14.

% Derive cells for boat
boat_cell(X,Y) :- placed(boat, R, C), boat_rel(DR, DC), X = R + DR, Y = C + DC, X <= 14, Y <= 14.

% Derive cells for loaf
loaf_cell(X,Y) :- placed(loaf, R, C), loaf_rel(DR, DC), X = R + DR, Y = C + DC, X <= 14, Y <= 14.

% No overlapping cells
:- block_cell(X,Y), boat_cell(X,Y).
:- block_cell(X,Y), loaf_cell(X,Y).
:- boat_cell(X,Y), loaf_cell(X,Y).

% Live cells are the union of all pattern cells
live(X,Y) :- block_cell(X,Y).
live(X,Y) :- boat_cell(X,Y).
live(X,Y) :- loaf_cell(X,Y).

% Neighbor relationships (8 directions)
neighbor(X,Y, X-1,Y-1) :- cell(X,Y), cell(X-1,Y-1).
neighbor(X,Y, X-1,Y  ) :- cell(X,Y), cell(X-1,Y  ).
neighbor(X,Y, X-1,Y+1) :- cell(X,Y), cell(X-1,Y+1).
neighbor(X,Y, X  ,Y-1) :- cell(X,Y), cell(X  ,Y-1).
neighbor(X,Y, X  ,Y+1) :- cell(X,Y), cell(X  ,Y+1).
neighbor(X,Y, X+1,Y-1) :- cell(X,Y), cell(X+1,Y-1).
neighbor(X,Y, X+1,Y  ) :- cell(X,Y), cell(X+1,Y  ).
neighbor(X,Y, X+1,Y+1) :- cell(X,Y), cell(X+1,Y+1).

% Count live neighbors for each cell
live_neighbors(X,Y,N) :- cell(X,Y), N = #count { X2,Y2 : neighbor(X,Y,X2,Y2), live(X2,Y2) }.

% Live cells must have 2 or 3 live neighbors
:- live(X,Y), live_neighbors(X,Y,N), N != 2, N != 3.

% Dead cells must not have exactly 3 live neighbors
:- cell(X,Y), not live(X,Y), live_neighbors(X,Y,3).

% Show the placements and live cells
#show placed/3.
#show live/2.