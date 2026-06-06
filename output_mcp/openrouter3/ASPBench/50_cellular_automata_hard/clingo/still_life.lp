% Conway's Game of Life Still Life Configuration
% 14x14 grid with Block, Boat, and Loaf patterns

% ==================== DOMAIN DEFINITIONS ====================
% Grid cells (0-13 for 14x14 grid)
grid(R, C) :- R = 0..13, C = 0..13.

% Pattern types
pattern_type("block", block).
pattern_type("boat", boat).
pattern_type("loaf", loaf).

% ==================== PATTERN DEFINITIONS ====================
% Block: 2x2 square at relative positions (0,0), (0,1), (1,0), (1,1)
block_cell(0, 0). block_cell(0, 1). block_cell(1, 0). block_cell(1, 1).

% Boat: 5 cells at relative positions (0,0), (0,1), (1,0), (1,2), (2,1)
boat_cell(0, 0). boat_cell(0, 1). boat_cell(1, 0). boat_cell(1, 2). boat_cell(2, 1).

% Loaf: 7 cells at relative positions (0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)
loaf_cell(0, 1). loaf_cell(0, 2). loaf_cell(1, 0). loaf_cell(1, 3).
loaf_cell(2, 1). loaf_cell(2, 3). loaf_cell(3, 2).

% ==================== PATTERN PLACEMENT ====================
% Each pattern has an anchor point (top-left corner of bounding box)
% Block: 2x2, Boat: 3x3, Loaf: 4x4
{ place_pattern(P, Type, R, C) } :- 
    pattern_type(P, Type),
    grid(R, C).

% Block placement constraints (must fit in 14x14)
:- place_pattern(P, block, R, C), 
   (R > 11; C > 11).  % Block needs 2x2 space

% Boat placement constraints (needs 3x3 space)
:- place_pattern(P, boat, R, C),
   (R > 11; C > 11).  % Boat needs 3x3 space

% Loaf placement constraints (needs 4x4 space)
:- place_pattern(P, loaf, R, C),
   (R > 10; C > 10).  % Loaf needs 4x4 space

% ==================== PATTERN CELLS ====================
% Derive live cells from pattern placements
live(R, C) :- place_pattern(P, block, R0, C0),
              block_cell(DR, DC),
              R = R0 + DR, C = C0 + DC.

live(R, C) :- place_pattern(P, boat, R0, C0),
              boat_cell(DR, DC),
              R = R0 + DR, C = C0 + DC.

live(R, C) :- place_pattern(P, loaf, R0, C0),
              loaf_cell(DR, DC),
              R = R0 + DR, C = C0 + DC.

% ==================== NO OVERLAP CONSTRAINT ====================
% Ensure patterns don't overlap
:- live(R, C), #count{P : place_pattern(P, _, R0, C0), 
                      (P = block, block_cell(R-R0, C-C0) |
                       P = boat, boat_cell(R-R0, C-C0) |
                       P = loaf, loaf_cell(R-R0, C-C0))} > 1.

% ==================== NEIGHBOR COUNTING ====================
% Count live neighbors for each cell (8 directions)
neighbor_count(R, C, N) :- grid(R, C),
    N = #count{ NR, NC : live(NR, NC), 
                NR >= 0, NR <= 13, NC >= 0, NC <= 13,
                (NR != R; NC != C),
                |NR - R| <= 1, |NC - C| <= 1 }.

% ==================== STILL LIFE CONSTRAINTS ====================
% A still life is stable when:
% 1. Every live cell has exactly 2 or 3 live neighbors
% 2. Every dead cell does NOT have exactly 3 live neighbors

% Constraint 1: Live cells must have 2 or 3 neighbors
:- live(R, C), neighbor_count(R, C, N), N != 2, N != 3.

% Constraint 2: Dead cells must NOT have exactly 3 neighbors
:- not live(R, C), neighbor_count(R, C, 3).

% ==================== EXACTLY ONE OF EACH PATTERN ====================
% Exactly one block
1 { place_pattern(P, block, R, C) : grid(R, C) } 1 :- pattern_type(P, block).

% Exactly one boat
1 { place_pattern(P, boat, R, C) : grid(R, C) } 1 :- pattern_type(P, boat).

% Exactly one loaf
1 { place_pattern(P, loaf, R, C) : grid(R, C) } 1 :- pattern_type(P, loaf).

% ==================== OUTPUT ====================
% Show the grid configuration
#show live/2.
#show place_pattern/4.