% --- Declarations ---
room(start).
room(goal).
room(r1). room(r2). room(r3). room(r4). room(r5).
room(r6). room(r7). room(r8). room(r9). room(r10).

item(red_key). item(blue_key). item(green_key). item(yellow_key).
item(boots). item(grapple).

special_type(flooded). special_type(chasm).

% --- Special room types ---
% Assign exactly one room as flooded and one as chasm, distinct from each other and from start/goal.
{ special_room(R, T) : room(R), special_type(T) } 2.
:- special_room(R1, T1), special_room(R2, T2), R1 = R2, T1 != T2.
:- special_room(start, _).
:- special_room(goal, _).

% Helper predicates for special room types
has_special_type(R, T) :- special_room(R, T).
requires_boots(R) :- has_special_type(R, flooded).
requires_grapple(R) :- has_special_type(R, chasm).

% --- Item placement ---
% Place all 6 items in rooms r1-r10.
% Equipment items cannot be placed in rooms of the type they enable.
{ item_in_room(I, R) : room(R) } 1 :- item(I).

% Constraints for equipment placement
:- item_in_room(boots, R), requires_boots(R).
:- item_in_room(grapple, R), requires_grapple(R).

% Ensure all items are placed
:- item(I), not item_in_room(I, _).

% --- Connections ---
% Generate bidirectional connections between rooms (10-15 total).
% Each connection may require a key or be keyless (null).
% We will generate 10-15 bidirectional connections and then add exactly two one-way connections.

% Generate bidirectional connections (undirected edges)
{ connection(F, T, K) : room(T), K = null; K = red_key; K = blue_key; K = green_key; K = yellow_key } 1 :- room(F), F != goal, F != start, F < T.

% Ensure at least 10 and at most 15 bidirectional connections
:- 15 < #count{ F, T, K : connection(F, T, K) }.
:- #count{ F, T, K : connection(F, T, K) } < 10.

% Ensure no self-connections
:- connection(F, T, _), F = T.

% --- One-way connections ---
% Exactly two one-way connections: one to goal and one additional one-way edge.
{ one_way(F, T) : room(F), room(T), F != T } 2.

% Ensure one of the one-way connections is to goal
:- not one_way(_, goal).

% Ensure goal has no outgoing connections
:- one_way(goal, _).

% Ensure goal has exactly one incoming connection (either bidirectional or one-way)
:- #count{ F : connection(F, goal, _) } + #count{ F : one_way(F, goal) } != 1.

% --- Bidirectional connection constraints ---
% For any bidirectional connection (F, T, K) and (T, F, K2), if K != null, then K2 must be null.
:- connection(F, T, K), connection(T, F, K2), K != null, K2 != null.

% --- Reachability and progression ---
% All rooms must be reachable from start.
% Goal must be the last room reachable.

% Reachability via connections (including one-way)
reachable(R, 0) :- room(R), R = start.
reachable(R, T+1) :- reachable(F, T), (connection(F, R, _); one_way(F, R)), time(T).

% Time horizon for reachability
% A sufficiently large horizon to allow propagation through the graph.
time(0..20).

% Ensure all rooms are reachable
:- room(R), not reachable(R, _).

% --- Item prerequisites ---
% Yellow key must be in the chasm room.
:- item_in_room(yellow_key, R), not has_special_type(R, chasm).

% --- Solution validity ---
% For now, we will assume the solution is valid if all constraints are satisfied.

% --- Show directives ---
#show special_room/2.
#show item_in_room/2.
#show connection/3.
#show one_way/2.