% Roguelike Dungeon Generation Problem

% ===== 1. ROOM DEFINITIONS =====
room(room1). room(room2). room(room3). room(room4). room(room5). room(room6). room(room7).

% Room types
room_type(room1, entrance). room_type(room2, chamber). room_type(room3, corridor).
room_type(room4, chamber). room_type(room5, treasury). room_type(room6, corridor). room_type(room7, boss_room).

% Room sizes
room_size(room1, small). room_size(room2, large). room_size(room3, small).
room_size(room4, medium). room_size(room5, medium). room_size(room6, small). room_size(room7, large).

% Connections (bidirectional)
connects(room1, room2). connects(room2, room1).
connects(room1, room3). connects(room3, room1).
connects(room2, room4). connects(room4, room2).
connects(room3, room5). connects(room5, room3).
connects(room4, room6). connects(room6, room4).
connects(room5, room6). connects(room6, room5).
connects(room5, room7). connects(room7, room5).

% ===== 2. TREASURE DEFINITIONS =====
treasure(treasure1). treasure(treasure2). treasure(treasure3).

% Treasure properties
treasure_value(treasure1, 100). treasure_value(treasure2, 500). treasure_value(treasure3, 1000).
treasure_rarity(treasure1, common). treasure_rarity(treasure2, rare). treasure_rarity(treasure3, legendary).

% ===== 3. MONSTER DEFINITIONS =====
monster(goblin). monster(orc). monster(dragon).

% Monster properties
monster_danger(goblin, 2). monster_danger(orc, 4). monster_danger(dragon, 8).
monster_group_size(goblin, 3). monster_group_size(orc, 2). monster_group_size(dragon, 1).

% ===== 4. TREASURE PLACEMENT =====
% Each treasure must be placed in exactly one room
{ treasure_in(T, R) : room(R) } 1 :- treasure(T).

% ===== 5. MONSTER PLACEMENT =====
% Monsters can be placed in multiple rooms, respecting group size limits
% For each monster type and room, we can place 0 to group_size monsters
{ monster_in(M, R, Count) : Count = 0..GroupSize } :- monster(M), room(R), monster_group_size(M, GroupSize).

% ===== 6. DANGER CALCULATION =====
% Calculate total danger per room (monsters only, as treasures don't add danger)
room_danger(R, D) :- room(R), D = #sum { Danger, M : monster_in(M, R, Count), monster_danger(M, Danger), Count > 0 }.

% ===== 7. DANGER CONSTRAINT =====
% Each room's total danger must not exceed 10
:- room_danger(R, D), D > 10.

% ===== 8. CONNECTIVITY =====
% Entrance is reachable
reachable(room1).

% Rooms are reachable if connected to a reachable room
reachable(R2) :- reachable(R1), connects(R1, R2).

% All rooms must be reachable from entrance
:- room(R), not reachable(R).

% ===== 9. PATH TO EXIT =====
% Exit is room7 (boss_room)
path_to_exit(room7).

% Rooms on path to exit (connected to exit or to rooms on path)
path_to_exit(R) :- connects(R, room7).
path_to_exit(R) :- connects(R, S), path_to_exit(S).

% ===== 10. STRATEGIC PLACEMENT =====
% Rare treasures should be in higher-danger rooms than common treasures
% For each common treasure, find its room and danger
common_treasure_room(T, R, D) :- treasure_in(T, R), treasure_rarity(T, common), room_danger(R, D).

% For each rare treasure, find its room and danger
rare_treasure_room(T, R, D) :- treasure_in(T, R), treasure_rarity(T, rare), room_danger(R, D).

% Rare treasures must be in rooms with higher danger than common treasures
:- common_treasure_room(_, R1, D1), rare_treasure_room(_, R2, D2), D2 <= D1.

% ===== 11. MINIMUM TREASURES PER PATH =====
% Minimum 1 treasure per path to exit (from entrance to boss_room)
% Count treasures on path to exit
treasures_on_path(N) :- N = #count { T : treasure_in(T, R), path_to_exit(R) }.
:- treasures_on_path(N), N < 1.

% ===== 12. OUTPUT =====
% Show room layout with monsters and treasures
room_layout(R, Type, Size, Danger, Monsters, Treasures) :-
    room(R), room_type(R, Type), room_size(R, Size), room_danger(R, Danger),
    Monsters = #count { M, C : monster_in(M, R, C), C > 0 },
    Treasures = #count { T : treasure_in(T, R) }.

% Show connectivity paths
connectivity_paths(R1, R2, Danger, Treasures) :-
    connects(R1, R2), room_danger(R1, Danger),
    Treasures = #count { T : treasure_in(T, R1) }.

% Show isolated rooms (should be empty)
connectivity_isolated_rooms(R) :- room(R), not reachable(R).

% Show balance analysis
balance_total_danger(Total) :- Total = #sum { D : room_danger(_, D) }.
balance_treasure_distribution(Rarity, Count) :-
    treasure_rarity(_, Rarity), Count = #count { T : treasure_in(T, _), treasure_rarity(T, Rarity) }.

% Difficulty rating based on average danger
% Calculate total danger first
total_danger_sum(Total) :- Total = #sum { D : room_danger(_, D) }.

% Determine difficulty rating based on total danger
% Easy: total < 21, Balanced: 21-42, Hard: 42-56, Extreme: >= 56
balance_difficulty_progression(easy) :- total_danger_sum(Total), Total < 21.
balance_difficulty_progression(balanced) :- total_danger_sum(Total), Total >= 21, Total < 42.
balance_difficulty_progression(hard) :- total_danger_sum(Total), Total >= 42, Total < 56.
balance_difficulty_progression(extreme) :- total_danger_sum(Total), Total >= 56.

% ===== SHOW DIRECTIVES =====
#show room_layout/6.
#show connectivity_paths/4.
#show connectivity_isolated_rooms/1.
#show balance_total_danger/1.
#show balance_treasure_distribution/2.
#show balance_difficulty_progression/1.