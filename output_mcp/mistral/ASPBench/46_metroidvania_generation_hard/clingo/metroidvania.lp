% Domains
room(start; r1; r2; r3; r4; r5; r6; r7; r8; r9; r10; goal).
item(redKey; blueKey; greenKey; yellowKey; boots; grapple).
specialType(flooded; chasm).
key(redKey; blueKey; greenKey; yellowKey).
equipment(boots; grapple).

% Room types for special rooms
% Exactly one room is Flooded and one is Chasm (from R1-R10)
1 { special_room_type(R, flooded) : room(R) } 1 :- room(R), R != start, R != goal.
1 { special_room_type(R, chasm) : room(R) } 1 :- room(R), R != start, R != goal.

% Item placement: all 6 items must be placed in R1-R10
1 { item_location(I, R) : room(R) } 1 :- item(I), R != start, R != goal.

% Equipment cannot be placed in rooms of the type they enable
:- item_location(boots, R), special_room_type(R, flooded).
:- item_location(grapple, R), special_room_type(R, chasm).

% YellowKey must be in the Chasm room (creates Grapple prerequisite)
:- item_location(yellowKey, R), not special_room_type(R, chasm).

% Connection representation
% Directed edges with possible requirements (keys or null)
{ connection(F, T, Req) : req(Req) } :- room(F), room(T), F != T.

% Define possible requirements
req(null).
req(K) :- key(K).

% Count bidirectional pairs (pairs of rooms connected both ways)
bidirectional_pair(F, T) :- connection(F, T, _), connection(T, F, _), F < T.

% Count one-way connections (directed edges without a return edge)
oneway_connection(F, T) :- connection(F, T, _), not connection(T, F, _).

% Count incoming connections to Goal
goal_incoming :- connection(F, goal, _).

% Constraints on connections:
% 1. 10-15 bidirectional pairs
:- not 10 <= #count { bidirectional_pair(F,T) : bidirectional_pair(F,T) } <= 15.

% 2. Exactly 2 one-way connections
:- #count { oneway_connection(F,T) : oneway_connection(F,T) } != 2.

% 3. For bidirectional pairs, if one direction requires a key, the other must be keyless
:- bidirectional_pair(F, T),
   connection(F, T, Req1),
   connection(T, F, Req2),
   Req1 != null,
   Req2 != null.

% 4. Goal room constraints:
% - Exactly one incoming connection
:- not #count { connection(F,goal,_) : connection(F,goal,_) } = 1.
% - No outgoing connections
:- connection(goal, _, _).

% Reachability and progression model
% We'll compute reachability with item collection

% Base case: Start is reachable at time 0
reached(0, start).

% Items are collected when first reaching a room that contains them
collected_item(0, I) :- item_location(I, start).

% Transition: from a reachable room, we can move to a connected room
% if we have the required item (or it's keyless)
reached(T+1, R2) :-
    reached(T, R1),
    connection(R1, R2, Req),
    (Req == null ; collected_item(T, Req)),
    time(T),
    T < 20.

% Collect items when reaching a new room
collected_item(T+1, I) :- 
    reached(T+1, R),
    item_location(I, R),
    not collected_item(T, I),
    time(T).

% We have an item at time T if we collected it at any time <= T
collected_item(T, I) :- collected_item(T2, I), time(T2), T2 <= T.

% All rooms must be reachable
:- room(R), not reached(_, R).

% Track first time each room is reached
first_reached(R, T) :- reached(T, R), not reached(T-1, R).

% Goal must be the last room reached
:- first_reached(goal, T1),
   first_reached(R, T2),
   R != goal,
   T1 =< T2.

% Goal cannot be reached before Grapple is obtained
:- reached(T, goal), not collected_item(T, grapple).

% Time step definition
time(0..20).

% Show directives
#show special_room_type/2.
#show item_location/2.
#show connection/3.

% Solution validity check
solution_valid :- 
    10 <= #count { bidirectional_pair(F,T) : bidirectional_pair(F,T) } <= 15,
    #count { oneway_connection(F,T) : oneway_connection(F,T) } = 2,
    #count { connection(F,goal,_) : connection(F,goal,_) } = 1,
    not connection(goal, _, _).

#show solution_valid.
#show special_room_type/2.
#show item_location/2.
#show connection/3.