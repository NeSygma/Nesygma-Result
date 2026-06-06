%% Data
puzzle(1..18).
position(1..18).

%% Room facts
room(1, r1). room(2, r1). room(3, r2). room(4, r2). room(5, r2).
room(6, r1). room(7, r1). room(8, r2). room(9, r3). room(10, r4).
room(11, r4). room(12, r3). room(13, r3). room(14, r4). room(15, r5).
room(16, r5). room(17, r5). room(18, r5).

%% Difficulty facts
difficulty(1, 1). difficulty(2, 1). difficulty(3, 2). difficulty(4, 2).
difficulty(5, 2). difficulty(6, 3). difficulty(7, 3). difficulty(8, 3).
difficulty(9, 3). difficulty(10, 3). difficulty(11, 4). difficulty(12, 4).
difficulty(13, 4). difficulty(14, 4). difficulty(15, 4). difficulty(16, 5).
difficulty(17, 5). difficulty(18, 5).

%% Theme facts
theme(1, search). theme(2, logic). theme(3, physical). theme(4, search).
theme(5, logic). theme(6, search). theme(7, logic). theme(8, physical).
theme(9, search). theme(10, physical). theme(11, logic). theme(12, search).
theme(13, logic). theme(14, search). theme(15, physical). theme(16, logic).
theme(17, search). theme(18, logic).

%% Prerequisites: prereq(puzzle, prerequisite)
prereq(2, 1). prereq(3, 2). prereq(4, 3). prereq(5, 4).
prereq(6, 5). prereq(7, 6). prereq(8, 7). prereq(9, 8).
prereq(10, 9). prereq(11, 10). prereq(12, 11). prereq(13, 12).
prereq(14, 13). prereq(15, 14). prereq(16, 15). prereq(17, 16).
prereq(18, 17).

%% Items required: requires_item(puzzle, item)
requires_item(4, key_red).
requires_item(6, uv_light).
requires_item(9, key_blue).
requires_item(10, crowbar).
requires_item(12, uv_light).
requires_item(15, crowbar).
requires_item(17, uv_light).
requires_item(18, key_red; key_blue).

%% Items yielded: yields_item(puzzle, item)
yields_item(2, key_red).
yields_item(5, uv_light).
yields_item(7, key_blue).
yields_item(8, crowbar).
yields_item(13, gear_1).
yields_item(15, gear_2).
yields_item(17, gear_3).

%% Adjacent rooms (same or adjacent)
adjacent(r1, r1). adjacent(r1, r2). adjacent(r2, r1). adjacent(r2, r2).
adjacent(r2, r3). adjacent(r3, r2). adjacent(r3, r3). adjacent(r3, r4).
adjacent(r4, r3). adjacent(r4, r4). adjacent(r4, r5). adjacent(r5, r4).
adjacent(r5, r5).

%% Assignment: each position gets exactly one puzzle, each puzzle at exactly one position
1 { assign(P, Pos) : puzzle(P) } 1 :- position(Pos).
1 { assign(P, Pos) : position(Pos) } 1 :- puzzle(P).

%% Constraint 1: Prerequisite ordering
:- assign(P, PosP), assign(Prereq, PosPrereq), prereq(P, Prereq), PosP <= PosPrereq.

%% Constraint 2: Item requirement
available(P, I) :- requires_item(P, I), yields_item(Q, I), assign(P, PosP), assign(Q, PosQ), PosQ < PosP.
:- requires_item(P, I), not available(P, I).

%% Constraint 3: Room adjacency
:- assign(P1, Pos), assign(P2, Pos+1), room(P1, R1), room(P2, R2), not adjacent(R1, R2).

%% Constraint 4: Theme balance
:- assign(P1, Pos), assign(P2, Pos+1), theme(P1, T), theme(P2, T).

%% Constraint 5: Difficulty curve
:- assign(P1, Pos), assign(P2, Pos+1), difficulty(P1, D1), difficulty(P2, D2), D1 - D2 > 1.
:- assign(P1, Pos), assign(P2, Pos+1), difficulty(P1, D1), difficulty(P2, D2), D2 - D1 > 1.

%% Output fields
puzzle_order(Pos, P) :- assign(P, Pos).
room_progression(Pos, R) :- assign(P, Pos), room(P, R).
difficulty_progression(Pos, D) :- assign(P, Pos), difficulty(P, D).
theme_progression(Pos, T) :- assign(P, Pos), theme(P, T).
all_constraints_satisfied(true).

%% puzzle_details per puzzle
puzzle_details(P, R, D, T) :- puzzle(P), room(P, R), difficulty(P, D), theme(P, T).

#show puzzle_order/2.
#show room_progression/2.
#show difficulty_progression/2.
#show theme_progression/2.
#show all_constraints_satisfied/1.
#show puzzle_details/4.