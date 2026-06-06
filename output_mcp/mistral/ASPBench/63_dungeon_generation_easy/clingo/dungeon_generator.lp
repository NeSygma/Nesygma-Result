%% ========== FACTS: ROOMS, CONNECTIONS, TREASURES, MONSTERS ==========

% Room definitions: room_id, type, size
room(room1, entrance, small).
room(room2, chamber, large).
room(room3, corridor, small).
room(room4, chamber, medium).
room(room5, treasury, medium).
room(room6, corridor, small).
room(room7, boss_room, large).

% Connections (undirected)
connects(room1, room2).
connects(room1, room3).
connects(room2, room4).
connects(room3, room5).
connects(room4, room6).
connects(room5, room6).
connects(room5, room7).

% Treasure definitions: treasure_id, value, rarity
% Rarity: common < rare < legendary
treasure(treasure1, 100, common).
treasure(treasure2, 500, rare).
treasure(treasure3, 1000, legendary).

% Monster definitions: monster_id, danger_level, group_size
monster(goblin, 2, 3).
monster(orc, 4, 2).
monster(dragon, 8, 1).


%% ========== CHOICE RULES: PLACEMENT DECISIONS ==========

% Place each treasure in exactly one room
1 { placed_treasure(T, R) : room(R, _, _) } 1 :- treasure(T, _, _).

% Place monsters in rooms, respecting group size limits
% A monster type can be placed multiple times in a room up to its group size
{ placed_monster(M, R, C) : C = 1..MaxC } :- 
    monster(M, _, MaxC),
    room(R, _, _).


%% ========== CALCULATIONS: DANGER, REACHABILITY, STRATEGIC PLACEMENT ==========

% Calculate total danger in each room
room_danger(R, Total) :-
    room(R, _, _),
    Total = #sum { Danger * Count : 
                   placed_monster(M, R, Count),
                   monster(M, Danger, _) }.

% Ensure danger per room does not exceed 10
:- room(R, _, _), room_danger(R, D), D > 10.

% Reachability from entrance (room1)
reachable(room1).
reachable(R2) :-
    reachable(R1),
    connects(R1, R2).

% All rooms must be reachable
:- room(R, _, _), not reachable(R).

% Strategic placement: rare treasures should be in higher-danger rooms than common treasures
% We need to ensure that for any rare treasure and common treasure placed, the rare one is in a room with >= danger of the common one's room
% To do this, we'll collect the danger levels of rooms with treasures and compare

% Get danger level of room containing a treasure
room_with_treasure(T, R) :- placed_treasure(T, R).
treasure_danger(T, D) :- room_with_treasure(T, R), room_danger(R, D).

% Count treasures by rarity in rooms
common_treasure_danger(D) :- treasure_danger(T, D), treasure(T, _, common).
rare_treasure_danger(D) :- treasure_danger(T, D), treasure(T, _, rare).
legendary_treasure_danger(D) :- treasure_danger(T, D), treasure(T, _, legendary).

% Strategic placement constraint: rare treasures should be in higher-danger rooms than common ones
% If there is a common treasure, all rare treasures should be in rooms with danger >= the common treasure's danger
% We'll enforce this by ensuring the minimum rare danger >= maximum common danger
% (This ensures all rare are at least as dangerous as all common)
:- common_treasure_danger(MinCommon), rare_treasure_danger(MaxRare), MaxRare < MinCommon.

% Similarly for legendary vs rare and legendary vs common
:- rare_treasure_danger(MinRare), legendary_treasure_danger(MaxLegend), MaxLegend < MinRare.
:- common_treasure_danger(MinCommon), legendary_treasure_danger(MaxLegend), MaxLegend < MinCommon.


%% ========== MINIMUM TREASURES PER PATH TO EXIT ==========
% We need to ensure that every path from entrance to exit (room7) has at least one treasure
% First, define all paths from room1 to room7
% We'll use a recursive definition of path
path(R1, R2) :- connects(R1, R2).
path(R1, R3) :- path(R1, R2), connects(R2, R3), R1 != R3.

% A path is valid if it goes from entrance to boss room
valid_path(P) :- path(room1, P), P = room7.

% For each valid path, check if it contains at least one treasure
% We need to define which rooms are on a path
room_on_path(R, P) :- path(room1, P), R = P.
room_on_path(R, P) :- path(room1, P), connects(R, R2), room_on_path(R2, P).

% A path has a treasure if any room on the path has a placed treasure
path_has_treasure(P) :- valid_path(P), room_on_path(R, P), placed_treasure(_, R).

% Enforce that every valid path has at least one treasure
:- valid_path(P), not path_has_treasure(P).


%% ========== SHOW DIRECTIVE: DISPLAY THE SOLUTION ==========
#show placed_treasure/2.
#show placed_monster/3.
#show room_danger/2.
#show reachable/1.

% Total danger across all rooms
total_danger(Total) :- Total = #sum { D : room_danger(_, D) }.

% Treasure distribution by rarity
% Ground Rarity by iterating over possible rarities
rarity(common).
rarity(rare).
rarity(legendary).

treasure_count(Rarity, Count) :-
    rarity(Rarity),
    Count = #count { T : treasure(T, _, Rarity), placed_treasure(T, _) }.

% Difficulty rating based on total danger and monster distribution
% Use separate rules for each case
difficulty_level(easy) :- total_danger(Total), Total < 20.
difficulty_level(balanced) :- total_danger(Total), Total >= 20, Total < 40.
difficulty_level(hard) :- total_danger(Total), Total >= 40, Total < 60.
difficulty_level(extreme) :- total_danger(Total), Total >= 60.

#show total_danger/1.
#show treasure_count/2.
#show difficulty_level/1.