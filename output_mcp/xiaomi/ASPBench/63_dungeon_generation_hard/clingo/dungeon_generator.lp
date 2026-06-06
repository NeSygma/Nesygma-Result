% ============================================
% ROGUELIKE DUNGEON GENERATOR - ASP Model
% ============================================

% ---- ROOMS ----
room(entrance, entrance).
room(hallway, chamber).
room(barracks, chamber).
room(secret_closet, secret).
room(mess_hall, chamber).
room(kitchen, chamber).
room(treasury, chamber).
room(boss_antechamber, chamber).
room(boss_lair, boss).

% ---- CONNECTIONS ----
% connection(From, To, LockKey) - "none" means unlocked
connection(entrance, hallway, none).
connection(hallway, barracks, none).
connection(barracks, secret_closet, none).
connection(hallway, mess_hall, none).
connection(mess_hall, kitchen, none).
connection(mess_hall, treasury, iron_key).
connection(treasury, boss_antechamber, gold_key).
connection(boss_antechamber, boss_lair, none).

% ---- ITEMS ----
item(iron_key, key).
item(gold_key, key).
item(trap_kit, tool).

% ---- TREASURES ----
treasure(silver_locket, 100).
treasure(jeweled_crown, 500).
treasure(dragon_hoard, 1000).

% ---- MONSTERS ----
monster(goblin, 2).
monster(orc, 5).
monster(troll, 10).
monster(dragon, 15).

% ---- TRAPS ----
trap(spike_trap, 3).
disarm_tool(spike_trap, trap_kit).

% ---- CONSTRAINTS ----
max_danger(15).
boss_room(boss_lair).
difficulty_slope(0.5).

% ============================================
% PLACEMENT DECISIONS (Choice Rules)
% ============================================

% Place each item in exactly one room
1 { placed_item(Item, Room) : room(Room, _) } 1 :- item(Item, _).

% Place each treasure in exactly one room
1 { placed_treasure(Treasure, Room) : room(Room, _) } 1 :- treasure(Treasure, _).

% Place monsters in rooms (each monster type can appear in multiple rooms with counts 1-3)
{ placed_monster(MType, Room, Count) : Count = 1..3 } :- monster(MType, _), room(Room, _), Room != entrance.

% Place traps in rooms (each trap type can appear in multiple rooms)
{ placed_trap(TType, Room) } :- trap(TType, _), room(Room, _), Room != entrance.

% ============================================
% REACHABILITY ANALYSIS
% ============================================

% Entrance is always reachable
reachable(entrance).

% A room is reachable if there's a connection from a reachable room
% and the lock requirement is satisfied (key is found in a reachable room before)
reachable(To) :- 
    connection(From, To, none), 
    reachable(From).

reachable(To) :- 
    connection(From, To, Key), 
    Key != none,
    reachable(From),
    placed_item(Key, KeyRoom),
    reachable(KeyRoom).

% ============================================
% TRAP ACTIVITY
% ============================================

% A trap is active if its disarm tool is NOT in the same room
trap_active(TType, Room) :- 
    placed_trap(TType, Room),
    disarm_tool(TType, Tool),
    not placed_item(Tool, Room).

% A trap is inactive if its disarm tool IS in the same room
trap_inactive(TType, Room) :- 
    placed_trap(TType, Room),
    disarm_tool(TType, Tool),
    placed_item(Tool, Room).

% ============================================
% DANGER LEVEL CALCULATION
% ============================================

% Monster danger contribution per room
monster_danger(Room, D) :- 
    D = #sum { Danger*MCount : placed_monster(MType, Room, MCount), monster(MType, Danger) }.

% Active trap danger contribution per room
trap_danger(Room, D) :- 
    D = #sum { TDanger : placed_trap(TType, Room), trap(TType, TDanger), trap_active(TType, Room) }.

% Total danger level for a room
danger_level(Room, TotalDanger) :- 
    room(Room, _),
    monster_danger(Room, MD),
    trap_danger(Room, TD),
    TotalDanger = MD + TD.

% Rooms with no monsters or traps have 0 danger
danger_level(Room, 0) :- 
    room(Room, _),
    not monster_danger(Room, _),
    not trap_danger(Room, _).

% ============================================
% CONSTRAINTS
% ============================================

% All rooms must be reachable from entrance
:- room(Room, _), not reachable(Room).

% Maximum danger per room must not exceed 15
:- danger_level(Room, D), max_danger(MaxD), D > MaxD.

% Boss monster (dragon, highest danger) must be in boss room
:- not placed_monster(dragon, boss_lair, _).

% Dragon must appear exactly once in boss room
1 { placed_monster(dragon, boss_lair, Count) : Count = 1..1 } 1.

% Secret rooms must connect to exactly one non-secret room that is reachable
% Count connections TO secret rooms from non-secret reachable rooms
secret_connection_count(SecretRoom, N) :- 
    room(SecretRoom, secret),
    N = #count { From : connection(From, SecretRoom, _), room(From, Type), Type != secret, reachable(From) }.

:- room(SecretRoom, secret), secret_connection_count(SecretRoom, N), N != 1.

% Keys must be placed in rooms reachable BEFORE the doors they unlock
% This is already enforced by the reachability rules above

% Each item must be placed exactly once (already in choice rule)

% Each treasure must be placed exactly once (already in choice rule)

% ============================================
% DIFFICULTY PROGRESSION
% ============================================

% Assign progression order to rooms (based on shortest path from entrance)
% Using a simple BFS-like ordering
progression(entrance, 0).
progression(Room, P) :- 
    connection(From, Room, none),
    progression(From, PrevP),
    P = PrevP + 1.

progression(Room, P) :- 
    connection(From, Room, Key),
    Key != none,
    progression(From, PrevP),
    P = PrevP + 1.

% Calculate difficulty progression score
% Score = sum of (danger * progression) for all rooms
% Lower score means better progression (danger increases with progression)
progression_score(Score) :- 
    Score = #sum { Danger*P : danger_level(Room, Danger), progression(Room, P) }.

% ============================================
% PATH ANALYSIS
% ============================================

% Check if path from entrance to boss_lair exists
path_exists :- reachable(boss_lair).

% Build main path (simplified - rooms in order of progression)
main_path(Room, P) :- 
    reachable(Room),
    progression(Room, P),
    P > 0.

% Key acquisition order
key_order(Key, KeyRoom, UnlockRoom, P) :-
    placed_item(Key, KeyRoom),
    connection(_, UnlockRoom, Key),
    progression(KeyRoom, P).

% ============================================
% OUTPUT
% ============================================

#show room/2.
#show connection/3.
#show placed_item/2.
#show placed_treasure/2.
#show placed_monster/3.
#show placed_trap/2.
#show trap_active/2.
#show trap_inactive/2.
#show danger_level/2.
#show reachable/1.
#show path_exists/0.
#show progression/2.
#show progression_score/1.
#show main_path/2.
#show key_order/4.
#show monster_danger/2.
#show trap_danger/2.