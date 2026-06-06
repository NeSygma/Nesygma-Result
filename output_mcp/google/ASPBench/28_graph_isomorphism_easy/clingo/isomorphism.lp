% --- Graph 1 Data ---
v1(0; 1; 2; 3; 4).
e1(0, 1). e1(0, 2). e1(1, 3). e1(2, 4). e1(3, 4).

% --- Graph 2 Data ---
v2(a; b; c; d; e).
e2(a, b). e2(a, c). e2(b, d). e2(c, e). e2(d, e).

% --- Undirected Adjacency ---
adj1(U, V) :- e1(U, V).
adj1(U, V) :- e1(V, U).
adj2(U, V) :- e2(U, V).
adj2(U, V) :- e2(V, U).

% --- Bijection ---
{ map(V1, V2) : v2(V2) } = 1 :- v1(V1).
{ map(V1, V2) : v1(V1) } = 1 :- v2(V2).

% --- Adjacency Preservation ---
:- e1(U, V), map(U, MU), map(V, MV), not adj2(MU, MV).
:- e2(MU, MV), map(U, MU), map(V, MV), not adj1(U, V).

% --- Degree Preservation (Implicitly handled by adjacency preservation) ---

% --- Result ---
is_isomorphic :- map(_, _).

% Mapping output
mapping(V1, V2) :- map(V1, V2).

% Preserved edges output
preserved_edge(U, V, MU, MV) :- e1(U, V), map(U, MU), map(V, MV).

% --- Option Mapping ---
option(true) :- is_isomorphic.
option(false) :- not is_isomorphic.

#show mapping/2.
#show preserved_edge/4.
#show option/1.