% ===================== DOMAIN DATA =====================

% Rooms
room(room1). room(room2). room(room3). room(room4).
room(room5). room(room6). room(room7).

room_type(room1, entrance). room_type(room2, chamber). room_type(room3, corridor).
room_type(room4, chamber). room_type(room5, treasury). room_type(room6, corridor).
room_type(room7, boss_room).

room_size(room1, small). room_size(room2, large). room_size(room3, small).
room_size(room4, medium). room_size(room5, medium). room_size(room6, small).
room_size(room7, large).

% Connectivity (bidirectional)
connects(room1, room2). connects(room2, room1).
connects(room1, room3). connects(room3, room1).
connects(room2, room4). connects(room4, room2).
connects(room3, room5). connects(room5, room3).
connects(room4, room6). connects(room6, room4).
connects(room5, room6). connects(room6, room5).
connects(room5, room7). connects(room7, room5).

% Treasures
treasure(treasure1). treasure(treasure2). treasure(treasure3).
treasure_value(treasure1, 100). treasure_value(treasure2, 500). treasure_value(treasure3, 1000).
treasure_rarity(treasure1, common). treasure_rarity(treasure2, rare). treasure_rarity(treasure3, legendary).

% Monster types
monster(goblin). monster(orc). monster(dragon).
monster_danger(goblin, 2). monster_danger(orc, 4). monster_danger(dragon, 8).
monster_group_size(goblin, 3). monster_group_size(orc, 2). monster_group_size(dragon, 1).

% Entrance and exit
entrance(room1).
exit_room(room7).

% ===================== CHOICE RULES (Open Relations) =====================

% Each treasure placed in exactly one room
1 { treasure_in(T, R) : room(R) } 1 :- treasure(T).

% Monster placement: number of each monster type per room (0 to group_size)
{ monsters_in(R, M, N) } :- room(R), monster(M), N = 1..GS, monster_group_size(M, GS).

% ===================== DERIVED PREDICATES =====================

% Danger per room from monsters
room_danger(R, D) :- room(R), D = #sum { N*DL, R, M : monsters_in(R, M, N), monster_danger(M, DL) }.

% ===================== CONSTRAINTS =====================

% Constraint 1: Danger limit per room must not exceed 10
:- room_danger(R, D), D > 10.

% Constraint 2: All rooms reachable from entrance via BFS
reachable(R) :- entrance(R).
reachable(R2) :- reachable(R1), connects(R1, R2).

:- room(R), not reachable(R).

% Constraint 3: Strategic placement - rare/legendary treasures in higher-danger rooms than common
% For each pair of treasures where one is rarer, the rarer one must be in a room with >= danger
rarity_rank(common, 1).
rarity_rank(rare, 2).
rarity_rank(legendary, 3).

% If treasure T1 has lower rarity than T2, then room of T2 must have danger >= room of T1
:- treasure(T1), treasure(T2), treasure_rarity(T1, R1), treasure_rarity(T2, R2),
   rarity_rank(R1, RK1), rarity_rank(R2, RK2), RK1 < RK2,
   treasure_in(T1, Rm1), treasure_in(T2, Rm2),
   room_danger(Rm1, D1), room_danger(Rm2, D2), D2 < D1.

% Constraint 4: Minimum 1 treasure per path from entrance to exit
% We define paths as sequences of rooms from entrance to exit
% Use reachability to check: every simple path from entrance to exit must have >= 1 treasure

% Define path rooms: a room is on SOME path if it's reachable and can reach the exit
can_reach_exit(R) :- exit_room(R).
can_reach_exit(R1) :- can_reach_exit(R2), connects(R1, R2).

on_some_path(R) :- reachable(R), can_reach_exit(R).

% Count treasures on rooms that are on some path
path_treasure_count(N) :- N = #count { R : on_some_path(R), treasure_in(_, R) }.
:- path_treasure_count(N), N < 1.

% ===================== OUTPUT / SHOW =====================

% Room layout: which monsters and treasures in each room
#show monsters_in/3.
#show treasure_in/2.
#show room_danger/2.
#show room/1.
#show room_type/2.
#show room_size/2.
#show treasure/1.
#show treasure_value/2.
#show treasure_rarity/2.
#show monster/1.
#show monster_danger/2.
#show connects/2.
#show entrance/1.
#show exit_room/1.
#show reachable/1.
#show on_some_path/1.
#show path_treasure_count/1.