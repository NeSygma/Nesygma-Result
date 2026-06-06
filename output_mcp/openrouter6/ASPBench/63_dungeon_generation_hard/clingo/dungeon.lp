% Dungeon Generation Problem
% Instance Data
room(entrance). room(hallway). room(barracks). room(secret_closet).
room(mess_hall). room(kitchen). room(treasury). room(boss_antechamber). room(boss_lair).

type(entrance, entrance). type(hallway, chamber). type(barracks, chamber).
type(secret_closet, secret). type(mess_hall, chamber). type(kitchen, chamber).
type(treasury, chamber). type(boss_antechamber, chamber). type(boss_lair, boss).

connection(entrance, hallway, unlocked).
connection(hallway, barracks, unlocked).
connection(barracks, secret_closet, unlocked).
connection(hallway, mess_hall, unlocked).
connection(mess_hall, kitchen, unlocked).
connection(mess_hall, treasury, locked, iron_key).
connection(treasury, boss_antechamber, locked, gold_key).
connection(boss_antechamber, boss_lair, unlocked).

item(iron_key). item(gold_key). item(trap_kit).
treasure(silver_locket). treasure(jeweled_crown). treasure(dragon_hoard).
monster(goblin). monster(orc). monster(troll). monster(dragon).
trap(spike_trap).

danger(goblin, 2). danger(orc, 5). danger(troll, 10). danger(dragon, 15).
danger(spike_trap, 3).

treasure_value(silver_locket, 100). treasure_value(jeweled_crown, 500). treasure_value(dragon_hoard, 1000).

% Choice rules for placements
{ item_in_room(Item, Room) : room(Room) } 1 :- item(Item).
{ treasure_in_room(Treasure, Room) : room(Room) } 1 :- treasure(Treasure).
{ monster_in_room(Monster, Room) : room(Room) } 1 :- monster(Monster), Monster != dragon.
monster_in_room(dragon, boss_lair). % dragon fixed in boss room
{ trap_in_room(Trap, Room) : room(Room) } 1 :- trap(Trap).

% Active trap calculation
active_trap(Trap, Room) :- trap_in_room(Trap, Room), not item_in_room(trap_kit, Room).

% Danger per room calculation
monster_danger_room(R, MD) :- room(R), MD = #sum{ DM, M : monster_in_room(M, R), danger(M, DM) }.
trap_danger_room(R, TD) :- room(R), TD = #sum{ DT : active_trap(spike_trap, R), danger(spike_trap, DT) }.
danger_room(R, D) :- monster_danger_room(R, MD), trap_danger_room(R, TD), D = MD + TD.

% Constraint: All rooms must be reachable
reachable(entrance).
reachable(R2) :- reachable(R1), connection(R1, R2, unlocked).
reachable(R2) :- reachable(R1), connection(R1, R2, locked, Key), key_available(Key).
key_available(Key) :- item_in_room(Key, R), reachable(R).
:- room(R), not reachable(R).

% Constraint: Maximum danger per room <= 15
:- danger_room(R, D), D > 15.

% Traversable connections
traversable(R1, R2) :- connection(R1, R2, unlocked).
traversable(R1, R2) :- connection(R1, R2, locked, Key), key_available(Key).

% Distance to boss calculation (shortest path)
step(0..10).
path_length(boss_lair, 0).
path_length(R, D+1) :- step(D), path_length(R2, D), traversable(R, R2).
:- path_length(R, D1), path_length(R, D2), D2 < D1.  % Keep only minimal distance
distance_to_boss(R, D) :- path_length(R, D), not path_length(R, D-1).

% Next room on shortest path to boss
next(R1, R2) :- traversable(R1, R2), distance_to_boss(R1, D1), distance_to_boss(R2, D2), D2 = D1 - 1.

% Path order from entrance to boss
path_order(entrance, 0).
path_order(R, D+1) :- path_order(R1, D), next(R1, R).

% Key acquisition order
key_acquisition(Key, Room, Order, UnlocksFrom, UnlocksTo) :-
    item_in_room(Key, Room), path_order(Room, Order),
    unlocks(Key, UnlocksFrom, UnlocksTo).

unlocks(iron_key, mess_hall, treasury).
unlocks(gold_key, treasury, boss_antechamber).

% Balance analysis
total_danger(T) :- T = #sum{ D, R : danger_room(R, D) }.

% Difficulty progression score (0 = perfectly progressive)
% Compute expected danger as linear progression: D_entrance + 0.5 * Order
% Use integer arithmetic: multiply by 2
difficulty_progression_score(Score) :-
    Score = #sum{ (2*D - (2*D_entrance + Order)) * (2*D - (2*D_entrance + Order)) :
                 path_order(Room, Order), danger_room(Room, D), danger_room(entrance, D_entrance) }.

% Solvable flag
solvable(true) :- reachable(boss_lair).

% Output instance data
#show room_instance/2.
#show connection_instance/4.
#show item_instance/2.
#show treasure_instance/2.
#show monster_instance/2.
#show trap_instance/3.

room_instance(R, T) :- room(R), type(R, T).
connection_instance(F, T, L, K) :- connection(F, T, L, K).
item_instance(I, "key") :- item(I), I != trap_kit.
item_instance(trap_kit, "tool").
treasure_instance(T, V) :- treasure(T), treasure_value(T, V).
monster_instance(M, D) :- monster(M), danger(M, D).
trap_instance(spike_trap, 3, trap_kit).

% Output solution
#show monster_in_room/3.
#show treasure_in_room/2.
#show item_in_room/2.
#show trap_in_room/2.
#show danger_room/2.

% Output path analysis
#show solvable/1.
#show path_order/2.
#show key_acquisition/4.

% Output balance analysis
#show total_danger/1.
#show difficulty_progression_score/1.