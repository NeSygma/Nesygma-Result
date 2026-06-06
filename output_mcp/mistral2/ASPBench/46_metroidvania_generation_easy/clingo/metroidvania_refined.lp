% --- Facts ---
room(a). room(b). room(c). room(d). room(e). room(f). room(g). room(h).
key(key1). key(key2). key(key3).
start(a).

% Item locations: key(k, r) means key k is in room r.
item_location(key1, b).
item_location(key2, c).
item_location(key3, d).

% Connections: connection(from, to, requires).
% requires is null if no key required.
connection(a, b, null).
connection(b, a, null).
connection(b, c, null).
connection(c, b, null).
connection(c, d, null).
connection(d, c, null).
connection(d, e, key1).
connection(e, d, key1).
connection(e, f, null).
connection(f, e, null).
connection(f, g, key2).
connection(g, f, key2).
connection(g, h, null).
connection(h, g, null).
connection(h, a, null).
connection(a, h, null).

% Time horizon
time(0..20).

% Player identifier (only one player)
player(p).

% --- Rules ---

% Player starts in the starting room at time 0
at(p, a, 0).

% Key obtainment: if the player is in a room with a key at time t,
% they obtain the key at time t.
has_key(p, K, T) :- key(K), at(p, R, T), item_location(K, R), time(T).

% Traversable connections:
% 1. No key required
traversable(p, From, To, T) :- connection(From, To, null), at(p, From, T), time(T).
% 2. Key required and player has the key
traversable(p, From, To, T) :- connection(From, To, K), has_key(p, K, T), at(p, From, T), time(T).

% Player movement: at time T+1, the player can be in any room To
% that is reachable via a traversable connection from their current room From.
{ at(p, To, T+1) : traversable(p, From, To, T) } 1 :- at(p, From, T), time(T), time(T+1).

% Visited rooms: a room is visited if the player is in it at any time.
visited(R) :- at(p, R, T), time(T).

% All rooms must be visited
:- room(R), not visited(R).

% --- Show directives ---
#show connection/3.
#show item_location/2.
#show visited/1.
#show at/3.
#show has_key/3.