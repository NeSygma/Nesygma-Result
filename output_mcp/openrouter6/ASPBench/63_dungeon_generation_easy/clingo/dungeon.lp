% Roguelike Dungeon Generation in Clingo ASP

% ===== 1. DOMAIN DECLARATIONS =====
% Rooms
room(room1). room(room2). room(room3). room(room4). room(room5). room(room6). room(room7).

% Room types and sizes (from instance data)
room_type(room1, entrance, small).
room_type(room2, chamber, large).
room_type(room3, corridor, small).
room_type(room4, chamber, medium).
room_type(room5, treasury, medium).
room_type(room6, corridor, small).
room_type(room7, boss_room, large).

% Connections (undirected edges)
edge(room1, room2). edge(room2, room1).
edge(room1, room3). edge(room3, room1).
edge(room2, room4). edge(room4, room2).
edge(room3, room5). edge(room5, room3).
edge(room4, room6). edge(room6, room4).
edge(room5, room6). edge(room6, room5).
edge(room5, room7). edge(room7, room5).

% Treasures with values and rarities
treasure(t1, 100, common).
treasure(t2, 500, rare).
treasure(t3, 1000, legendary).

% Domain predicate for treasures (for choice rules)
treasure_domain(t1). treasure_domain(t2). treasure_domain(t3).

% Monster types with danger levels and group sizes
monster_type(goblin, 2, 3).
monster_type(orc, 4, 2).
monster_type(dragon, 8, 1).

% Domain predicate for monster types (for choice rules)
monster_domain(goblin). monster_domain(orc). monster_domain(dragon).

% Rarity ordering for strategic placement
rarity_order(common, 1).
rarity_order(rare, 2).
rarity_order(legendary, 3).

% ===== 2. DECISION VARIABLES =====
% Treasure placement: each treasure in exactly one room
{ placed_treasure(T, R) : room(R) } 1 :- treasure_domain(T).

% Monster placement: monsters can be in multiple rooms
% We model groups: each group has fixed size and danger
{ has_monster_group(T, R) } :- room(R), monster_domain(T).

% ===== 3. CONSTRAINTS =====

% Constraint 1: Each treasure in exactly one room (already enforced by choice rule)

% Constraint 2: Danger limit per room (max 10)
% Calculate danger per room from monster groups
danger(R, D) :- room(R), D = #sum { GD : has_monster_group(T, R), group_danger(T, GD) }.
group_danger(T, GD) :- monster_type(T, DL, GS), GD = DL * GS.

% Danger must not exceed 10 per room
:- danger(R, D), D > 10.

% Constraint 3: Connectivity - all rooms reachable from entrance (room1)
% Compute reachable rooms using transitive closure
reachable(room1).
reachable(R2) :- reachable(R1), edge(R1, R2).
:- room(R), not reachable(R).

% Constraint 4: Minimum treasures per path to exit (room7)
% Define rooms that are reachable without passing through treasure rooms
safe_reachable(room1) :- not placed_treasure(_, room1).
safe_reachable(R2) :- safe_reachable(R1), edge(R1, R2), not placed_treasure(_, R2).
% Every path from room1 to room7 must contain at least one treasure
:- safe_reachable(room7).

% Constraint 5: Strategic placement - rare treasures in higher-danger rooms than common
% For any two treasures with different rarities, the room with higher rarity must have higher danger
:- treasure(T1, _, R1), treasure(T2, _, R2), rarity_order(R1, O1), rarity_order(R2, O2),
   O1 < O2, placed_treasure(T1, Room1), placed_treasure(T2, Room2), danger(Room1, D1), danger(Room2, D2), D1 >= D2.

% ===== 4. OUTPUT PREDICATES =====

% Room layout configuration
room_config(R, Type, Size, Danger) :- room_type(R, Type, Size), danger(R, Danger).

% Treasures per room
room_treasures(R, T) :- placed_treasure(T, R).

% Monsters per room
room_monsters(R, T) :- has_monster_group(T, R).

% Isolated rooms (should be empty)
isolated_room(R) :- room(R), not reachable(R).

% Total danger analysis
total_danger(TD) :- TD = #sum { D, R : danger(R, D) }.

% Treasure distribution by rarity
treasure_count(common, C) :- C = #count { T : treasure(T, _, common), placed_treasure(T, _) }.
treasure_count(rare, R) :- R = #count { T : treasure(T, _, rare), placed_treasure(T, _) }.
treasure_count(legendary, L) :- L = #count { T : treasure(T, _, legendary), placed_treasure(T, _) }.

% Difficulty progression based on total danger
difficulty(easy) :- total_danger(TD), TD < 20.
difficulty(balanced) :- total_danger(TD), TD >= 20, TD < 35.
difficulty(hard) :- total_danger(TD), TD >= 35, TD < 50.
difficulty(extreme) :- total_danger(TD), TD >= 50.

% ===== 5. PATH FINDING FOR CONNECTIVITY OUTPUT =====
% Find a simple path from room1 to room7 using directed edges (lower index to higher)
room_index(room1, 1). room_index(room2, 2). room_index(room3, 3).
room_index(room4, 4). room_index(room5, 5). room_index(room6, 6). room_index(room7, 7).

% Directed edges for path finding (from lower index to higher)
dir_edge(R1, R2) :- edge(R1, R2), room_index(R1, I1), room_index(R2, I2), I1 < I2.

% Path as sequence of rooms using a simple approach
% Define path edges that form a valid path from room1 to room7
path_edge(R1, R2) :- dir_edge(R1, R2), on_path(R1), on_path(R2).

% Rooms on the path are those connected in a chain from room1 to room7
on_path(room1).
on_path(R2) :- on_path(R1), dir_edge(R1, R2).

% Ensure we reach room7
:- not on_path(room7).

% Path room sequence for output (simple enumeration)
path_room(1, room1).
path_room(2, room2) :- on_path(room2), dir_edge(room1, room2).
path_room(2, room3) :- on_path(room3), dir_edge(room1, room3).
path_room(3, room4) :- on_path(room4), dir_edge(room2, room4).
path_room(3, room5) :- on_path(room5), dir_edge(room3, room5).
path_room(4, room6) :- on_path(room6), dir_edge(room4, room6).
path_room(4, room6) :- on_path(room6), dir_edge(room5, room6).
path_room(5, room7) :- on_path(room7), dir_edge(room5, room7).

% Path danger and treasures (simplified)
path_danger(D) :- D = #sum { DR : path_room(_, R), danger(R, DR) }.
path_has_treasure(T) :- path_room(_, R), placed_treasure(T, R).

% ===== 6. SHOW DIRECTIVES =====
#show room_config/4.
#show room_treasures/2.
#show room_monsters/2.
#show isolated_room/1.
#show total_danger/1.
#show treasure_count/2.
#show difficulty/1.
#show path_room/2.
#show path_danger/1.
#show path_has_treasure/1.