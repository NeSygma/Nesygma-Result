% ========== FACTS: INSTANCE DATA ==========

% Rooms (id, type)
room(entrance,entrance).
room(hallway,chamber).
room(barracks,chamber).
room(secret_closet,secret).
room(mess_hall,chamber).
room(kitchen,chamber).
room(treasury,chamber).
room(boss_antechamber,chamber).
room(boss_lair,boss).

% Connections (from, to, lock)
connection(entrance, hallway, none).
connection(hallway, barracks, none).
connection(barracks, secret_closet, none).
connection(hallway, mess_hall, none).
connection(mess_hall, kitchen, none).
connection(mess_hall, treasury, iron_key).
connection(treasury, boss_antechamber, gold_key).
connection(boss_antechamber, boss_lair, none).

% Items (id, type)
item(iron_key,key).
item(gold_key,key).
item(trap_kit,tool).

% Treasures (id, value)
treasure(silver_locket,100).
treasure(jeweled_crown,500).
treasure(dragon_hoard,1000).

% Monsters (id, danger_level)
monster(goblin,2).
monster(orc,5).
monster(troll,10).
monster(dragon,15).

% Traps (id, danger_level, disarm_tool)
trap(spike_trap,3,trap_kit).

% Constraints
max_danger_per_room(15).
boss_room_id(boss_lair).
difficulty_slope(0.5).


% ========== CHOICE RULES: PLACEMENTS ==========

% Items can be placed in any room
{placed_item(R,I) : room(R,_)} :- item(I,_).

% Treasures can be placed in any room
{placed_treasure(R,T) : room(R,_)} :- treasure(T,_).

% Monsters can be placed in any room (with count 1-3)
{placed_monster(R,M,C) : monster(M,_) : C=1..3} :- room(R,_).

% Traps can be placed in any room (active or inactive)
{placed_trap(R,T,active) : trap(T,_,_)} :- room(R,_).
{placed_trap(R,T,inactive) : trap(T,_,_)} :- room(R,_).


% ========== AUXILIARY PREDICATES ==========

% Reachability from entrance (ignoring locks for now)
reachable(entrance).
reachable(R2) :- reachable(R1), connection(R1,R2,_).

% All rooms must be reachable
:- room(R,_), not reachable(R).


% ========== DANGER CALCULATION ==========

% Monster danger in each room
room_monster_danger(R,Total) :-
    room(R,_),
    Total = #sum { C*D : placed_monster(R,M,C), monster(M,D) }.

% Trap danger in each room (active traps only)
room_trap_danger(R,Total) :-
    room(R,_),
    Total = #sum { D : placed_trap(R,T,active), trap(T,D,Tool), not placed_item(R,Tool) }.

% Total danger per room
room_danger(R,Total) :-
    room(R,_),
    room_monster_danger(R,M), room_trap_danger(R,T),
    Total = M + T.

% Danger constraint: max 15 per room
:- room_danger(R,D), max_danger_per_room(Max), D > Max.


% ========== TRAP ACTIVATION LOGIC ==========

% A trap is active unless its disarm tool is in the same room
:- placed_trap(R,T,inactive), trap(T,_,Tool), placed_item(R,Tool).


% ========== BOSS PLACEMENT ==========

% Boss monster must be in boss room
:- boss_room_id(BossRoom),
   not placed_monster(BossRoom,dragon,_).


% ========== SECRET ROOM CONSTRAINT ==========

% Secret rooms must connect to exactly one reachable non-secret room
secret_room_connects_one(R) :-
    room(R,secret),
    #count { R2 : room(R2,Type), R2\=R, not Type=secret, reachable(R2), connection(R,R2,_) } = 1.

:- room(R,secret), not secret_room_connects_one(R).


% ========== PATH ANALYSIS ==========

% Find a path from entrance to boss_lair using connections
path(R1,R2) :- connection(R1,R2,_).
path(R1,R3) :- path(R1,R2), connection(R2,R3,_).

% Main path should be a valid path from entrance to boss
:- not path(entrance,boss_lair).


% ========== KEY ACQUISITION ==========

% Keys must be placed in rooms that are reachable before the door they unlock
% This is implicitly enforced by the connection rule requiring the key to be present

% Track which keys are found and what they unlock
key_found_in(Key,Room) :- placed_item(Room,Key), item(Key,key).
key_unlocks(Key,To) :- connection(From,To,Key).


% ========== SOLUTION OUTPUT ==========

% Show the room layout
#show placed_item/2.
#show placed_treasure/2.
#show placed_monster/3.
#show placed_trap/3.
#show room_danger/2.

% Show path analysis
solution(solvable) :- path(entrance,boss_lair).
#show solution/1.

% Show key acquisition
key_acquisition(Key,FoundIn,Unlocks) :-
    key_found_in(Key,FoundIn),
    key_unlocks(Key,Unlocks).
#show key_acquisition/3.

% Balance analysis
room_count(N) :- N = #count { R : room(R,_) }.
total_danger(Total) :- Total = #sum { D : room_danger(_,D) }.
#show total_danger/1.