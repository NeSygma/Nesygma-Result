%% ============================================================
%% DOMAIN DEFINITIONS
%% ============================================================

%% Rooms
room(entrance). room(hallway). room(barracks). room(secret_closet).
room(mess_hall). room(kitchen). room(treasury).
room(boss_antechamber). room(boss_lair).

%% Room types
rtype(entrance, entrance).
rtype(hallway, chamber).
rtype(barracks, chamber).
rtype(secret_closet, secret).
rtype(mess_hall, chamber).
rtype(kitchen, chamber).
rtype(treasury, chamber).
rtype(boss_antechamber, chamber).
rtype(boss_lair, boss).

%% Connections (directed as given)
conn(entrance, hallway, "none").
conn(hallway, barracks, "none").
conn(barracks, secret_closet, "none").
conn(hallway, mess_hall, "none").
conn(mess_hall, kitchen, "none").
conn(mess_hall, treasury, iron_key).
conn(treasury, boss_antechamber, gold_key).
conn(boss_antechamber, boss_lair, "none").

%% Undirected connections (can traverse both ways once unlocked)
connected(R1, R2, Key) :- conn(R1, R2, Key).
connected(R1, R2, Key) :- conn(R2, R1, Key).

%% Items
item(iron_key). item(gold_key). item(trap_kit).
itype(iron_key, key). itype(gold_key, key). itype(trap_kit, tool).

%% Treasures
treasure(silver_locket, 100).
treasure(jeweled_crown, 500).
treasure(dragon_hoard, 1000).

%% Monster types
mtype(goblin, 2).
mtype(orc, 5).
mtype(troll, 10).
mtype(dragon, 15).

%% Trap types
ttype(spike_trap, 3, trap_kit).

%% Constants
max_danger(15).

%% ============================================================
%% CHOICE: PLACEMENTS
%% ============================================================

%% Place each item in exactly one room
{ placed_in(Item, Room) : room(Room) } 1 :- item(Item).

%% Place each treasure in exactly one room
{ placed_in_treasure(Treasure, Room) : room(Room) } 1 :- treasure(Treasure, _).

%% Monster counts: each monster type in each room gets count 0..5
1 { mcount(Type, Room, C) : C = 0..5 } 1 :- room(Room), mtype(Type, _).

%% Traps: at most one spike trap per room
{ trap_present(Type, Room) } :- room(Room), ttype(Type, _, _).

%% Whether a trap is active: present and disarm tool not in same room
trap_active(Type, Room) :- trap_present(Type, Room), ttype(Type, _, Tool), 
    not placed_in(Tool, Room).

%% ============================================================
%% REACHABILITY (least fixpoint computation)
%% ============================================================

reachable(entrance).
reachable(R2) :- reachable(R1), connected(R1, R2, "none").
reachable(R2) :- reachable(R1), connected(R1, R2, Key), key_is_found(Key).
reachable(R1) :- reachable(R2), connected(R1, R2, "none").
reachable(R1) :- reachable(R2), connected(R1, R2, Key), key_is_found(Key).

%% A key is found if placed in a reachable room
key_is_found(Key) :- itype(Key, key), placed_in(Key, Room), reachable(Room).

%% ============================================================
%% DANGER CALCULATION
%% ============================================================

%% Danger from monsters in a room
danger_monsters(Room, D) :- 
    D = #sum { Danger*C : mcount(Type, Room, C), mtype(Type, Danger) },
    room(Room).

%% Danger from traps in a room
danger_traps(Room, D) :-
    D = #sum { Danger : trap_active(Type, Room), ttype(Type, Danger, _) },
    room(Room).

%% Total danger
total_danger(Room, D) :- 
    danger_monsters(Room, D1),
    danger_traps(Room, D2),
    D = D1 + D2,
    room(Room).

%% ============================================================
%% CONSTRAINTS
%% ============================================================

%% 1. All rooms must be reachable
:- room(R), not reachable(R).

%% 4. Secret rooms connect to exactly one non-secret reachable room
:- room(R), rtype(R, secret),
    NS = #count { R2 : connected(R, R2, _), not rtype(R2, secret), reachable(R2) },
    NS != 1.

%% 7. Max danger per room
:- total_danger(Room, D), max_danger(Max), D > Max.

%% 8. Boss monster (dragon, highest danger 15) must be in boss_lair
:- mcount(dragon, boss_lair, C), C < 1.

%% 9. Path must be solvable - ensured by all rooms being reachable

%% ============================================================
%% MAIN PATH AND DIFFICULTY PROGRESSION
%% ============================================================

%% The main path rooms in order (shortest path from entrance to boss_lair)
main_path_order(1, entrance).
main_path_order(2, hallway).
main_path_order(3, mess_hall).
main_path_order(4, treasury).
main_path_order(5, boss_antechamber).
main_path_order(6, boss_lair).

%% Danger at each main path position
main_path_danger(Pos, D) :- main_path_order(Pos, Room), total_danger(Room, D).

%% Difficulty progression: danger should be non-decreasing on main path
:- main_path_order(P1, R1), main_path_order(P2, R2), P1 < P2,
   total_danger(R1, D1), total_danger(R2, D2), D1 > D2.

%% ============================================================
%% OUTPUT
%% ============================================================

#show placed_in/2.
#show placed_in_treasure/2.
#show mcount/3.
#show trap_present/2.
#show trap_active/2.
#show total_danger/2.
#show reachable/1.
#show key_is_found/1.
#show main_path_danger/2.