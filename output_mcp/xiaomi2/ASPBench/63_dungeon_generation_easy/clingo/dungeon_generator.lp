% ==========================================
% Roguelike Dungeon Generator in ASP
% ==========================================

% --- Room Facts ---
room(room1, entrance, small).
room(room2, chamber, large).
room(room3, corridor, small).
room(room4, chamber, medium).
room(room5, treasury, medium).
room(room6, corridor, small).
room(room7, boss_room, large).

% --- Connections (bidirectional) ---
connects(room1, room2).
connects(room1, room3).
connects(room2, room4).
connects(room3, room5).
connects(room4, room6).
connects(room5, room6).
connects(room5, room7).
connects(R2, R1) :- connects(R1, R2).

% --- Treasure Facts ---
treasure(treasure1, 100, common).
treasure(treasure2, 500, rare).
treasure(treasure3, 1000, legendary).

% --- Monster Facts ---
monster(goblin, 2, 3).
monster(orc, 4, 2).
monster(dragon, 8, 1).

% --- Rarity Ranking ---
rarity_rank(common, 1).
rarity_rank(rare, 2).
rarity_rank(legendary, 3).

% ==========================================
% Decision Variables (Choice Rules)
% ==========================================

% Each treasure placed in exactly one room
1 { place_treasure(T, R) : room(R, _, _) } 1 :- treasure(T, _, _).

% Monster placement: for each monster type and room, choose count 0..group_size
0 { place_monsters(M, R, N) : N = 1..GS } 1 :- monster(M, _, GS), room(R, _, _).

% ==========================================
% Derived Predicates
% ==========================================

% Danger per room from placed monsters
room_danger_from_monsters(R, D) :-
    room(R, _, _),
    D = #sum { DL*N, M : place_monsters(M, R, N), monster(M, DL, _) }.

% Track which rooms have any monsters
has_monsters(R) :- place_monsters(M, R, N).

% Total danger per room (0 if no monsters)
room_danger(R, D) :- room_danger_from_monsters(R, D).
room_danger(R, 0) :- room(R, _, _), not has_monsters(R).

% Total danger across all rooms
total_danger_sum(TD) :- TD = #sum { D, R : room_danger(R, D) }.

% Reachability from entrance (room1)
reachable(room1).
reachable(R2) :- reachable(R1), connects(R1, R2).

% Isolated rooms (should be empty for valid dungeon)
isolated(R) :- room(R, _, _), not reachable(R).

% --- Path Definitions (simple paths from entrance to exit room7) ---
path_name(p1).
path_name(p2).

% Path 1: room1 -> room2 -> room4 -> room6 -> room5 -> room7
on_path(p1, room1).
on_path(p1, room2).
on_path(p1, room4).
on_path(p1, room6).
on_path(p1, room5).
on_path(p1, room7).

% Path 2: room1 -> room3 -> room5 -> room7
on_path(p2, room1).
on_path(p2, room3).
on_path(p2, room5).
on_path(p2, room7).

% Path has at least one treasure
path_has_treasure(P) :- on_path(P, R), place_treasure(_, R).

% Path danger totals
path_danger(P, PD) :-
    path_name(P),
    PD = #sum { D, R : on_path(P, R), room_danger(R, D) }.

% Path treasure counts
path_treasure_count(P, TC) :-
    path_name(P),
    TC = #count { T, R : on_path(P, R), place_treasure(T, R) }.

% Treasure count by rarity
rarity_count(Rarity, C) :-
    rarity_rank(Rarity, _),
    C = #count { T : place_treasure(T, _), treasure(T, _, Rarity) }.

% Room layout summary
room_layout(R, Type, Size, D, TC, MC) :-
    room(R, Type, Size),
    room_danger(R, D),
    TC = #count { T : place_treasure(T, R) },
    MC = #count { M : place_monsters(M, R, _) }.

% ==========================================
% Constraints
% ==========================================

% C1: Danger limit per room (must not exceed 10)
:- room_danger(R, D), D > 10.

% C2: All rooms must be reachable from entrance
:- room(R, _, _), not reachable(R).

% C3: Minimum 1 treasure per path to exit
:- path_name(P), not path_has_treasure(P).

% C4: Strategic placement - higher rarity treasures in higher danger rooms
:- treasure(T1, _, Rarity1), treasure(T2, _, Rarity2),
   rarity_rank(Rarity1, RK1), rarity_rank(Rarity2, RK2),
   RK1 < RK2,
   place_treasure(T1, Room1), place_treasure(T2, Room2),
   room_danger(Room1, D1), room_danger(Room2, D2),
   D2 <= D1.

% ==========================================
% Optimization: prefer balanced monster distribution
% ==========================================

#maximize { 1, R : has_monsters(R) }.

% ==========================================
% Difficulty Rating
% ==========================================

difficulty(easy) :- total_danger_sum(TD), TD <= 20.
difficulty(balanced) :- total_danger_sum(TD), TD >= 21, TD <= 35.
difficulty(hard) :- total_danger_sum(TD), TD >= 36, TD <= 50.
difficulty(extreme) :- total_danger_sum(TD), TD >= 51.

% ==========================================
% Output Directives
% ==========================================

#show room_layout/6.
#show place_treasure/2.
#show place_monsters/3.
#show room_danger/2.
#show total_danger_sum/1.
#show rarity_count/2.
#show path_has_treasure/1.
#show path_danger/2.
#show path_treasure_count/2.
#show isolated/1.
#show difficulty/1.