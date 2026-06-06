% --- Domains ---
room(start; r1; r2; r3; r4; r5; r6; r7; r8; r9; r10; goal).
item(red_key; blue_key; green_key; yellow_key; boots; grapple).
special_type(flooded; chasm).
req(red_key; blue_key; green_key; yellow_key; null).

% --- Item Placement ---
1 { item_loc(I, R) : room(R), R != start, R != goal } 1 :- item(I).
:- item_loc(I1, R), item_loc(I2, R), I1 != I2.

% --- Special Room Types ---
1 { special_room(T, R) : room(R), R != start, R != goal } 1 :- special_type(T).
:- special_room(T1, R), special_room(T2, R), T1 != T2.

% --- Equipment Restrictions ---
:- item_loc(boots, R), special_room(flooded, R).
:- item_loc(grapple, R), special_room(chasm, R).
:- item_loc(yellow_key, R), not special_room(chasm, R).

% --- Connections ---
% Generate potential connections
{ conn(F, T, R) : room(F), room(T), F != T, req(R) }.

% Basic constraints
:- conn(F, T, _), F == goal. 
:- conn(F, T, _), T == start. 
:- conn(F, goal, R), not conn(goal, F, _). 
goal_incoming(F) :- conn(F, goal, _).
:- #count { F : goal_incoming(F) } != 1.

% Bidirectional rule
is_bidirectional(F, T) :- conn(F, T, R1), conn(T, F, R2), F < T.
is_oneway(F, T) :- conn(F, T, R), not conn(T, F, _).

% If any direction requires a key, return must be null
:- conn(F, T, R1), conn(T, F, R2), R1 != null, R2 != null.

% Count connections
num_bidirectional(N) :- N = #count { F, T : is_bidirectional(F, T) }.
num_oneway(N) :- N = #count { F, T : is_oneway(F, T) }.

% --- Reachability ---
% Simplified reachability: all rooms must be reachable
reachable(start).
reachable(T) :- reachable(F), conn(F, T, _).
:- room(R), not reachable(R).

% --- Constraints ---
% 10-15 bidirectional connections
:- num_bidirectional(N), N < 10.
:- num_bidirectional(N), N > 15.
% Exactly two one-way connections (one to goal, one other)
:- num_oneway(N), N != 2.

% --- Final Answer Mapping ---
option(valid) :- num_bidirectional(N), num_oneway(N1).
#show option/1.