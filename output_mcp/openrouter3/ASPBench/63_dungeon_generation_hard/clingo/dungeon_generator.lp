% Dungeon Generator - Roguelike Dungeon with Logical Progression

% ==================== INSTANCE DATA ====================
% Rooms
room(entrance, entrance).
room(hallway, chamber).
room(barracks, chamber).
room(secret_closet, secret).
room(mess_hall, chamber).
room(kitchen, chamber).
room(treasury, chamber).
room(boss_antechamber, chamber).
room(boss_lair, boss).

% Connections (directed)
connection(entrance, hallway, unlocked).
connection(hallway, barracks, unlocked).
connection(barracks, secret_closet, unlocked).
connection(hallway, mess_hall, unlocked).
connection(mess_hall, kitchen, unlocked).
connection(mess_hall, treasury, locked, iron_key).
connection(treasury, boss_antechamber, locked, gold_key).
connection(boss_antechamber, boss_lair, unlocked).

% Items
item(iron_key, key).
item(gold_key, key).
item(trap_kit, tool).

% Treasures
treasure(silver_locket, 100).
treasure(jeweled_crown, 500).
treasure(dragon_hoard, 1000).

% Monsters
monster_type(goblin, 2).
monster_type(orc, 5).
monster_type(troll, 10).
monster_type(dragon, 15).

% Traps
trap_type(spike_trap, 3, trap_kit).

% Constraints
max_danger(15).
boss_room(boss_lair).
difficulty_slope(0.5).

% ==================== DUNGEON LAYOUT ====================
% Define which rooms are reachable from entrance
reachable(entrance).
reachable(R) :- reachable(R1), connection(R1, R, _).

% All rooms must be reachable
:- not reachable(R), room(R, _).

% Secret room constraint: must connect to exactly one non-secret room that is reachable
secret_room(secret_closet).
secret_connection(R) :- connection(R, secret_closet, _), room(R, Type), Type != secret.
secret_connection(R) :- connection(secret_closet, R, _), room(R, Type), Type != secret.
:- secret_room(S), #count{R : secret_connection(R)} != 1.

% ==================== ITEM PLACEMENT ====================
% Keys must be placed in rooms reachable before the doors they unlock
% Iron key unlocks treasury, so must be in a room reachable before treasury
% Gold key unlocks boss_antechamber, so must be in a room reachable before boss_antechamber

% Define which rooms are reachable before a given room
reachable_before(R1, R2) :- reachable(R1), not reachable_after(R1, R2).
reachable_after(R1, R2) :- connection(R1, R2, _).
reachable_after(R1, R2) :- connection(R1, X, _), reachable_after(X, R2).

% Iron key placement: must be in a room reachable before treasury
valid_iron_key_room(R) :- room(R, _), reachable_before(R, treasury).

% Gold key placement: must be in a room reachable before boss_antechamber
valid_gold_key_room(R) :- room(R, _), reachable_before(R, boss_antechamber).

% Trap kit placement: can be anywhere
valid_trap_kit_room(R) :- room(R, _).

% Choice rules for item placement
{ placed_item(Item, Room) } :- item(Item, _), room(Room, _).

% Constraints on item placement
:- placed_item(iron_key, R), not valid_iron_key_room(R).
:- placed_item(gold_key, R), not valid_gold_key_room(R).
:- placed_item(trap_kit, R), not valid_trap_kit_room(R).

% Each item must be placed exactly once
1 { placed_item(Item, Room) : room(Room, _) } 1 :- item(Item, _).

% ==================== TREASURE PLACEMENT ====================
% Treasures can be placed in any room
{ placed_treasure(Treasure, Room) } :- treasure(Treasure, _), room(Room, _).

% Each treasure must be placed exactly once
1 { placed_treasure(Treasure, Room) : room(Room, _) } 1 :- treasure(Treasure, _).

% ==================== MONSTER PLACEMENT ====================
% Monsters can be placed in any room, but boss monster must be in boss_lair
% Danger level calculation: Sum of (monster_count × monster_danger) + (active_trap_danger)

% Monster count per room (0 or more)
{ monster_in_room(Type, Room, Count) } :- monster_type(Type, _), room(Room, _), Count = 0..10.

% Boss monster constraint: dragon must be in boss_lair
:- monster_in_room(dragon, R, C), C > 0, R != boss_lair.

