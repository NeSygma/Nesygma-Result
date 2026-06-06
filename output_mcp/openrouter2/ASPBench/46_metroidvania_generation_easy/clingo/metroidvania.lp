% Rooms
room(a). room(b). room(c). room(d). room(e). room(f). room(g). room(h).

% Keys
key(key1). key(key2). key(key3). key(none).

% Starting room
start(a).

% Choice of connections: at most 12 edges
1 { conn(F,T,K) : room(F), room(T), F != T, key(K) } 12.

% Each room except start has at least one incoming edge
in_edge(R) :- conn(_,R,_).
:- room(R), R != a, not in_edge(R).

% Key placement: each key in exactly one room
1 { key_loc(K,R) : room(R) } 1 :- key(K), K != none.
% At most one key per room
:- key_loc(K1,R), key_loc(K2,R), K1 != K2.

% Reachability without using a specific key
reachable_without_key(K,a) :- key(K), K != none.
reachable_without_key(K,R) :- conn(F,R,K2), reachable_without_key(K,F), K2 != K, K != none.

% Key must be reachable without using itself
:- key(K), K != none, key_loc(K,R2), not reachable_without_key(K,R2).

% Reachability
reachable(a).
reachable(R) :- conn(F,R,K), reachable(F), K = none.
reachable(R) :- conn(F,R,K), reachable(F), key_available(K).

% Key availability
key_available(K) :- key(K), K != none, key_loc(K,R2), reachable(R2).

% All rooms reachable
:- room(R), not reachable(R).

% All keys reachable
:- key(K), K != none, not key_available(K).

#show conn/3.
#show key_loc/2.
#show reachable/1.