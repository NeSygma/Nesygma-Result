% ===== DOMAIN DEFINITIONS =====
room(a). room(b). room(c). room(d). room(e). room(f). room(g). room(h).
key(key1). key(key2). key(key3).

% Time steps for progressive exploration
time(0..15).

% ===== CHOICE RULES FOR DESIGN DECISIONS =====

% Each key must be placed in exactly one room
1 { key_location(K, R) : room(R) } 1 :- key(K).

% Connections: allow directed connections between any two different rooms
{ connection(R1, R2) } :- room(R1), room(R2), R1 != R2.

% Each connection either requires a key or doesn't
{ requires(R1, R2, K) : key(K) } 1 :- connection(R1, R2).
% Note: if no key is chosen, the connection is unkeyed

% ===== EXPLORATION SIMULATION =====

% Player starts in room A at time 0
reachable(a, 0).
has_key(K, 0) :- key_location(K, a).

% Player can move through unkeyed connections
reachable(R2, T+1) :- reachable(R1, T), connection(R1, R2), not requires(R1, R2, _), time(T+1).

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

% No self-connections
:- connection(R, R).

% Ensure meaningful connectivity: at least 7 connections for 8 rooms
:- #count { R1, R2 : connection(R1, R2) } < 7.

% Ensure keys are actually used (each key must be required by at least one connection)
:- key(K), not requires(_, _, K).

% ===== OUTPUT =====
#show connection/2.
#show requires/3.
#show key_location/2.