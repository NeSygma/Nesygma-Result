% Metroidvania-style game world design
% Rooms: A, B, C, D, E, F, G, H
% Keys: key1, key2, key3
% Starting room: A

% Domain declarations (use quoted strings for uppercase names)
room("A"). room("B"). room("C"). room("D"). room("E"). room("F"). room("G"). room("H").
key(key1). key(key2). key(key3).

% Possible key requirements for connections
req(null). req(key1). req(key2). req(key3).

% Choice rule for connections: for each ordered pair of distinct rooms, decide if a connection exists and what key it requires.
{ connection(From, To, Req) : req(Req) } :- room(From), room(To), From != To.

% Item location: each key is placed in exactly one room.
{ item_location(K, R) : room(R) } 1 :- key(K).

% Ensure each key is in a distinct room.
:- item_location(K1, R), item_location(K2, R), K1 != K2.

% Constraint 1: All rooms must be reachable from A when all keys are available.
% Define reachable_all using transitive closure over all connections (ignoring key requirements).
reachable_all("A").
reachable_all(To) :- reachable_all(From), connection(From, To, _).
:- room(R), not reachable_all(R).

% Constraint 2: For each key K, the room containing K must be reachable without using edges that require K.
% For key1:
reachable_without_key1("A").
reachable_without_key1(To) :- reachable_without_key1(From), connection(From, To, Req), Req != key1.
:- item_location(key1, R), not reachable_without_key1(R).

% For key2:
reachable_without_key2("A").
reachable_without_key2(To) :- reachable_without_key2(From), connection(From, To, Req), Req != key2.
:- item_location(key2, R), not reachable_without_key2(R).

% For key3:
reachable_without_key3("A").
reachable_without_key3(To) :- reachable_without_key3(From), connection(From, To, Req), Req != key3.
:- item_location(key3, R), not reachable_without_key3(R).

% Optional: Ensure each room has at least one connection (incoming or outgoing) to avoid isolated rooms.
% But reachable_all already ensures connectivity.

% Optional: Ensure there is at least one connection from A (otherwise only A reachable).
% reachable_all ensures all rooms reachable, so there must be a path from A to each room.

% Output the connections and item locations.
#show connection/3.
#show item_location/2.