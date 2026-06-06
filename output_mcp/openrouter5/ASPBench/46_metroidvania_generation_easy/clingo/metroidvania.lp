%% Metroidvania Game World Design
%% Find a valid room layout with connections and key placements

%% Domain definitions
room(a; b; c; d; e; f; g; h).
key(k1; k2; k3).
start_room(a).

%% Each key must be placed in exactly one room
{ placed_in(K, R) : room(R) } 1 :- key(K).

%% A room can have at most one key
:- placed_in(K1, R), placed_in(K2, R), K1 != K2.

%% Connections: directed edges between distinct rooms
%% conn(R1, R2, Req) where Req is null (no key) or a key name
{ conn(R1, R2, null) : room(R1), room(R2), R1 != R2 }.
{ conn(R1, R2, K) : room(R1), room(R2), key(K), R1 != R2 }.

%% A pair of rooms can have at most one connection in each direction
:- conn(R1, R2, Req1), conn(R1, R2, Req2), Req1 != Req2.

%% ===== EXPLORATION MODEL =====
%% Model the player's progressive exploration through time steps
step(0..7).

%% At each step, player is in exactly one room
1 { at(R, S) : room(R) } 1 :- step(S).

%% Start in room A
at(a, 0).
:- at(R, 0), R != a.

%% Keys held at each step
{ has(K, S) } :- key(K), step(S).

%% Initially no keys
:- has(K, 0), key(K).

%% Movement: can move from current room to connected room
%% if no key required, or if player has the required key
{ move(R1, R2, S) : room(R1), room(R2), R1 != R2, conn(R1, R2, null) } :- step(S), S < 7, at(R1, S).
{ move(R1, R2, S) : room(R1), room(R2), R1 != R2, conn(R1, R2, K), has(K, S) } :- step(S), S < 7, at(R1, S).

%% At most one move per step
:- { move(_, _, S) } > 1, step(S), S < 7.

%% Effect of movement: arrive at destination
at(R2, S+1) :- move(_, R2, S), step(S), S < 7.

%% Stay in place if no movement
at(R, S+1) :- at(R, S), not move(R, _, S), not move(_, R, S), step(S), S < 7.

%% Pick up keys: if at a room with a key, you get it at next step
has(K, S+1) :- placed_in(K, R), at(R, S), step(S), S < 7.

%% Keys persist
has(K, S+1) :- has(K, S), not placed_in(K, R), at(R, S), step(S), S < 7.
%% Actually simpler: keys persist always
has(K, S+1) :- has(K, S), step(S), S < 7.

%% All rooms must be visited at some step
:- room(R), not visited(R).
visited(R) :- at(R, S).

%% Soft-lock prevention: For any key K placed in room R,
%% the player must be able to reach R without already having K.
%% This means there exists a step S where player is at R
%% and does NOT have K at that step (they acquire it at S+1).
:- placed_in(K, R), not reachable_without_key(K, R).
reachable_without_key(K, R) :- placed_in(K, R), at(R, S), not has(K, S), has(K, S+1), step(S), S < 7.

%% Each room (except start) must have at least one incoming connection
:- room(R), R != a, not { conn(_, R, _) } 1.

%% Each room must be reachable from start via some path (ignoring keys for basic connectivity)
:- room(R), R != a, not path_from_start(R).
path_from_start(R) :- start_room(R).
path_from_start(R) :- path_from_start(R1), conn(R1, R, _).

%% At least 7 connections (to connect 8 rooms in a tree-like structure)
:- { conn(_, _, _) } < 7.

%% At most 14 connections (keep it reasonable)
:- { conn(_, _, _) } > 14.

%% Each room should have at least one connection (in or out)
:- room(R), not { conn(R, _, _) } 1, not { conn(_, R, _) } 1.

%% Show the solution
#show conn/3.
#show placed_in/2.
#show at/2.
#show has/2.