% ==================== TRAP PLACEMENT ====================
% Traps can be placed in any room
{ trap_in_room(Trap, Room, Active) } :- trap_type(Trap, _, _), room(Room, _), Active = 0..1.

% Trap is active unless disarm_tool is present in the same room
% disarm_tool for spike_trap is trap_kit
trap_active(Trap, Room) :- trap_in_room(Trap, Room, 1).
trap_active(Trap, Room) :- trap_in_room(Trap, Room, 0), not placed_item(trap_kit, Room).

% ==================== DANGER CALCULATION ====================
% Calculate danger level for each room
% Danger = sum(monster_count × monster_danger) + sum(active_trap_danger)

% Monster danger contribution
monster_danger_contribution(Room, Danger) :-
    room(Room, _),
    Danger = #sum{ D, Type : monster_in_room(Type, Room, Count), monster_type(Type, D), D * Count }.

% Trap danger contribution (only if active)
trap_danger_contribution(Room, Danger) :-
    room(Room, _),
    Danger = #sum{ T, Type : trap_in_room(Type, Room, Active), trap_type(Type, T, _), trap_active(Type, Room), T }.

% Total danger per room
room_danger(Room, TotalDanger) :-
    room(Room, _),
    monster_danger_contribution(Room, MD),
    trap_danger_contribution(Room, TD),
    TotalDanger = MD + TD.

% Maximum danger constraint
:- room_danger(Room, Danger), max_danger(Max), Danger > Max.

% ==================== PATH SOLVABILITY ====================
% Define valid path from entrance to boss_lair
% A path is valid if we can traverse connections, acquiring keys as needed

% Player state: has key if placed in a room they can reach
has_key(Key) :- placed_item(Key, R), reachable(R).

% Can traverse connection if unlocked or if we have the key
can_traverse(R1, R2) :- connection(R1, R2, unlocked).
can_traverse(R1, R2) :- connection(R1, R2, locked, Key), has_key(Key).

% Define reachable rooms considering key constraints
reachable_with_keys(entrance).
reachable_with_keys(R) :- reachable_with_keys(R1), can_traverse(R1, R).

% Boss room must be reachable with keys
:- not reachable_with_keys(boss_lair).

% ==================== DIFFICULTY PROGRESSION ====================
% Difficulty should increase with progression (difficulty_slope: 0.5)
% We'll measure this by ordering rooms along the main path

% Define main path (simplified - just the direct connections)
main_path_room(entrance).
main_path_room(hallway).
main_path_room(mess_hall).
main_path_room(treasury).
main_path_room(boss_antechamber).
main_path_room(boss_lair).

% Difficulty progression score (simplified)
% For now, just ensure boss room has highest danger
:- room_danger(boss_lair, D), room_danger(R, D2), R != boss_lair, D < D2.

% ==================== OUTPUT GENERATION ====================
% Generate solution in required format

% Room layout - simplified representation
room_layout(Room, Monsters, Treasures, Items, Traps, Danger) :-
    room(Room, _),
    room_danger(Room, Danger),
    Monsters = [ (Type, Count) : monster_in_room(Type, Room, Count), Count > 0 ],
    Treasures = [ T : placed_treasure(T, Room) ],
    Items = [ I : placed_item(I, Room) ],
    Traps = [ (Type, Active) : trap_in_room(Type, Room, Active), Active > 0 ].

% Path analysis
solvable :- reachable_with_keys(boss_lair).

% Key acquisition order
key_acquisition_order(Key, FoundIn, Unlocks) :-
    placed_item(Key, FoundIn),
    connection(_, _, locked, Key),
    Unlocks = #min{ R : connection(_, R, locked, Key) }.

% Balance analysis
total_danger_sum(Sum) :- Sum = #sum{ D : room_danger(_, D) }.

% Difficulty progression score (simplified)
difficulty_progression_score(Score) :-
    room_danger(entrance, E),
    room_danger(boss_lair, B),
    Score = (B - E) / 5.

% ==================== SHOW DIRECTIVES ====================
#show room/2.
#show reachable/1.
#show placed_item/2.
#show placed_treasure/2.
#show monster_in_room/3.
#show trap_in_room/3.
#show room_danger/2.
#show reachable_with_keys/1.
#show solvable/0.
#show total_danger_sum/1.
#show difficulty_progression_score/1.