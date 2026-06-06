% --- Instance Data ---
room(entrance, entrance).
room(hallway, chamber).
room(barracks, chamber).
room(secret_closet, secret).
room(mess_hall, chamber).
room(kitchen, chamber).
room(treasury, chamber).
room(boss_antechamber, chamber).
room(boss_lair, boss).

connection(entrance, hallway, none).
connection(hallway, barracks, none).
connection(barracks, secret_closet, none).
connection(hallway, mess_hall, none).
connection(mess_hall, kitchen, none).
connection(mess_hall, treasury, iron_key).
connection(treasury, boss_antechamber, gold_key).
connection(boss_antechamber, boss_lair, none).

item(iron_key, key).
item(gold_key, key).
item(trap_kit, tool).

treasure(silver_locket, 100).
treasure(jeweled_crown, 500).
treasure(dragon_hoard, 1000).

monster(goblin, 2).
monster(orc, 5).
monster(troll, 10).
monster(dragon, 15).

trap(spike_trap, 3, trap_kit).

% --- Placement ---
1 { placed_item(I, R) : room(R, _) } 1 :- item(I, _).
1 { placed_treasure(T, R) : room(R, _) } 1 :- treasure(T, _).
1 { placed_monster(M, 1, R) : room(R, _) } :- monster(M, _).
1 { placed_trap(T, R) : room(R, _) } 1 :- trap(T, _, _).

% --- Logic ---
:- not placed_monster(dragon, 1, boss_lair).

active_trap(T, R) :- placed_trap(T, R), not placed_item(trap_kit, R).

monster_danger(R, D) :- room(R, _), D = #sum { C*Danger, M : placed_monster(M, C, R), monster(M, Danger) }.
trap_danger(R, D) :- room(R, _), D = #sum { Danger, T : active_trap(T, R), trap(T, Danger, _) }.
danger(R, D) :- room(R, _), monster_danger(R, D1), trap_danger(R, D2), D = D1 + D2.

:- danger(R, D), D > 15.

% Reachability
% A room is reachable if there is a path from entrance.
% For locked doors, we need the key.
% Let's define reachability based on the set of keys held.
% Since there are only 2 keys, we can define reachability for each subset of keys.
% Subset of keys: {}, {iron}, {gold}, {iron, gold}
key_subset(none).
key_subset(iron).
key_subset(gold).
key_subset(both).

% Which keys are in which room?
key_in_room(iron_key, R) :- placed_item(iron_key, R).
key_in_room(gold_key, R) :- placed_item(gold_key, R).

% Reachable rooms given a set of keys
reachable(entrance, none).
reachable(To, S) :- reachable(From, S), connection(From, To, none).
reachable(To, iron) :- reachable(From, none), connection(From, To, iron_key).
reachable(To, iron) :- reachable(From, iron), connection(From, To, none).
reachable(To, both) :- reachable(From, iron), connection(From, To, gold_key).
reachable(To, both) :- reachable(From, both), connection(From, To, none).

% A room is reachable if it's reachable with any key set
is_reachable(R) :- reachable(R, _).

% Ensure all rooms are reachable
:- room(R, _), not is_reachable(R).

% Keys must be reachable before the doors they unlock
% Iron key must be reachable without iron key
:- placed_item(iron_key, R), not reachable(R, none).
% Gold key must be reachable with iron key (but not gold key)
:- placed_item(gold_key, R), not reachable(R, iron).

#show placed_item/2.
#show placed_treasure/2.
#show placed_monster/3.
#show placed_trap/2.
#show danger/2.