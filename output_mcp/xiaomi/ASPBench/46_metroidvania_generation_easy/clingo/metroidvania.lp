% ===== DOMAIN DEFINITIONS =====
room(a). room(b). room(c). room(d). room(e). room(f). room(g). room(h).
key(key1). key(key2). key(key3).

% Time steps for progressive exploration (max 8 rooms + 3 keys = 11 steps)
time(0..15).

% ===== CHOICE RULES FOR DESIGN DECISIONS =====

% Each key must be placed in exactly one room
1 { key_location(K, R) : room(R) } 1 :- key(K).

% Connections: allow directed connections between any two different rooms
% Each connection may or may not require a key
{ connection(R1, R2) } :- room(R1), room(R2), R1 != R2.
{ requires(R1, R2, K) : key(K) } 1 :- connection(R1, R2).
% A connection can also have no key requirement (empty choice)

% A connection requires no key if it exists but has no key requirement
no_key_required(R1, R2) :- connection(R1, R2), not requires(R1, R2, _).

% ===== EXPLORATION SIMULATION =====

% Player starts in room A at time 0
reachable(a, 0).
has_key(K, 0) :- key_location(K, a).  % Pick up keys in starting room

% Player can move through unkeyed connections to reachable rooms
reachable(R2, T+1) :- reachable(R1, T), connection(R1, R2), no_key_required(R1, R2), time(T+1).

% Player can move through keyed connections if they have the key
reachable(R2, T+1) :- reachable(R1, T), connection(R1, R2), requires(R1, R2, K), has_key(K, T), time(T+1).

% Reachability persists
reachable(R, T+1) :- reachable(R, T), time(T+1).

% Player picks up keys when entering a room
has_key(K, T+1) :- reachable(R, T), key_location(K, R), time(T+1).
has_key(K, T+1) :- has_key(K, T), time(T+1).

% ===== CONSTRAINTS =====

% All rooms must be reachable at some time step
:- room(R), not reachable(R, _).

% Each key must be obtainable - there must exist a path to its location
% This is implicitly ensured by the reachability constraint above

% No self-connections
:- connection(R, R).

% Ensure meaningful connectivity: at least 7 connections for 8 rooms (spanning tree minimum)
:- #count { R1, R2 : connection(R1, R2) } < 7.

% Ensure keys are actually used (each key must be required by at least one connection)
:- key(K), not requires(_, _, K).

% Ensure no circular key dependencies: 
% A key cannot be required to reach the room where that same key is located
:- key_location(K, R), requires(R1, R2, K), reachable(R, T), not reachable(R, T-1).

% ===== OUTPUT =====
#show connection/2.
#show requires/3.
#show key_location/2.
#show no_key_required/2.