% Domains
room(a; b; c; d; e; f; g; h).
key(key1; key2; key3).

% Time steps (bounded exploration horizon)
time(0..20).

% Starting room
start(a).

% Choice: Which connections exist and what keys they require
% We allow connections to require a key or be free (requires null)
{ connection(From, To, Key) : key(Key) ; connection(From, To, null) } :- room(From), room(To), From != To.

% Choice: Where each key is located (exactly one room per key)
1 { item_location(Key, Room) : room(Room) } 1 :- key(Key).

% Player starts at room A at time 0
visited(Room, Time) :- start(Room), time(Time).

% Player entity (simplified as a single entity)
player(player).

% At each time step, if player is in a room, they can traverse connections
% from that room that they can legally traverse
can_traverse(From, To, Time) :-
    visited(From, Time),
    connection(From, To, Key),
    time(Time),
    (Key == null ; has_key(player, Key, Time)).

% When traversing, player moves to the new room at the next time step
visited(To, Time+1) :- can_traverse(From, To, Time), time(Time+1).

% When entering a room, collect all keys in that room
collected_key(Key, Time+1) :- 
    visited(Room, Time),
    item_location(Key, Room),
    time(Time+1),
    not collected_key(Key, Time).

% Player has a key if it was collected in any previous time step
has_key(player, Key, Time) :- 
    collected_key(Key, T),
    time(T),
    time(Time),
    T <= Time.

% All rooms must be visited by the end of the time horizon
:- room(Room), not visited(Room, 20).

% Soft-lock prevention: If a connection requires a key, that key must be 
% located in a room that is reachable before the connection can be used
:- connection(From, To, Key),
   key(Key),
   not has_key(player, Key, T),
   time(T),
   visited(To, T+1),
   not collected_key(Key, T).

% Ensure no self-connections (optional but reasonable)
:- connection(Room, Room, _).

% Show the solution: connections and item locations
#show connection/3.
#show item_location/2.
#show visited/2.