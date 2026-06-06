%%% Escape Room Puzzle Ordering %%%

%%% DOMAIN DEFINITIONS %%%

% 18 puzzles
puzzle(1..18).

% 5 rooms
room(r1; r2; r3; r4; r5).

% Difficulty levels 1-5
difficulty(1..5).

% Themes
theme(search; logic; physical).

% Items
item(key_red; key_blue; uv_light; crowbar; gear_1; gear_2; gear_3).

% Positions in the sequence (1..18)
position(1..18).

%%% FIXED PUZZLE PROPERTIES %%%

% puzzle_room(ID, Room)
puzzle_room(1, r1). puzzle_room(2, r1). puzzle_room(3, r2). puzzle_room(4, r2).
puzzle_room(5, r2). puzzle_room(6, r1). puzzle_room(7, r1). puzzle_room(8, r2).
puzzle_room(9, r3). puzzle_room(10, r4). puzzle_room(11, r4). puzzle_room(12, r3).
puzzle_room(13, r3). puzzle_room(14, r4). puzzle_room(15, r5). puzzle_room(16, r5).
puzzle_room(17, r5). puzzle_room(18, r5).

% puzzle_difficulty(ID, Level)
puzzle_difficulty(1, 1). puzzle_difficulty(2, 1). puzzle_difficulty(3, 2).
puzzle_difficulty(4, 2). puzzle_difficulty(5, 2). puzzle_difficulty(6, 3).
puzzle_difficulty(7, 3). puzzle_difficulty(8, 3). puzzle_difficulty(9, 3).
puzzle_difficulty(10, 3). puzzle_difficulty(11, 4). puzzle_difficulty(12, 4).
puzzle_difficulty(13, 4). puzzle_difficulty(14, 4). puzzle_difficulty(15, 4).
puzzle_difficulty(16, 5). puzzle_difficulty(17, 5). puzzle_difficulty(18, 5).

% puzzle_theme(ID, Theme)
puzzle_theme(1, search). puzzle_theme(2, logic). puzzle_theme(3, physical).
puzzle_theme(4, search). puzzle_theme(5, logic). puzzle_theme(6, search).
puzzle_theme(7, logic). puzzle_theme(8, physical). puzzle_theme(9, search).
puzzle_theme(10, physical). puzzle_theme(11, logic). puzzle_theme(12, search).
puzzle_theme(13, logic). puzzle_theme(14, search). puzzle_theme(15, physical).
puzzle_theme(16, logic). puzzle_theme(17, search). puzzle_theme(18, logic).

% Prerequisites: puzzle_prereq(ID, PrereqID)
puzzle_prereq(2, 1). puzzle_prereq(3, 2). puzzle_prereq(4, 3). puzzle_prereq(5, 4).
puzzle_prereq(6, 5). puzzle_prereq(7, 6). puzzle_prereq(8, 7). puzzle_prereq(9, 8).
puzzle_prereq(10, 9). puzzle_prereq(11, 10). puzzle_prereq(12, 11). puzzle_prereq(13, 12).
puzzle_prereq(14, 13). puzzle_prereq(15, 14). puzzle_prereq(16, 15). puzzle_prereq(17, 16).
puzzle_prereq(18, 17).

% Item requirements: puzzle_requires_item(ID, Item)
puzzle_requires_item(4, key_red). puzzle_requires_item(6, uv_light).
puzzle_requires_item(9, key_blue). puzzle_requires_item(10, crowbar).
puzzle_requires_item(12, uv_light). puzzle_requires_item(15, crowbar).
puzzle_requires_item(17, uv_light). puzzle_requires_item(18, key_red).
puzzle_requires_item(18, key_blue).

% Item yields: puzzle_yields_item(ID, Item)
puzzle_yields_item(2, key_red). puzzle_yields_item(5, uv_light).
puzzle_yields_item(7, key_blue). puzzle_yields_item(8, crowbar).
puzzle_yields_item(13, gear_1). puzzle_yields_item(15, gear_2).
puzzle_yields_item(17, gear_3).

% Room adjacency
adjacent(r1, r2). adjacent(r2, r1).
adjacent(r2, r3). adjacent(r3, r2).
adjacent(r3, r4). adjacent(r4, r3).
adjacent(r4, r5). adjacent(r5, r4).

%%% CHOICE: Assign each puzzle to a unique position %%%

% Each position gets exactly one puzzle
1 { order(Pos, P) : puzzle(P) } 1 :- position(Pos).

% Each puzzle appears in exactly one position
1 { order(Pos, P) : position(Pos) } 1 :- puzzle(P).

%%% CONSTRAINT 1: Prerequisite Constraint %%%
% If puzzle P has prerequisite Q, then Q must be at an earlier position than P.
:- order(PosQ, Q), order(PosP, P), puzzle_prereq(P, Q), PosQ >= PosP.

%%% CONSTRAINT 2: Item Requirement Constraint %%%
% Helper: item_yielded_at(Item, Pos) - item Item is yielded by puzzle at position Pos
item_yielded_at(Item, Pos) :- order(Pos, P), puzzle_yields_item(P, Item).

% Helper: item_available(Item, Pos) - item Item is available before solving puzzle at position Pos
item_available(Item, Pos) :- position(Pos), item(Item), item_yielded_at(Item, Pos2), Pos2 < Pos.

% Constraint: If puzzle at position Pos requires item Item, Item must be available before Pos.
:- order(Pos, P), puzzle_requires_item(P, Item), not item_available(Item, Pos).

%%% CONSTRAINT 3: Room Adjacency Constraint %%%
% The rooms of consecutive puzzles must be the same or adjacent.
:- order(Pos, P1), order(Pos+1, P2), puzzle_room(P1, R1), puzzle_room(P2, R2), R1 != R2, not adjacent(R1, R2).

%%% CONSTRAINT 4: Theme Balance Constraint %%%
% No two consecutive puzzles can have the same theme.
:- order(Pos, P1), order(Pos+1, P2), puzzle_theme(P1, T), puzzle_theme(P2, T).

%%% CONSTRAINT 5: Difficulty Curve Constraint %%%
% Difficulty difference between consecutive puzzles must be at most 1.
:- order(Pos, P1), order(Pos+1, P2), puzzle_difficulty(P1, D1), puzzle_difficulty(P2, D2), |D1 - D2| > 1.

%%% OUTPUT %%%

% Show the ordering
#show order/2.

% For convenience, show derived progression info
room_at(Pos, R) :- order(Pos, P), puzzle_room(P, R).
diff_at(Pos, D) :- order(Pos, P), puzzle_difficulty(P, D).
theme_at(Pos, T) :- order(Pos, P), puzzle_theme(P, T).

#show room_at/2.
#show diff_at/2.
#show theme_at/2.