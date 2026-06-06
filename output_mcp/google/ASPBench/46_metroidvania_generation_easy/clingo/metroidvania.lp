% Rooms and Keys
room(a; b; c; d; e; f; g; h).
key(key1; key2; key3).
key_or_none(none).
key_or_none(K) :- key(K).

% Generate connections (at least 7 to ensure connectivity)
% We limit the number of connections to keep the graph simple
{ conn(U, V, K) : room(U), room(V), U != V, key_or_none(K) } = 10.

% Each key is in exactly one room
1 { key_loc(K, R) : room(R) } 1 :- key(K).
:- key_loc(K1, R), key_loc(K2, R), K1 != K2.

% Reachability without a specific key K
% A room R is reachable without key K if there is a path from A to R
% that does not use key K.
reachable_without(a, K) :- key(K).
reachable_without(V, K) :- reachable_without(U, K), conn(U, V, none), key(K).
reachable_without(V, K) :- reachable_without(U, K), conn(U, V, K2), K2 != K, has_key_without(K2, K), key(K).

has_key_without(K2, K) :- reachable_without(R, K), key_loc(K2, R), key(K).

% Constraint: No soft-locks
% If a connection requires key K, K must be obtainable without using K.
:- conn(U, V, K), K != none, not has_key_without(K, K).

% Global Reachability
% All rooms must be reachable from A using all keys
reachable(a).
reachable(V) :- reachable(U), conn(U, V, none).
reachable(V) :- reachable(U), conn(U, V, K), K != none, has_key(K).
has_key(K) :- reachable(R), key_loc(K, R).

:- room(R), not reachable(R).

% Progressive exploration: No circular dependencies
% A key K1 depends on K2 if K2 is needed to reach K1.
% This is implicitly handled by the soft-lock constraint.

#show conn/3.
#show key_loc/2.