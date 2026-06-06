% Metroidvania Game World Design Problem

% ===== DOMAINS =====
% Rooms
room(start). room(goal).
room(r1). room(r2). room(r3). room(r4). room(r5).
room(r6). room(r7). room(r8). room(r9). room(r10).

% Items
item(redkey). item(bluekey). item(greenkey). item(yellowkey).
item(boots). item(grapple).

% Special room types
special_type(flooded). special_type(chasm).

% ===== ITEM PLACEMENT =====
% Items must be placed in R1-R10 only (not Start or Goal)
{ item_in(Item, Room) : room(Room), Room != start, Room != goal } 1 :- item(Item).

% Start and Goal cannot have items
:- item_in(_, start).
:- item_in(_, goal).

% ===== SPECIAL ROOM TYPES =====
% Exactly one Flooded room and one Chasm room from R1-R10
1 { has_special(Room, flooded) : room(Room), Room != start, Room != goal } 1.
1 { has_special(Room, chasm) : room(Room), Room != start, Room != goal } 1.

% Start and Goal cannot have special types
:- has_special(start, _).
:- has_special(goal, _).

% Equipment cannot be in the room type it enables
:- item_in(boots, Room), has_special(Room, flooded).
:- item_in(grapple, Room), has_special(Room, chasm).

% YellowKey must be in Chasm room
:- item_in(yellowkey, Room), not has_special(Room, chasm).

% ===== CONNECTIONS =====
% Define all possible room pairs (excluding self)
room_pair(R1, R2) :- room(R1), room(R2), R1 != R2.

% Connection requirements (key or null)
req(null). req(redkey). req(bluekey). req(greenkey).

% Mandatory one-way connection to Goal
{ oneway_to_goal(From) : room(From), From != goal } 1.
oneway_connection(From, goal, null) :- oneway_to_goal(From).

% Additional one-way connection (exactly one)
{ additional_oneway(From, To, Req) : room_pair(From, To), To != goal, req(Req) } 1.
oneway_connection(From, To, Req) :- additional_oneway(From, To, Req).

% Bidirectional connections: 10-15 of them
{ bidirectional(R1, R2, Req) : room_pair(R1, R2), R1 < R2, req(Req) } 10..15.

% For each bidirectional connection, create both directions
bidirectional_connection(R1, R2, Req) :- bidirectional(R1, R2, Req).
bidirectional_connection(R2, R1, Req) :- bidirectional(R1, R2, Req).

% ===== CONNECTION CONSTRAINTS =====
% Goal must have exactly one incoming connection
incoming_to_goal(N) :- N = #count { From : oneway_connection(From, goal, _) }.
:- incoming_to_goal(N), N != 1.

% No outgoing connections from Goal
:- oneway_connection(goal, _, _).

% For bidirectional connections: at least one direction must be keyless
% We need to check each pair (R1,R2) where both directions exist
:- bidirectional_connection(R1, R2, Req1), bidirectional_connection(R2, R1, Req2), 
   Req1 != null, Req2 != null.

% ===== REACHABILITY SIMULATION =====
% Time steps for simulation
time(0..20).

% Player position at each time
player_at(start, 0).

% Helper: player has item if it's in a room they've visited
has_item(Item, T) :- item_in(Item, Room), player_at(Room, T).

% Movement rules
% Can move via oneway connection if requirements met
can_move(From, To, T) :-
    oneway_connection(From, To, Req),
    player_at(From, T),
    requirement_met(Req, T).

% Can move via bidirectional connection if requirements met
can_move(From, To, T) :-
    bidirectional_connection(From, To, Req),
    player_at(From, T),
    requirement_met(Req, T).

% Requirement met helper
requirement_met(null, T) :- time(T).
requirement_met(redkey, T) :- has_item(redkey, T), time(T).
requirement_met(bluekey, T) :- has_item(bluekey, T), time(T).
requirement_met(greenkey, T) :- has_item(greenkey, T), time(T).

% Special room entry requirements
% To enter Flooded room, need Boots
can_move(From, To, T) :-
    has_special(To, flooded),
    has_item(boots, T),
    player_at(From, T),
    time(T).

% To enter Chasm room, need Grapple
can_move(From, To, T) :-
    has_special(To, chasm),
    has_item(grapple, T),
    player_at(From, T),
    time(T).

% Frame axiom: player stays in same room if no move
player_at(Room, T+1) :- player_at(Room, T), time(T), time(T+1), 
    not can_move(Room, _, T).

% Player moves to new room
player_at(To, T+1) :- can_move(From, To, T), time(T), time(T+1).

% Track which rooms have been visited
visited(Room, T) :- player_at(Room, T).

% ===== PROGRESSION CONSTRAINTS =====
% Goal must be last reachable room
% All other rooms must be visited before Goal is visited
:- visited(goal, T), visited(Room, T), Room != goal, Room != start.

% ===== OUTPUT =====
#show item_in/2.
#show has_special/2.
#show oneway_connection/3.
#show bidirectional_connection/3.
#show visited/2.