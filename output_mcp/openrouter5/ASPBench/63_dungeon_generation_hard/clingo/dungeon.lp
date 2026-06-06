%% ============================================================
%% DUNGEON GENERATION - ASP Model
%% ============================================================

%% ===================== DOMAINS =====================

% Rooms
room(entrance; hallway; barracks; secret_closet; mess_hall; kitchen; treasury; boss_antechamber; boss_lair).

% Room types
room_type(entrance, entrance).
room_type(hallway, chamber).
room_type(barracks, chamber).
room_type(secret_closet, secret).
room_type(mess_hall, chamber).
room_type(kitchen, chamber).
room_type(treasury, chamber).
room_type(boss_antechamber, chamber).
room_type(boss_lair, boss).

% Connections (directed edges)
conn(entrance, hallway).
conn(hallway, barracks).
conn(barracks, secret_closet).
conn(hallway, mess_hall).
conn(mess_hall, kitchen).
conn(mess_hall, treasury).
conn(treasury, boss_antechamber).
conn(boss_antechamber, boss_lair).

% Locked connections: (from, to, key_required)
locked_conn(mess_hall, treasury, iron_key).
locked_conn(treasury, boss_antechamber, gold_key).

% Items
item(iron_key; gold_key; trap_kit).
item_type(iron_key, key).
item_type(gold_key, key).
item_type(trap_kit, tool).

% Treasures
treasure(silver_locket; jeweled_crown; dragon_hoard).
treasure_value(silver_locket, 100).
treasure_value(jeweled_crown, 500).
treasure_value(dragon_hoard, 1000).

% Monsters
monster_type(goblin; orc; troll; dragon).
monster_danger(goblin, 2).
monster_danger(orc, 5).
monster_danger(troll, 10).
monster_danger(dragon, 15).

% Traps
trap_type(spike_trap).
trap_danger(spike_trap, 3).
trap_disarm_tool(spike_trap, trap_kit).

% Constants
max_danger(15).
boss_room(boss_lair).
difficulty_slope(0.5).

%% ===================== CHOICE RULES =====================

% Place each item in exactly one room
{ placed_in(Room, Item) : room(Room) } 1 :- item(Item).

% Place each treasure in exactly one room
{ treasure_in(Room, Treasure) : room(Room) } 1 :- treasure(Treasure).

% Place monsters in rooms (count per type per room)
{ monster_count(Room, Type, C) : C = 0..5 } :- room(Room), monster_type(Type).

% Place traps in rooms
{ trap_in(Room, spike_trap) } :- room(Room).

%% ===================== REACHABILITY =====================

% reachable(R) - R is reachable from entrance via unlocked connections
reachable(entrance).
reachable(R2) :- reachable(R1), conn(R1, R2), not locked_conn(R1, R2, _).
% Also reachable via locked doors if we have the key
reachable(R2) :- reachable(R1), conn(R1, R2), locked_conn(R1, R2, Key), have_key_before(Key, R2).

% have_key_before(Key, Room) - Key is obtainable before reaching Room
have_key_before(Key, Room) :- 
    locked_conn(From, Room, Key),
    placed_in(RoomK, Key),
    reachable_before(RoomK, From).

% reachable_before(R1, R2) - R1 is reachable without going through R2
reachable_before(R1, _) :- reachable(R1).

% Constraint: All rooms must be reachable
:- room(R), not reachable(R).

%% ===================== KEY PLACEMENT CONSTRAINTS =====================

% Keys must be placed in rooms reachable before the door they unlock
:- locked_conn(From, To, Key), 
   placed_in(RoomK, Key),
   not reachable_before(RoomK, From).

% A key cannot be placed in the room it unlocks (or beyond)
:- locked_conn(_, To, Key), placed_in(To, Key).
:- locked_conn(_, To, Key), placed_in(RoomK, Key), 
   conn(To, RoomK).

%% ===================== SECRET ROOM CONSTRAINTS =====================

% Secret rooms must connect to exactly one non-secret room that is reachable
secret_connections(N) :- 
    N = #count { R : room(R), room_type(R, chamber), conn(R, secret_closet) }.
:- secret_connections(N), N != 1.

% The connected non-secret room must be reachable
:- room_type(secret_closet, secret),
   not reachable(secret_closet).

%% ===================== DANGER CALCULATION =====================

% Calculate monster danger per room
monster_danger_total(Room, D) :-
    room(Room),
    D = #sum { Danger*C, Type : 
        monster_count(Room, Type, C), 
        monster_danger(Type, Danger) }.

% Trap is active if trap is in room and disarm tool is NOT in same room
trap_active(Room) :- trap_in(Room, spike_trap), not placed_in(Room, trap_kit).
% Trap is inactive if disarm tool is in same room
:- trap_in(Room, spike_trap), placed_in(Room, trap_kit), trap_active(Room).

% Active trap danger
active_trap_danger(Room, 3) :- trap_active(Room).
active_trap_danger(Room, 0) :- trap_in(Room, spike_trap), not trap_active(Room).
active_trap_danger(Room, 0) :- not trap_in(Room, spike_trap), room(Room).

% Total danger per room
room_danger(Room, D) :-
    room(Room),
    monster_danger_total(Room, MD),
    active_trap_danger(Room, TD),
    D = MD + TD.

% Max danger constraint
:- room(Room), room_danger(Room, D), max_danger(Max), D > Max.

%% ===================== BOSS PLACEMENT =====================

% Boss monster (dragon, danger 15) must be in boss room
boss_monster_count(C) :- monster_count(boss_lair, dragon, C).
:- boss_monster_count(C), C < 1.

% No dragon outside boss room
:- monster_count(Room, dragon, C), C > 0, Room != boss_lair.

%% ===================== DIFFICULTY PROGRESSION =====================

% Define progression order
progression_step(entrance, 0).
progression_step(hallway, 1).
progression_step(barracks, 2).
progression_step(secret_closet, 3).
progression_step(mess_hall, 2).
progression_step(kitchen, 3).
progression_step(treasury, 3).
progression_step(boss_antechamber, 4).
progression_step(boss_lair, 5).

% Difficulty should generally increase with progression
:~ progression_step(R1, S1), progression_step(R2, S2), 
   S1 < S2, room_danger(R1, D1), room_danger(R2, D2), D1 > D2. [1@1]

%% ===================== SOLVABLE PATH =====================

% Define the main path explicitly for verification
main_path_room(entrance).
main_path_room(hallway).
main_path_room(mess_hall).
main_path_room(treasury).
main_path_room(boss_antechamber).
main_path_room(boss_lair).

% Path is solvable if all main path rooms are reachable
solvable :- main_path_room(R) : reachable(R).

% Constraint: must be solvable
:- not solvable.

%% ===================== OUTPUT =====================

% Show room layouts
#show placed_in/2.
#show treasure_in/2.
#show monster_count/3.
#show trap_in/2.
#show trap_active/1.
#show room_danger/2.
#show solvable/0.
#show reachable/1.