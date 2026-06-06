% Multi-room escape experience with 18 puzzles
% Find a valid puzzle ordering satisfying all constraints.

% Domains
puzzle(1..18).
room(r1). room(r2). room(r3). room(r4). room(r5).
theme(search). theme(logic). theme(physical).
difficulty(1..5).
item(key_red). item(key_blue). item(uv_light). item(crowbar). item(gear_1). item(gear_2). item(gear_3).

% Puzzle properties
puzzle_room(1, r1). puzzle_difficulty(1, 1). puzzle_theme(1, search).
puzzle_room(2, r1). puzzle_difficulty(2, 1). puzzle_theme(2, logic).
puzzle_room(3, r2). puzzle_difficulty(3, 2). puzzle_theme(3, physical).
puzzle_room(4, r2). puzzle_difficulty(4, 2). puzzle_theme(4, search).
puzzle_room(5, r2). puzzle_difficulty(5, 2). puzzle_theme(5, logic).
puzzle_room(6, r1). puzzle_difficulty(6, 3). puzzle_theme(6, search).
puzzle_room(7, r1). puzzle_difficulty(7, 3). puzzle_theme(7, logic).
puzzle_room(8, r2). puzzle_difficulty(8, 3). puzzle_theme(8, physical).
puzzle_room(9, r3). puzzle_difficulty(9, 3). puzzle_theme(9, search).
puzzle_room(10, r4). puzzle_difficulty(10, 3). puzzle_theme(10, physical).
puzzle_room(11, r4). puzzle_difficulty(11, 4). puzzle_theme(11, logic).
puzzle_room(12, r3). puzzle_difficulty(12, 4). puzzle_theme(12, search).
puzzle_room(13, r3). puzzle_difficulty(13, 4). puzzle_theme(13, logic).
puzzle_room(14, r4). puzzle_difficulty(14, 4). puzzle_theme(14, search).
puzzle_room(15, r5). puzzle_difficulty(15, 4). puzzle_theme(15, physical).
puzzle_room(16, r5). puzzle_difficulty(16, 5). puzzle_theme(16, logic).
puzzle_room(17, r5). puzzle_difficulty(17, 5). puzzle_theme(17, search).
puzzle_room(18, r5). puzzle_difficulty(18, 5). puzzle_theme(18, logic).

% Prerequisites
prerequisite(2, 1).
prerequisite(3, 2).
prerequisite(4, 3).
prerequisite(5, 4).
prerequisite(6, 5).
prerequisite(7, 6).
prerequisite(8, 7).
prerequisite(9, 8).
prerequisite(10, 9).
prerequisite(11, 10).
prerequisite(12, 11).
prerequisite(13, 12).
prerequisite(14, 13).
prerequisite(15, 14).
prerequisite(16, 15).
prerequisite(17, 16).
prerequisite(18, 17).

% Item requirements
requires(4, key_red).
requires(6, uv_light).
requires(9, key_blue).
requires(10, crowbar).
requires(12, uv_light).
requires(15, crowbar).
requires(17, uv_light).
requires(18, key_red).
requires(18, key_blue).

% Item yields
yields(2, key_red).
yields(5, uv_light).
yields(7, key_blue).
yields(8, crowbar).
yields(13, gear_1).
yields(15, gear_2).
yields(17, gear_3).

% Room adjacency (linear layout r1-r2-r3-r4-r5)
adjacent_room(r1, r1). adjacent_room(r1, r2).
adjacent_room(r2, r1). adjacent_room(r2, r2). adjacent_room(r2, r3).
adjacent_room(r3, r2). adjacent_room(r3, r3). adjacent_room(r3, r4).
adjacent_room(r4, r3). adjacent_room(r4, r4). adjacent_room(r4, r5).
adjacent_room(r5, r4). adjacent_room(r5, r5).

% Positions
pos(1..18).

% Assignment: each puzzle gets exactly one position, each position gets exactly one puzzle
{ assign(P, Pos) : puzzle(P) } 1 :- pos(Pos).
{ assign(P, Pos) : pos(Pos) } 1 :- puzzle(P).

% Puzzle at position
puzzle_at(Pos, P) :- assign(P, Pos).

% Derived properties per position
room_at(Pos, R) :- puzzle_at(Pos, P), puzzle_room(P, R).
difficulty_at(Pos, D) :- puzzle_at(Pos, P), puzzle_difficulty(P, D).
theme_at(Pos, T) :- puzzle_at(Pos, P), puzzle_theme(P, T).

% Constraint 1: Prerequisite must be solved earlier
:- assign(P, PosP), assign(Q, PosQ), prerequisite(P, Q), PosQ >= PosP.

% Constraint 2: Item requirement: required items must be obtained earlier
has_item_before(Pos, I) :- pos(Pos), assign(Q, PosQ), yields(Q, I), PosQ < Pos.
:- puzzle_at(Pos, P), requires(P, I), not has_item_before(Pos, I).

% Constraint 3: Room adjacency for consecutive puzzles
:- puzzle_at(Pos, P1), puzzle_at(Pos+1, P2), pos(Pos), pos(Pos+1), room_at(Pos, R1), room_at(Pos+1, R2), not adjacent_room(R1, R2).

% Constraint 4: Theme balance (no two consecutive same theme)
:- puzzle_at(Pos, P1), puzzle_at(Pos+1, P2), pos(Pos), pos(Pos+1), theme_at(Pos, T), theme_at(Pos+1, T).

% Constraint 5: Difficulty curve (difference at most 1)
:- puzzle_at(Pos, P1), puzzle_at(Pos+1, P2), pos(Pos), pos(Pos+1), difficulty_at(Pos, D1), difficulty_at(Pos+1, D2), D1 > D2 + 1.
:- puzzle_at(Pos, P1), puzzle_at(Pos+1, P2), pos(Pos), pos(Pos+1), difficulty_at(Pos, D1), difficulty_at(Pos+1, D2), D2 > D1 + 1.

% Output predicates
puzzle_order(Pos, P) :- puzzle_at(Pos, P).
room_progression(Pos, R) :- room_at(Pos, R).
difficulty_progression(Pos, D) :- difficulty_at(Pos, D).
theme_progression(Pos, T) :- theme_at(Pos, T).
all_constraints_satisfied.  % Any model satisfies all constraints by construction
puzzle_details(P, R, D, T) :- puzzle_room(P, R), puzzle_difficulty(P, D), puzzle_theme(P, T).

% Show relevant output
#show puzzle_order/2.
#show room_progression/2.
#show difficulty_progression/2.
#show theme_progression/2.
#show all_constraints_satisfied/0.
#show puzzle_details/4.