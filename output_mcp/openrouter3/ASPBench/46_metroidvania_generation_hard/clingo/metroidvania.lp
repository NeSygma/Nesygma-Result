% Metroidvania World Design Problem

% ===== DOMAINS =====
room(start). room(goal).
room(R) :- R = "R1"; R = "R2"; R = "R3"; R = "R4"; R = "R5"; 
           R = "R6"; R = "R7"; R = "R8"; R = "R9"; R = "R10".

item("RedKey"). item("BlueKey"). item("GreenKey"). item("YellowKey").
item("Boots"). item("Grapple").

special_type("flooded"). special_type("chasm").

% ===== SPECIAL ROOM ASSIGNMENT =====
% Exactly one flooded and one chasm room from R1-R10
1 { has_special(R, "flooded") : room(R), R != start, R != goal } 1.
1 { has_special(R, "chasm") : room(R), R != start, R != goal } 1.

% No room can have both special types
:- has_special(R, "flooded"), has_special(R, "chasm").

% ===== ITEM PLACEMENT =====
% All items must be placed in R1-R10 (not Start or Goal)
1 { item_location(I, R) : room(R), R != start, R != goal } 1 :- item(I).

% Equipment cannot be in rooms of the type they enable
:- item_location("Boots", R), has_special(R, "flooded").
:- item_location("Grapple", R), has_special(R, "chasm").

% YellowKey must be in Chasm room
:- item_location("YellowKey", R), not has_special(R, "chasm").

% ===== CONNECTIONS =====
% Define possible connections (excluding Start->Goal direct)
% We'll use choice rules for connections
{ connection(F, T, K) : room(T), T != F, K = null } :- room(F).
{ connection(F, T, K) : room(T), T != F, K = "RedKey" } :- room(F).
{ connection(F, T, K) : room(T), T != F, K = "BlueKey" } :- room(F).
{ connection(F, T, K) : room(T), T != F, K = "GreenKey" } :- room(F).
{ connection(F, T, K) : room(T), T != F, K = "YellowKey" } :- room(F).

% Bidirectional connections: 10-15 pairs
% Count bidirectional connections (use F < T to avoid double counting)
bidirectional(F, T) :- connection(F, T, _), connection(T, F, _), F < T.
bidirectional_count(N) :- N = #count { F, T : bidirectional(F, T) }.

% Constraint: 10-15 bidirectional connections
:- bidirectional_count(N), N < 10.
:- bidirectional_count(N), N > 15.

% One-way connections: exactly 1 (plus mandatory to Goal)
% Count one-way connections (excluding Goal connections)
one_way(F, T) :- connection(F, T, _), not connection(T, F, _), T != goal.
one_way_count(N) :- N = #count { F, T : one_way(F, T) }.

% Exactly one one-way connection (excluding the mandatory Goal connection)
:- one_way_count(N), N != 1.

% Goal room constraints: exactly one incoming connection, no outgoing
% No outgoing connections from Goal
:- connection(goal, T, _).

% Exactly one incoming connection to Goal (fixed unsafe variable)
% Use a helper predicate to ground the connection
incoming_to_goal(F) :- connection(F, goal, _).
1 { incoming_to_goal(F) : room(F), F != goal } 1.

% ===== KEYLESS RETURN PATH REQUIREMENT =====
% For each bidirectional connection, if one direction requires a key,
% the other direction must have at least one keyless connection
:- bidirectional(F, T), connection(F, T, K1), K1 != null,
   not connection(T, F, null).

% ===== EQUIPMENT TRAVERSAL RULES =====
% To enter a Flooded room, player must have Boots
% To enter a Chasm room, player must have Grapple
% We'll model this as constraints on connections to special rooms
:- connection(F, R, _), has_special(R, "flooded"), not item_location("Boots", F).
:- connection(F, R, _), has_special(R, "chasm"), not item_location("Grapple", F).

% ===== REACHABILITY & PROGRESSION =====
% Time steps for progression
time(0..12). % 12 rooms, so up to 12 time steps

% Initial state: Start room reachable at time 0
reachable(start, 0).

% Player starts with no items
has_item(I, 0) :- item(I), false. % No items at start

% Progression rules: move to adjacent room if connection exists and requirements met
% This is complex - we need to model item acquisition and movement

% Simplified approach: Define reachability based on item acquisition
% First, define which items are needed for which connections
needs_item(F, T, I) :- connection(F, T, K), K = I.

% For equipment rooms: need equipment to enter
needs_item(F, R, "Boots") :- connection(F, R, _), has_special(R, "flooded").
needs_item(F, R, "Grapple") :- connection(F, R, _), has_special(R, "chasm").

% Item acquisition: player gets item when reaching its room
has_item(I, T) :- item_location(I, R), reachable(R, T).

% Movement: can move from F to T at time T+1 if:
% 1. F is reachable at time T
% 2. All required items for connection F->T are possessed at time T
% 3. T is not already reachable earlier
% 4. Time bound
reachable(T, T+1) :- connection(F, T, _), reachable(F, T), time(T), time(T+1),
                      forall(needs_item(F, T, I), has_item(I, T)),
                      not reachable(T, T).

% Frame axiom: reachability persists
reachable(R, T+1) :- reachable(R, T), time(T), time(T+1).

% ===== GOAL TIMING CONSTRAINT =====
% Goal must be the last new room reachable
% All other 11 rooms must be reachable before Goal
:- reachable(goal, T), 
   #count { R : reachable(R, T), R != goal } < 11.

% ===== OUTPUT =====
#show room/1.
#show item/1.
#show has_special/2.
#show item_location/2.
#show connection/3.
#show bidirectional/2.
#show reachable/2.