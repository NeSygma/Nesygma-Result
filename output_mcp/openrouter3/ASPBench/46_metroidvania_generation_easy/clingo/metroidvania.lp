% Metroidvania Game World Design
% Problem: Design a valid room layout with key placements

% ===== DOMAIN DECLARATIONS =====
room(a). room(b). room(c). room(d). room(e). room(f). room(g). room(h).
key(key1). key(key2). key(key3).
start_room(a).

% ===== CONNECTIONS =====
% We need to define possible connections between rooms
% Each connection can require a key or be free
% We'll use choice rules to explore different layouts

% Possible connections (undirected, but we'll make them directed)
% Allow connections between any two distinct rooms
{ connection(From, To, Req) : req(Req) } :- room(From), room(To), From != To.

% Define possible requirements (including null/no key)
req(null). req(key1). req(key2). req(key3).

% ===== KEY PLACEMENTS =====
% Each key must be placed in exactly one room
1 { item_location(K, R) : room(R) } 1 :- key(K).

% ===== REACHABILITY LOGIC =====
% Start room is always reachable
reachable(a).

% A room is reachable if there's a connection from a reachable room
% and the player has the required key (or no key required)
can_traverse(From, To) :- connection(From, To, null), reachable(From).
can_traverse(From, To) :- connection(From, To, K), reachable(From), has_key(K).

% A room becomes reachable if there's a traversable connection to it
reachable(To) :- can_traverse(From, To).

% ===== KEY COLLECTION LOGIC =====
% Player collects keys when they reach the room containing the key
has_key(K) :- item_location(K, R), reachable(R).

% ===== SOFT-LOCK PREVENTION =====
% A soft-lock occurs if a key is required to progress but is located
% in a room that can only be reached AFTER obtaining that key

% Helper: Check if a key is required to reach a specific room
key_required_for_room(K, R) :- connection(_, R, K).

% A key cannot be required to reach the room where it's located
:- item_location(K, R), key_required_for_room(K, R).

% More sophisticated soft-lock prevention:
% For each key, there must exist a path from start to the key's room
% that doesn't require that same key
:- key(K), item_location(K, R), not reachable_without_key(K, R).

% Define reachable without a specific key - fixed unsafe variables
% Base case: start room is always reachable without any key
reachable_without_key(K, a) :- key(K), start_room(a).

% Recursive case: can reach To from From without key K
reachable_without_key(K, To) :- 
    connection(From, To, null), 
    reachable_without_key(K, From).

reachable_without_key(K, To) :- 
    connection(From, To, K2), 
    K2 != K, 
    reachable_without_key(K, From).

% ===== VALIDITY CONSTRAINTS =====
% All rooms must be reachable
:- not reachable(R), room(R).

% ===== FINAL VALIDATION =====
% A layout is valid if all rooms are reachable and no soft-locks
valid_layout :- #count{R : reachable(R)} = 8.

% ===== OUTPUT =====
#show room/1.
#show key/1.
#show connection/3.
#show item_location/2.
#show reachable/1.
#show has_key/1.
#show valid_layout/0.