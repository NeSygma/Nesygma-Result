% --- DOMAIN FACTS ---

% Rooms
room(1..7).
entrance(1).
exit(7).

% Connections (undirected graph)
link(1,2). link(1,3).
link(2,4).
link(3,5).
link(4,6).
link(5,6). link(5,7).
connected(X,Y) :- link(X,Y).
connected(Y,X) :- link(X,Y).

% Treasures
treasure(t1; t2; t3).
treasure_val(t1,100). treasure_rarity(t1,common).
treasure_val(t2,500). treasure_rarity(t2,rare).
treasure_val(t3,1000). treasure_rarity(t3,legendary).

% Rarity ordering for strategic placement
rarity_rank(common,1). rarity_rank(rare,2). rarity_rank(legendary,3).

% Monster types
mtype(goblin; orc; dragon).
m_danger(goblin,2). m_max(goblin,3).
m_danger(orc,4). m_max(orc,2).
m_danger(dragon,8). m_max(dragon,1).

% --- CHOICE RULES ---

% Constraint 1: Each treasure in exactly one room
1 { in_room(T,R) : room(R) } 1 :- treasure(T).

% Constraint 2: Monster counts per room (0 to m_max)
% For each (monster type, room), choose count N where 0 <= N <= max
count_option(M,R,N) :- mtype(M), room(R), m_max(M,S), N = 0..S.
1 { mcount(M,R,N) : count_option(M,R,N) } 1 :- mtype(M), room(R).

% --- COMPUTED VALUES ---

% Total danger contributed by monsters in each room
room_danger(R, D) :- D = #sum{ V*N, M,N : mcount(M,R,N), m_danger(M,V) }, room(R).

% --- CONSTRAINTS ---

% Constraint 3: Danger limit per room (must not exceed 10)
:- room_danger(R, D), D > 10.

% Constraint 4: All rooms reachable from entrance
reachable(1).
reachable(R2) :- reachable(R1), connected(R1,R2), R1 != R2.
:- room(R), not reachable(R).

% Constraint 5: Strategic placement
% Rarer treasures must be in rooms with strictly higher danger than less rare treasures
:- treasure(T1), treasure(T2), T1 != T2,
   in_room(T1,R1), in_room(T2,R2),
   treasure_rarity(T1,Rar1), treasure_rarity(T2,Rar2),
   rarity_rank(Rar1,Rank1), rarity_rank(Rar2,Rank2),
   Rank1 > Rank2,
   room_danger(R1,D1), room_danger(R2,D2),
   D1 <= D2.

% Constraint 6: Minimum 1 treasure per path to exit
% A room with no treasure
no_treasure_room(R) :- room(R), not in_room(_, R).

% Rooms reachable from entrance using only rooms without treasures
nt_reachable(1) :- no_treasure_room(1).
nt_reachable(R2) :- nt_reachable(R1), connected(R1,R2), no_treasure_room(R2), R1 != R2.

% Exit must NOT be reachable without passing through a treasure room
:- nt_reachable(7).

% --- OUTPUT PREDICATES ---

% Room layout: which treasures are in each room
room_treasure(R, T) :- in_room(T,R).

% Room layout: which monsters are in each room (with count)
room_monsters(R, M, N) :- mcount(M,R,N), N > 0.

% Room layout: danger level per room
danger_level(R, D) :- room_danger(R,D).

% Connectivity: isolated rooms (should be empty)
isolated_room(R) :- room(R), not reachable(R).

% Balance analysis: total danger
total_danger(D) :- D = #sum{ D2, R : room_danger(R,D2) }.

% Balance analysis: treasure distribution by rarity
count_treasures_by_rarity(Rar, C) :- C = #count{ T : treasure_rarity(T,Rar) }, rarity_rank(Rar,_).

% Balance analysis: difficulty progression
% Compare average danger in early rooms (1-3) vs late rooms (5-7)
early_room(1;2;3).
late_room(5;6;7).
early_total_danger(D) :- D = #sum{ D2, R : room_danger(R,D2), early_room(R) }.
late_total_danger(D) :- D = #sum{ D2, R : room_danger(R,D2), late_room(R) }.

% Simple assessment based on danger difference
difficulty_progression(easy)      :- early_total_danger(D1), late_total_danger(D2), D2 <= D1.
difficulty_progression(balanced)  :- early_total_danger(D1), late_total_danger(D2), D2 > D1, D2 - D1 <= 6.
difficulty_progression(hard)      :- early_total_danger(D1), late_total_danger(D2), D2 > D1, D2 - D1 > 6, D2 - D1 <= 12.
difficulty_progression(extreme)   :- early_total_danger(D1), late_total_danger(D2), D2 - D1 > 12.

% Path from entrance to exit (find one valid simple path)
% Use step-by-step path construction
path_connected(1).
{ path_edge(X,Y) : connected(X,Y) } :- path_connected(X), X != 7.
path_connected(Y) :- path_edge(X,Y).
:- path_connected(X), path_edge(X,Y), path_edge(Y,X).
% No cycles
:- path_edge(X,Y), path_edge(X,Z), Y != Z.
% Must reach exit
:- not path_connected(7).

% Helper: rooms on the path
on_path(R) :- path_connected(R).

% Path danger total
path_danger(D) :- D = #sum{ D2, R : room_danger(R,D2), on_path(R) }.

% Path treasures
path_has_treasure(T) :- in_room(T,R), on_path(R).

% Show output
#show room_treasure/2.
#show room_monsters/3.
#show danger_level/2.
#show isolated_room/1.
#show total_danger/1.
#show count_treasures_by_rarity/2.
#show difficulty_progression/1.
#show on_path/1.
#show path_edge/2.
#show path_danger/1.
#show path_has_treasure/1.