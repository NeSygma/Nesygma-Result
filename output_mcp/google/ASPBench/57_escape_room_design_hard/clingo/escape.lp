% --- Domain ---
room(r1; r2; r3; r4; r5).
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

prereq(2, 1).
prereq(3, 2).
prereq(4, 3).
prereq(5, 4).
prereq(6, 5).
prereq(7, 6).
prereq(8, 7).
prereq(9, 8).
prereq(10, 9).
prereq(11, 10).
prereq(12, 11).
prereq(13, 12).
prereq(14, 13).
prereq(15, 14).
prereq(16, 15).
prereq(17, 16).
prereq(18, 17).

requires(4, key_red).
requires(6, uv_light).
requires(9, key_blue).
requires(10, crowbar).
requires(12, uv_light).
requires(15, crowbar).
requires(17, uv_light).
requires(18, key_red).
requires(18, key_blue).

yields(2, key_red).
yields(5, uv_light).
yields(7, key_blue).
yields(8, crowbar).
yields(13, gear_1).
yields(15, gear_2).
yields(17, gear_3).

room_adj(r1, r2). room_adj(r2, r1).
room_adj(r2, r3). room_adj(r3, r2).
room_adj(r3, r4). room_adj(r4, r3).
room_adj(r4, r5). room_adj(r5, r4).
room_adj(R, R) :- room(R).

% --- Assignment ---
1 { order(ID, Step) : puzzle(ID, _, _, _) } 1 :- Step = 1..18.
1 { order(ID, Step) : Step = 1..18 } 1 :- puzzle(ID, _, _, _).

solved_at(ID, Step) :- order(ID, Step).

% --- Constraints ---
% 1. Prerequisite
:- prereq(ID, P), solved_at(ID, S1), solved_at(P, S2), S1 <= S2.

% 2. Item Requirement
% Define items
item(key_red; key_blue; uv_light; crowbar; gear_1; gear_2; gear_3).
has_item(Item, Step) :- yields(ID, Item), solved_at(ID, S), S <= Step, Step = 1..18.
:- requires(ID, Item), solved_at(ID, S), S > 1, not has_item(Item, S-1).
:- requires(ID, Item), solved_at(ID, 1). % Cannot require item at step 1

% 3. Room Adjacency
:- order(ID1, S), order(ID2, S+1), puzzle(ID1, R1, _, _), puzzle(ID2, R2, _, _), not room_adj(R1, R2).

% 4. Theme Balance
:- order(ID1, S), order(ID2, S+1), puzzle(ID1, _, _, T), puzzle(ID2, _, _, T).

% 5. Difficulty Curve
:- order(ID1, S), order(ID2, S+1), puzzle(ID1, _, D1, _), puzzle(ID2, _, D2, _), D1 - D2 > 1.
:- order(ID1, S), order(ID2, S+1), puzzle(ID1, _, D1, _), puzzle(ID2, _, D2, _), D2 - D1 > 1.

% --- Output ---
option(valid) :- #count { S : order(ID, S) } = 18.
#show order/2.
#show option/1.