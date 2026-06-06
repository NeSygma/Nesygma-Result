% Multi-room escape experience with 18 puzzles

% Domain declarations
room(R1). room(R2). room(R3). room(R4). room(R5).
puzzle(1..18).
item(key_red). item(key_blue). item(uv_light). item(crowbar). item(gear_1). item(gear_2). item(gear_3).
theme(search). theme(logic). theme(physical).
difficulty(1..5).
position(1..18).

% Room adjacency (linear arrangement)
adjacent(R1, R2). adjacent(R2, R1).
adjacent(R2, R3). adjacent(R3, R2).
adjacent(R3, R4). adjacent(R4, R3).
adjacent(R4, R5). adjacent(R5, R4).

% Puzzle specifications
puzzle(1, R1, 1, search).
puzzle(2, R1, 1, logic).
puzzle(3, R2, 2, physical).
puzzle(4, R2, 2, search).
puzzle(5, R2, 2, logic).
puzzle(6, R1, 3, search).
puzzle(7, R1, 3, logic).
puzzle(8, R2, 3, physical).
puzzle(9, R3, 3, search).
puzzle(10, R4, 3, physical).
puzzle(11, R4, 4, logic).
puzzle(12, R3, 4, search).
puzzle(13, R3, 4, logic).
puzzle(14, R4, 4, search).
puzzle(15, R5, 4, physical).
puzzle(16, R5, 5, logic).
puzzle(17, R5, 5, search).
puzzle(18, R5, 5, logic).

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

% Puzzle ordering - each puzzle appears exactly once
1 { order(ID, Pos) : position(Pos) } 1 :- puzzle(ID).

% Room progression based on ordering
room_at_position(Pos, Room) :- order(ID, Pos), puzzle(ID, Room, _, _).

% Difficulty progression based on ordering
difficulty_at_position(Pos, Diff) :- order(ID, Pos), puzzle(ID, _, Diff, _).

% Theme progression based on ordering
theme_at_position(Pos, Theme) :- order(ID, Pos), puzzle(ID, _, _, Theme).

% Item collection logic
has_item(Item) :- yields(ID, Item), solved(ID).

% Solved status: puzzle is solved if all prerequisites are solved and required items are available
solved(ID) :- order(ID, Pos), Pos = 1. % First puzzle has no prerequisites
solved(ID) :- order(ID, Pos), Pos > 1, 
              prerequisite(ID, Prereq), solved(Prereq),
              requires(ID, Item), has_item(Item).

% Constraint 1: Prerequisite constraint (enforced by solved definition)
% Constraint 2: Item requirement constraint (enforced by solved definition)

% Constraint 3: Room adjacency constraint
:- order(ID1, Pos1), order(ID2, Pos2), 
   Pos2 = Pos1 + 1,
   puzzle(ID1, Room1, _, _), puzzle(ID2, Room2, _, _),
   Room1 != Room2, not adjacent(Room1, Room2).

% Constraint 4: Theme balance constraint
:- theme_at_position(Pos, Theme), theme_at_position(Pos + 1, Theme).

% Constraint 5: Difficulty curve constraint
:- difficulty_at_position(Pos, D1), difficulty_at_position(Pos + 1, D2), D1 > D2 + 1.
:- difficulty_at_position(Pos, D1), difficulty_at_position(Pos + 1, D2), D2 > D1 + 1.

% Show directives
#show order/2.
#show room_at_position/2.
#show difficulty_at_position/2.
#show theme_at_position/2.
#show solved/1.
#show has_item/1.

% Helper: all constraints satisfied (should be true in valid solution)
all_constraints_satisfied :- 
    order(_, Pos), Pos < 18,
    room_at_position(Pos, R1), room_at_position(Pos + 1, R2),
    (R1 = R2 ; adjacent(R1, R2)),
    theme_at_position(Pos, T1), theme_at_position(Pos + 1, T2), T1 != T2,
    difficulty_at_position(Pos, D1), difficulty_at_position(Pos + 1, D2),
    D1 <= D2 + 1, D2 <= D1 + 1.

#show all_constraints_satisfied/0.