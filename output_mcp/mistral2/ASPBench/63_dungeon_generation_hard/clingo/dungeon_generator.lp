% --- DOMAIN DECLARATIONS ---
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

% Connections
connection(entrance, hallway, unlocked, none).
connection(hallway, barracks, unlocked, none).
connection(barracks, secret_closet, unlocked, none).
connection(hallway, mess_hall, unlocked, none).
connection(mess_hall, kitchen, unlocked, none).
connection(mess_hall, treasury, locked, iron_key).
connection(treasury, boss_antechamber, locked, gold_key).
connection(boss_antechamber, boss_lair, unlocked, none).

% Items
item(iron_key, key).
item(gold_key, key).
item(trap_kit, tool).

% Treasures
treasure(silver_locket, 100).
treasure(jeweled_crown, 500).
treasure(dragon_hoard, 1000).

% Monsters
monster(goblin, 2).
monster(orc, 5).
monster(troll, 10).
monster(dragon, 15).

% Traps
trap(spike_trap, 3, trap_kit).

% Room types
entrance(entrance).
boss_room(boss_lair).
secret_room(secret_closet).

% --- CHOICE RULES FOR PLACEMENT ---
% Items can be placed in any room
{ item_in_room(Room, Item) : room(Room, _) } :- item(Item, _).

% Treasures can be placed in any room
{ treasure_in_room(Room, Treasure) : room(Room, _), treasure(Treasure, _) }.

% Monsters can be placed in any room (with count >= 0)
{ monster_in_room(Room, Monster, Count) : monster(Monster, _), room(Room, _) } 1 :- room(Room, _).

% Traps can be placed in any room (active or not)
{ trap_in_room(Room, Trap, Active) : trap(Trap, _, _), room(Room, _) } 1 :- room(Room, _).

% --- HELPER PREDICATES ---
% Reachability with key constraints
reachable(entrance) :- entrance(entrance).

% Reachability without locked doors
reachable(Room2) :-
    reachable(Room1),
    connection(Room1, Room2, unlocked, _).

% Reachability with keys
reachable(Room2) :-
    reachable(Room1),
    connection(Room1, Room2, locked, Key),
    has_key(Key).

% Has key if item is in a reachable room
has_key(Key) :-
    item_in_room(Room, Key),
    reachable(Room).

% Danger calculation per room
monster_danger(Room, TotalDanger) :-
    room(Room, _),
    TotalDanger = #sum { D*C : monster_in_room(Room, M, C), monster(M, D) }.

trap_danger(Room, TotalDanger) :-
    room(Room, _),
    TotalDanger = #sum { D : trap_in_room(Room, T, true), trap(T, D, _) }.

room_danger(Room, Total) :-
    room(Room, _),
    monster_danger(Room, MD),
    trap_danger(Room, TD),
    Total = MD + TD.

% --- CONSTRAINTS ---
% Danger level per room must not exceed 15
:- room(Room, _), room_danger(Room, Danger), Danger > 15.

% Traps are active unless their disarm_tool is present in the same room
trap_in_room(Room, Trap, false) :-
    trap_in_room(Room, Trap, _),
    item_in_room(Room, Tool),
    trap(Trap, _, Tool).

% Secret rooms must connect to exactly one non-secret room that is reachable
:- secret_room(Room),
   #count { R2 : connection(Room, R2, _, _), not secret_room(R2), reachable(R2) } != 1.

% Boss monster (highest danger level) must be in the boss room
:- not monster_in_room(boss_lair, dragon, _).

% Path from entrance to boss_lair must exist
path(entrance, hallway) :- connection(entrance, hallway, _, _).
path(Room1, Room2) :-
    path(Room1, Room3),
    connection(Room3, Room2, _, _),
    reachable(Room2).

:- not path(entrance, boss_lair).

% --- SOLUTION ANALYSIS ---
% Calculate total danger
total_danger(Total) :-
    Total = #sum { D : room(R, _), room_danger(R, D) }.

% Difficulty progression score (simplified as difference between max and min danger)
max_danger(Max) :- Max = #max { D : room(R, _), room_danger(R, D) }.
min_danger(Min) :- Min = #min { D : room(R, _), room_danger(R, D) }.
difficulty_progression_score(Score) :-
    max_danger(Max),
    min_danger(Min),
    Score = Max - Min.

% Key acquisition order
key_acquisition(Key, FoundIn, Unlocks) :-
    item_in_room(FoundIn, Key),
    connection(_, Unlocks, locked, Key).

% Main path from entrance to boss_lair
main_path(Room1, Room2) :- path(Room1, Room2).

% Solvable if path exists and all constraints are satisfied
solvable :- path(entrance, boss_lair).

% --- SHOW DIRECTIVES ---
#show item_in_room/2.
#show treasure_in_room/2.
#show monster_in_room/3.
#show trap_in_room/3.
#show room_danger/2.
#show total_danger/1.
#show difficulty_progression_score/1.
#show solvable/0.
#show main_path/2.
#show key_acquisition/3.