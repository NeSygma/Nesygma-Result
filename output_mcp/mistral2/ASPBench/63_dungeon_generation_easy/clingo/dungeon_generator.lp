% --- Fixed Data ---
% Room properties
room(room1; room2; room3; room4; room5; room6; room7).
type(room1, entrance, small).
type(room2, chamber, large).
type(room3, corridor, small).
type(room4, chamber, medium).
type(room5, treasury, medium).
type(room6, corridor, small).
type(room7, boss_room, large).

% Connections between rooms
connects(room1, room2).
connects(room2, room1).
connects(room1, room3).
connects(room3, room1).
connects(room2, room4).
connects(room4, room2).
connects(room3, room5).
connects(room5, room3).
connects(room4, room6).
connects(room6, room4).
connects(room5, room6).
connects(room6, room5).
connects(room5, room7).
connects(room7, room5).

% Entrance and boss room
entrance(room1).
boss_room(room7).

% Treasure properties
treasure(treasure1, 100, common).
treasure(treasure2, 500, rare).
treasure(treasure3, 1000, legendary).

% Monster types
monster_type(goblin, 2, 3).
monster_type(orc, 4, 2).
monster_type(dragon, 8, 1).

% --- Choice Rules ---
% Treasure placement: each treasure in exactly one room
{ placed_in(T, R) : room(R) } = 1 :- treasure(T, _, _).

% Monster placement: monsters can be placed in rooms
{ placed_in(M, R) : monster_type(M, _, _) } :- room(R).

% --- Constraints ---
% Danger limit: total danger per room <= 10
% Calculate danger for each room
danger(R, D) :- room(R), D = #sum { DL, GS : placed_in(M, R), monster_type(M, DL, GS) }.
:- danger(R, D), D > 10.

% Connectivity: all rooms reachable from entrance
reachable(R) :- entrance(R).
reachable(R2) :- reachable(R1), connects(R1, R2).
:- room(R), not reachable(R).

% Path from entrance to boss room
path(R1, R2) :- connects(R1, R2).
path(R1, R3) :- path(R1, R2), connects(R2, R3).
:- not path(room1, room7).

% Minimum treasures per path to exit
treasures_in_path(P, C) :- path(P, R), C = #count { T : placed_in(T, R), path(P, R) }.
:- treasures_in_path(room1, C), C < 1.

% Strategic placement: rare treasures in higher-danger rooms
rarer_than(T1, T2) :- treasure(T1, _, R1), treasure(T2, _, R2), R1 != R2, R1 < R2.
higher_danger_than(R1, R2) :- danger(R1, D1), danger(R2, D2), D1 > D2.
:- rarer_than(T1, T2), placed_in(T1, R1), placed_in(T2, R2), not higher_danger_than(R1, R2).

% --- Calculations ---
% Total danger
total_danger(D) :- D = #sum { D1 : danger(_, D1) }.

% Treasure count by rarity
treasure_count(R, C) :- treasure(_, _, R), C = #count { T : placed_in(T, _), treasure(T, _, R) }.

% Difficulty rating
difficulty(easy) :- total_danger(D), D <= 20.
difficulty(balanced) :- total_danger(D), D > 20, D <= 40.
difficulty(hard) :- total_danger(D), D > 40, D <= 60.
difficulty(extreme) :- total_danger(D), D > 60.

% --- Show Directives ---
#show placed_in/2.
#show danger/2.
#show total_danger/1.
#show treasure_count/2.
#show difficulty/1.
#show reachable/1.
#show path/2.