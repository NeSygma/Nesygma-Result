% Metroidvania Game World Layout Generation
% ==========================================

% --- Domain Definitions ---
room(a;b;c;d;e;f;g;h).
key("key1";"key2";"key3").

% --- Starting Room ---
start_room(a).

% --- Connection Choices ---
% For each pair of distinct rooms, at most one null connection (no key required)
0 { null_conn(R1,R2) } 1 :- room(R1), room(R2), R1 != R2.

% For each pair, at most one keyed connection (with one specific key)
0 { keyed_conn(R1,R2,K) : key(K) } 1 :- room(R1), room(R2), R1 != R2.

% Cannot have both null and keyed connection for the same pair
:- null_conn(R1,R2), keyed_conn(R1,R2,K).

% --- Key Placement ---
% Each key is in exactly one room
1 { key_location(K,R) : room(R) } 1 :- key(K).

% --- Reachability (Progressive Exploration) ---
% Start room is always reachable
reachable(a).

% Reachable via null connections (no key required)
reachable(R2) :- reachable(R1), null_conn(R1,R2).

% Reachable via keyed connections (must have the key first)
reachable(R2) :- reachable(R1), keyed_conn(R1,R2,K), have_key(K).

% Have a key if its location room is reachable
have_key(K) :- reachable(R), key_location(K,R).

% --- Constraints ---

% All rooms must be reachable
:- room(R), not reachable(R).

% Each key must be useful (required for at least one connection)
:- key(K), not keyed_conn(_,_,K).

% Keys should matter: not all rooms should be null-reachable
null_reachable(a).
null_reachable(R2) :- null_reachable(R1), null_conn(R1,R2).
:- #count { R : null_reachable(R) } = 8.

% --- Output in Problem Format ---
connection(R1,R2,"null") :- null_conn(R1,R2).
connection(R1,R2,K) :- keyed_conn(R1,R2,K).

#show connection/3.
#show key_location/2.