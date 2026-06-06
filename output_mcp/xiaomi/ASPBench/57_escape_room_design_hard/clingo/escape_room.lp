% ===== DOMAIN =====
puzzle(1..18).
position(1..18).
room(r1). room(r2). room(r3). room(r4). room(r5).

% ===== PUZZLE PROPERTIES =====
% puzzle_room(P, R)
puzzle_room(1, r1). puzzle_room(2, r1). puzzle_room(3, r2). puzzle_room(4, r2).
puzzle_room(5, r2). puzzle_room(6, r1). puzzle_room(7, r1). puzzle_room(8, r2).
puzzle_room(9, r3). puzzle_room(10, r4). puzzle_room(11, r4). puzzle_room(12, r3).
puzzle_room(13, r3). puzzle_room(14, r4). puzzle_room(15, r5). puzzle_room(16, r5).
puzzle_room(17, r5). puzzle_room(18, r5).

% difficulty(P, D)
difficulty(1,1). difficulty(2,1). difficulty(3,2). difficulty(4,2).
difficulty(5,2). difficulty(6,3). difficulty(7,3). difficulty(8,3).
difficulty(9,3). difficulty(10,3). difficulty(11,4). difficulty(12,4).
difficulty(13,4). difficulty(14,4). difficulty(15,4). difficulty(16,5).
difficulty(17,5). difficulty(18,5).

% theme(P, T)
theme(1, search). theme(2, logic). theme(3, physical). theme(4, search).
theme(5, logic). theme(6, search). theme(7, logic). theme(8, physical).
theme(9, search). theme(10, physical). theme(11, logic). theme(12, search).
theme(13, logic). theme(14, search). theme(15, physical). theme(16, logic).
theme(17, search). theme(18, logic).

% prereq(P, Q): Q must be solved before P
prereq(2, 1). prereq(3, 2). prereq(4, 3). prereq(5, 4).
prereq(6, 5). prereq(7, 6). prereq(8, 7). prereq(9, 8).
prereq(10, 9). prereq(11, 10). prereq(12, 11). prereq(13, 12).
prereq(14, 13). prereq(15, 14). prereq(16, 15). prereq(17, 16).
prereq(18, 17).

% requires(P, I): puzzle P requires item I
requires(4, key_red). requires(6, uv_light). requires(9, key_blue).
requires(10, crowbar). requires(12, uv_light). requires(15, crowbar).
requires(17, uv_light). requires(18, key_red). requires(18, key_blue).

% yields(P, I): puzzle P yields item I
yields(2, key_red). yields(5, uv_light). yields(7, key_blue).
yields(8, crowbar). yields(13, gear_1). yields(15, gear_2). yields(17, gear_3).

% item domain
item(key_red). item(key_blue). item(uv_light). item(crowbar).
item(gear_1). item(gear_2). item(gear_3).

% ===== CHOICE: ASSIGN EACH PUZZLE TO A POSITION =====
1 { pos(P, N) : position(N) } 1 :- puzzle(P).
1 { pos(P, N) : puzzle(P) } 1 :- position(N).

% ===== DERIVED: SOLVED AND INVENTORY AT EACH POSITION =====
% solved(P, N): puzzle P is solved at or before position N
solved(P, N) :- pos(P, N).
solved(P, N+1) :- solved(P, N), position(N+1).

% has_item(I, N): item I is in inventory at position N
% An item is acquired when the puzzle that yields it is solved
has_item(I, N) :- pos(P, N), yields(P, I).
has_item(I, N+1) :- has_item(I, N), position(N+1).

% ===== CONSTRAINT 1: PREREQUISITE CONSTRAINT =====
% If Q is a prerequisite of P, then Q must be solved before P
:- prereq(P, Q), pos(P, NP), pos(Q, NQ), NQ >= NP.

% ===== CONSTRAINT 2: ITEM REQUIREMENT CONSTRAINT =====
% A puzzle requiring item I can only be solved when I is already in inventory
% (i.e., some earlier puzzle yielded it)
% We check: at the position where P is solved, item I must already be in inventory
% from a previous position
:- requires(P, I), pos(P, NP), NP > 1, not has_item(I, NP - 1).
% Special case: if NP = 1, no item can be available, so puzzle requiring item can't be at pos 1
:- requires(P, I), pos(P, 1).

% ===== CONSTRAINT 3: ROOM ADJACENCY CONSTRAINT =====
% The room of consecutive puzzles must be the same or adjacent
adjacent(r1, r2). adjacent(r2, r1).
adjacent(r2, r3). adjacent(r3, r2).
adjacent(r3, r4). adjacent(r4, r3).
adjacent(r4, r5). adjacent(r5, r4).
% Same room is also allowed (reflexive)
adjacent(R, R) :- room(R).

:- pos(P1, N), pos(P2, N+1), puzzle_room(P1, R1), puzzle_room(P2, R2), not adjacent(R1, R2).

% ===== CONSTRAINT 4: THEME BALANCE CONSTRAINT =====
% No two consecutive puzzles can have the same theme
:- pos(P1, N), pos(P2, N+1), theme(P1, T), theme(P2, T).

% ===== CONSTRAINT 5: DIFFICULTY CURVE CONSTRAINT =====
% Difficulty difference between consecutive puzzles must be at most 1
:- pos(P1, N), pos(P2, N+1), difficulty(P1, D1), difficulty(P2, D2), |D1 - D2| > 1.

% ===== OUTPUT =====
#show pos/2.