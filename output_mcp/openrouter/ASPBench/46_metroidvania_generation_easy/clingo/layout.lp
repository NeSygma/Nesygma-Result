% Rooms and indices
room(a). index(a,1).
room(b). index(b,2).
room(c). index(c,3).
room(d). index(d,4).
room(e). index(e,5).
room(f). index(f,6).
room(g). index(g,7).
room(h). index(h,8).

% Keys and their numeric ids
key(key1,1).
key(key2,2).
key(key3,3).

% Linear chain edges (directed)
edge(From,To) :- index(From,I), I < 8, I1 = I + 1, index(To,I1).

% Assign each key to a specific edge based on source index (deterministic)
requires(From,To,Key) :- edge(From,To), index(From,I), key(Key,K), I = 2 * K.

% Key location: placed in the source room of its required edge
key_loc(Key,From) :- requires(From,To,Key).

% Reachability (player can traverse edges, having keys when needed)
reachable(a).
reachable(To) :- reachable(From), edge(From,To), not requires(From,To,_).
reachable(To) :- reachable(From), edge(From,To), requires(From,To,Key), key_loc(Key,From).

% All rooms must be reachable
:- room(R), not reachable(R).

% Connections output (include null for no key)
connection(From,To,Key) :- requires(From,To,Key).
connection(From,To,"null") :- edge(From,To), not requires(From,To,_).

% Reachability verification flag
bad :- room(R), not reachable(R).
reachability_verified :- not bad.

#show connection/3.
#show key_loc/2.
#show reachability_verified/0.