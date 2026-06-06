%%% DUNGEON GENERATION - Clingo ASP Model %%%

% ========== DOMAINS ==========
% Rooms
room(room1; room2; room3; room4; room5; room6; room7).
room_size(room1, small). room_size(room2, large). room_size(room3, small).
room_size(room4, medium). room_size(room5, medium). room_size(room6, small).
room_size(room7, large).
room_type(room1, entrance). room_type(room2, chamber). room_type(room3, corridor).
room_type(room4, chamber). room_type(room5, treasury). room_type(room6, corridor).
room_type(room7, boss_room).

% Connections (undirected)
conn(room1, room2). conn(room1, room3).
conn(room2, room4).
conn(room3, room5).
conn(room4, room6).
conn(room5, room6). conn(room5, room7).
conn(X, Y) :- conn(Y, X).
connected(X, Y) :- conn(X, Y).

% Treasures
treasure(treasure1; treasure2; treasure3).
treasure_value(treasure1, 100). treasure_value(treasure2, 500). treasure_value(treasure3, 1000).
treasure_rarity(treasure1, common). treasure_rarity(treasure2, rare). treasure_rarity(treasure3, legendary).

% Monsters
monster_type(goblin; orc; dragon).
monster_danger(goblin, 2). monster_danger(orc, 4). monster_danger(dragon, 8).
monster_group(goblin, 3). monster_group(orc, 2). monster_group(dragon, 1).

% ========== CHOICE RULES ==========

% 1. Treasure placement: each treasure in exactly one room
{ placed_in(T, R) : room(R) } 1 :- treasure(T).

% 2. Monster placement: monsters can be placed in multiple rooms
{ monster_group_placed(M, R) } :- monster_type(M), room(R).

% ========== DERIVED PREDICATES ==========

% Total danger per room
room_danger(R, D) :- D = #sum { Danger, M : monster_group_placed(M, R), monster_danger(M, Danger) }, room(R).

% ========== CONSTRAINTS ==========

% 3. Danger limit: each room's total danger must not exceed 10
:- room(R), room_danger(R, D), D > 10.

% 4. Connectivity: All rooms must be reachable from entrance (room1)
reachable(room1).
reachable(Y) :- reachable(X), conn(X, Y), room(Y).
:- room(R), not reachable(R).

% 5. Strategic placement: Rare treasures should be in higher-danger rooms than common treasures
rarer(legendary, rare). rarer(legendary, common). rarer(rare, common).

:- treasure(T1), treasure(T2), treasure_rarity(T1, R1), treasure_rarity(T2, R2),
   rarer(R1, R2), placed_in(T1, Rm1), placed_in(T2, Rm2),
   room_danger(Rm1, D1), room_danger(Rm2, D2), D1 < D2.

% ========== MINIMUM TREASURES PER PATH TO EXIT ==========
% There must be at least 1 treasure on every path from entrance (room1) to exit (room7)
% We forbid the existence of a treasure-free path from room1 to room7
treasure_free_reachable(room1) :- not placed_in(_, room1).
treasure_free_reachable(Y) :- treasure_free_reachable(X), conn(X, Y), room(Y), not placed_in(_, Y).
:- treasure_free_reachable(room7).

% ========== OUTPUT PREDICATES ==========

% Room layout output
room_layout(R, M, D) :- room(R), monster_group_placed(M, R), room_danger(R, D).
room_treasure(R, T) :- placed_in(T, R).

% Isolated rooms (should be empty)
isolated_room(R) :- room(R), not reachable(R).

% Balance analysis
total_danger(TD) :- TD = #sum { D, R : room_danger(R, D) }.

treasure_count_by_rarity(R, C) :- C = #count { T : treasure(T), treasure_rarity(T, R) }, rarity(R).
rarity(common; rare; legendary).

% Difficulty progression
total_danger_sum(TD) :- TD = #sum { D, R : room_danger(R, D) }.
avg_danger(A) :- total_danger_sum(TD), A = TD / 7.
difficulty_progression(easy) :- avg_danger(A), A <= 2.
difficulty_progression(balanced) :- avg_danger(A), A > 2, A <= 5.
difficulty_progression(hard) :- avg_danger(A), A > 5, A <= 8.
difficulty_progression(extreme) :- avg_danger(A), A > 8.

#show room_layout/3.
#show room_treasure/2.
#show isolated_room/1.
#show total_danger/1.
#show treasure_count_by_rarity/2.
#show difficulty_progression/1.