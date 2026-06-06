% --- Instance Data ---
room(room1; room2; room3; room4; room5; room6; room7).
adj(room1, room2). adj(room2, room1).
adj(room1, room3). adj(room3, room1).
adj(room2, room4). adj(room4, room2).
adj(room3, room5). adj(room5, room3).
adj(room4, room6). adj(room6, room4).
adj(room5, room6). adj(room6, room5).
adj(room5, room7). adj(room7, room5).

treasure(treasure1, 100, common).
treasure(treasure2, 500, rare).
treasure(treasure3, 1000, legendary).

monster(goblin, 2, 3).
monster(orc, 4, 2).
monster(dragon, 8, 1).

% --- Constraints ---

% 1. Treasure placement
{ place_treasure(T, R) : room(R) } = 1 :- treasure(T, _, _).

% 2. Monster placement
% Each room can have a count of each monster type
{ place_monster(M, R, C) : C = 0..Size } = 1 :- monster(M, _, Size), room(R).

% 3. Danger limit
danger(R, D) :- room(R), D = #sum { Danger*C, M : place_monster(M, R, C), monster(M, Danger, _) }.
:- danger(R, D), D > 10.

% 4. Connectivity
reachable(room1).
reachable(Y) :- reachable(X), adj(X, Y).
:- room(R), not reachable(R).

% 5. Strategic placement
% Rare treasures should be in higher-danger rooms than common treasures
:- place_treasure(T1, R1), place_treasure(T2, R2), 
   treasure(T1, _, rare), treasure(T2, _, common), 
   danger(R1, D1), danger(R2, D2), D1 <= D2.

% 6. Minimum 1 treasure per path to exit (room7)
% If we remove all rooms with treasures, room7 is not reachable from room1.
has_treasure(R) :- place_treasure(_, R).
reachable_no_treasure(room1) :- not has_treasure(room1).
reachable_no_treasure(Y) :- reachable_no_treasure(X), adj(X, Y), not has_treasure(Y).
:- reachable_no_treasure(room7).

% --- Output ---
#show place_treasure/2.
#show place_monster/3.
#show danger/2.