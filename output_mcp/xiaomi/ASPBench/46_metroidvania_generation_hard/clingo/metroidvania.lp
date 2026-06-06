% ============================================================
% Metroidvania Game World Design - ASP Model
% ============================================================

% ---- Domain Definitions ----
room(start).
room(r1). room(r2). room(r3). room(r4). room(r5).
room(r6). room(r7). room(r8). room(r9). room(r10).
room(goal).

% Rooms that can have items and special types
item_room(r1). item_room(r2). item_room(r3). item_room(r4). item_room(r5).
item_room(r6). item_room(r7). item_room(r8). item_room(r9). item_room(r10).

% Items
key(redkey). key(bluekey). key(greenkey). key(yellowkey).
equipment(boots). equipment(grapple).
item(X) :- key(X).
item(X) :- equipment(X).

% Special room types
special_type(flooded). special_type(chasm).

% ---- Special Room Type Assignment ----
% Exactly one room of each special type in R1-R10
1 { special_room(R, flooded) : item_room(R) } 1.
1 { special_room(R, chasm) : item_room(R) } 1.
% Each room can have at most one special type
:- special_room(R, flooded), special_room(R, chasm).

% ---- Item Placement ----
% Each item placed in exactly one room R1-R10
1 { item_at(I, R) : item_room(R) } 1 :- item(I).
% Each room has at most 2 items (to keep it reasonable)
{ item_at(I, R) : item(I) } 2 :- item_room(R).

% ---- Constraint 3: Equipment cannot be in the room type it enables ----
:- item_at(boots, R), special_room(R, flooded).
:- item_at(grapple, R), special_room(R, chasm).

% ---- Constraint 4: YellowKey must be in Chasm room ----
:- item_at(yellowkey, R), not special_room(R, chasm).
:- special_room(R, chasm), not item_at(yellowkey, R).

% ---- Connection Structure ----
% Define potential edges (excluding start->start, goal->goal, etc.)
potential_edge(R1, R2) :- room(R1), room(R2), R1 != R2, R1 != goal, R2 != start.

% Select bidirectional connections (pairs)
% We need 10-15 bidirectional connections
{ bidir(R1, R2) } :- potential_edge(R1, R2), R1 < R2, R1 != goal, R2 != start.

% Count bidirectional connections
bidir_count(N) :- N = #count { R1, R2 : bidir(R1, R2) }.
:- bidir_count(N), N < 10.
:- bidir_count(N), N > 15.

% Generate edges from bidirectional connections
edge(R1, R2) :- bidir(R1, R2).
edge(R2, R1) :- bidir(R1, R2).

% One-way connections (2 total: one general + one to goal)
% One-way to goal
1 { oneway_to_goal(R) : room(R), R != goal } 1.
edge(R, goal) :- oneway_to_goal(R).

% One general one-way connection (not involving goal)
1 { oneway(R1, R2) : potential_edge(R1, R2), R1 != goal, R2 != goal, R1 != R2 } 1.
edge(R1, R2) :- oneway(R1, R2).

% Goal has exactly one incoming (already from oneway_to_goal) and no outgoing
:- edge(goal, _).

% ---- Key Requirements on Edges ----
% Each edge may require a key or be free
{ requires(R1, R2, K) : key(K) } 1 :- edge(R1, R2).
% If no key is specified, it's free (null)
free(R1, R2) :- edge(R1, R2), not requires(R1, R2, _).

% Constraint 2: For bidirectional pairs, if one direction requires a key,
% the return must have at least one keyless path
:- bidir(R1, R2), requires(R1, R2, _), not free(R2, R1).
:- bidir(R1, R2), requires(R2, R1, _), not free(R1, R2).

% ---- Reachability and Progression ----
% Define time steps for exploration
time(0..20).

% Player starts at start at time 0
at(start, 0).

% Movement: player can move along free edges if they have required keys
% and equipment for special rooms
can_enter(R2, T+1) :- at(R1, T), edge(R1, R2), free(R1, R2), 
                       not special_room(R2, flooded), not special_room(R2, chasm),
                       time(T+1).
can_enter(R2, T+1) :- at(R1, T), edge(R1, R2), free(R1, R2),
                       special_room(R2, flooded), has(boots, T),
                       time(T+1).
can_enter(R2, T+1) :- at(R1, T), edge(R1, R2), free(R1, R2),
                       special_room(R2, chasm), has(grapple, T),
                       time(T+1).

% Movement through key-locked doors
can_enter(R2, T+1) :- at(R1, T), edge(R1, R2), requires(R1, R2, K), has(K, T),
                       not special_room(R2, flooded), not special_room(R2, chasm),
                       time(T+1).
can_enter(R2, T+1) :- at(R1, T), edge(R1, R2), requires(R1, R2, K), has(K, T),
                       special_room(R2, flooded), has(boots, T),
                       time(T+1).
can_enter(R2, T+1) :- at(R1, T), edge(R1, R2), requires(R1, R2, K), has(K, T),
                       special_room(R2, chasm), has(grapple, T),
                       time(T+1).

% Player can be at a room if they can enter it
{ at(R, T) } :- can_enter(R, T).

% Pick up items when entering a room
has(I, T+1) :- at(R, T+1), item_at(I, R), time(T+1).
% Items persist
has(I, T+1) :- has(I, T), time(T+1).

% ---- Reachability Constraints ----
% All rooms must be reachable
reachable(R) :- at(R, _).
:- room(R), not reachable(R).

% Goal must be reachable
:- not reachable(goal).

% Goal must be the LAST new room reached
% Define first time each room is reached
first_reached(R, T) :- at(R, T), not at(R, T-1), time(T).
first_reached(R, 0) :- at(R, 0).

% Goal's first reached time must be after all other rooms
:- first_reached(goal, Tg), first_reached(R, Tr), R != goal, Tr >= Tg.

% ---- Output ----
#show special_room/2.
#show item_at/2.
#show edge/2.
#show requires/3.
#show free/2.
#show bidir/2.
#show oneway/2.
#show oneway_to_goal/1.