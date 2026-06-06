% Define the 5 rooms
room(r1). room(r2). room(r3). room(r4). room(r5).

% Define the 18 puzzles with their properties
% Format: puzzle(ID, room, difficulty, theme)
puzzle(1, r1, 1, search).
puzzle(2, r1, 1, logic).
puzzle(3, r2, 2, physical).
puzzle(4, r2, 2, search).
puzzle(5, r2, 2, logic).
puzzle(6, r1, 3, search).
puzzle(7, r1, 3, logic).
puzzle(8, r2, 3, physical).
puzzle(9, r3, 3, search).
puzzle(10, r4, 3, physical).
puzzle(11, r4, 4, logic).
puzzle(12, r3, 4, search).
puzzle(13, r3, 4, logic).
puzzle(14, r4, 4, search).
puzzle(15, r5, 4, physical).
puzzle(16, r5, 5, logic).
puzzle(17, r5, 5, search).
puzzle(18, r5, 5, logic).

% Define items and their relationships
% Items required by puzzles
requires_item(4, key_red).
requires_item(18, key_red).
requires_item(9, key_blue).
requires_item(18, key_blue).
requires_item(6, uv_light).
requires_item(12, uv_light).
requires_item(17, uv_light).
requires_item(10, crowbar).
requires_item(15, crowbar).

% Items yielded by puzzles
yields_item(2, key_red).
yields_item(7, key_blue).
yields_item(5, uv_light).
yields_item(8, crowbar).
yields_item(13, gear_1).
yields_item(15, gear_2).
yields_item(17, gear_3).

% Prerequisites for puzzles
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

% Define the set of all puzzles
puzzle_id(1..18).

% Define the set of all positions (1 to 18)
position(1..18).

% Define adjacency between rooms
adjacent(R1, R2) :- room(R1), room(R2), R1 = r1, R2 = r2.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r2, R2 = r1.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r2, R2 = r3.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r3, R2 = r2.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r3, R2 = r4.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r4, R2 = r3.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r4, R2 = r5.
adjacent(R1, R2) :- room(R1), room(R2), R1 = r5, R2 = r4.

% Define themes
theme(search). theme(logic). theme(physical).

% Choice rule: assign a puzzle to each position
1 { puzzle_order(P, ID) : puzzle_id(ID) } 1 :- position(P).

% Ensure each puzzle appears exactly once in the ordering
:- puzzle_id(ID), 2 { puzzle_order(P, ID) : position(P) }.

% Helper: solved(P, ID) means puzzle ID is solved at position P
solved(P, ID) :- puzzle_order(P, ID).

% Ensure all prerequisites are solved before a puzzle
:- puzzle_order(P, ID), prerequisite(ID, Pre),
   not solved(Pp, Pre), Pp < P.

% Track collected items: An item is collected if it is yielded by a puzzle solved earlier
collected_item(P, Item) :-
    position(P), puzzle_order(Pp, IDp), Pp < P, yields_item(IDp, Item).

% Item requirement constraint: If a puzzle requires an item, that item must be collected before solving it
:- puzzle_order(P, ID), requires_item(ID, Item),
   not collected_item(P, Item).

% Room adjacency constraint: Consecutive puzzles must be in the same or adjacent rooms
:- puzzle_order(P, ID1), puzzle_order(P+1, ID2), P < 18,
   puzzle(ID1, Room1, _, _), puzzle(ID2, Room2, _, _),
   not adjacent(Room1, Room2), Room1 != Room2.

% Theme balance constraint: No two consecutive puzzles can have the same theme
:- puzzle_order(P, ID1), puzzle_order(P+1, ID2), P < 18,
   puzzle(ID1, _, _, Theme), puzzle(ID2, _, _, Theme).

% Difficulty curve constraint: Difficulty difference between consecutive puzzles <= 1
:- puzzle_order(P, ID1), puzzle_order(P+1, ID2), P < 18,
   puzzle(ID1, _, Diff1, _), puzzle(ID2, _, Diff2, _),
   abs(Diff1 - Diff2) > 1.

% Show the solution
#show puzzle_order/2.
#show puzzle/4.
#show requires_item/2.
#show yields_item/2.
#show prerequisite/2.