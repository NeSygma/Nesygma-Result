% Crossword Puzzle Generator - 5x5 Grid with Technology Theme

% ===== DOMAIN DEFINITIONS =====
% Grid dimensions
row(0..4).
col(0..4).

% Words in the puzzle
word(code). word(data). word(tech). word(chip). word(byte). word(net).

% Word lengths
len(code, 4). len(data, 4). len(tech, 4). len(chip, 4). len(byte, 4). len(net, 3).

% Letters in each word (position, character)
% CODE: C-O-D-E
letter(code, 0, "C"). letter(code, 1, "O"). letter(code, 2, "D"). letter(code, 3, "E").
% DATA: D-A-T-A
letter(data, 0, "D"). letter(data, 1, "A"). letter(data, 2, "T"). letter(data, 3, "A").
% TECH: T-E-C-H
letter(tech, 0, "T"). letter(tech, 1, "E"). letter(tech, 2, "C"). letter(tech, 3, "H").
% CHIP: C-H-I-P
letter(chip, 0, "C"). letter(chip, 1, "H"). letter(chip, 2, "I"). letter(chip, 3, "P").
% BYTE: B-Y-T-E
letter(byte, 0, "B"). letter(byte, 1, "Y"). letter(byte, 2, "T"). letter(byte, 3, "E").
% NET: N-E-T
letter(net, 0, "N"). letter(net, 1, "E"). letter(net, 2, "T").

% Directions
dir(h). dir(v).  % horizontal, vertical

% ===== PLACEMENT CHOICE =====
% Each word must be placed exactly once with a position and direction
1 { placed(W, R, C, D) : row(R), col(C), dir(D) } 1 :- word(W).

% ===== BOUNDARY CONSTRAINTS =====
% Horizontal words must fit within grid columns
:- placed(W, R, C, h), len(W, L), C + L > 5.

% Vertical words must fit within grid rows
:- placed(W, R, C, v), len(W, L), R + L > 5.

% ===== CELL ASSIGNMENT =====
% For each placed word, determine which cells it occupies and what letter goes there
% Horizontal placement
cell(R, C+P, Ch) :- placed(W, R, C, h), letter(W, P, Ch), len(W, L), P < L.

% Vertical placement
cell(R+P, C, Ch) :- placed(W, R, C, v), letter(W, P, Ch), len(W, L), P < L.

% ===== NO CONFLICTS =====
% Each grid cell can have at most one letter
:- cell(R, C, Ch1), cell(R, C, Ch2), Ch1 != Ch2.

% ===== INTERSECTION DETECTION =====
% Two words intersect if they share a cell
% For horizontal word W1 at (R1,C1) and vertical word W2 at (R2,C2):
% They intersect at (R1, C2+P2) = (R1, C1+P1) when R2 <= R1 < R2+L2 and C1 <= C2+P2 < C1+L1
% This means: R1 = R2+P2 and C2+P2 = C1+P1

% Detect intersections between horizontal and vertical words
intersect(W1, W2, P1, P2) :- 
    placed(W1, R1, C1, h), placed(W2, R2, C2, v),
    letter(W1, P1, Ch), letter(W2, P2, Ch),
    len(W1, L1), len(W2, L2),
    P1 < L1, P2 < L2,
    R1 = R2 + P2, C2 + P2 = C1 + P1,
    W1 != W2.

% Also detect intersections between vertical and horizontal words (reverse order)
intersect(W1, W2, P1, P2) :- 
    placed(W1, R1, C1, v), placed(W2, R2, C2, h),
    letter(W1, P1, Ch), letter(W2, P2, Ch),
    len(W1, L1), len(W2, L2),
    P1 < L1, P2 < L2,
    R1 + P1 = R2, C1 = C2 + P1,
    W1 != W2.

% ===== REQUIRE INTERSECTIONS =====
% We want at least some intersections for a proper crossword
% Count total intersections
total_intersections(N) :- N = #count{W1,W2,P1,P2 : intersect(W1,W2,P1,P2)}.

% Require at least 3 intersections for a good crossword
:- total_intersections(N), N < 3.

% ===== SHOW OUTPUT =====
#show placed/4.
#show cell/3.
#show intersect/4.
#show total_intersections/1.