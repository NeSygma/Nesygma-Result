% Rooms
room(start). room(goal). room(r1). room(r2). room(r3). room(r4). room(r5). room(r6). room(r7). room(r8). room(r9). room(r10).

% Items
item(redkey). item(bluekey). item(greenkey). item(yellowkey). item(boots). item(grapple).

% Special types (just for reference)
special_type(flooded). special_type(chasm).

% Assign exactly one flooded and one chasm room among r1..r10
{ special_room(R,flooded) : room(R), R != start, R != goal } = 1.
{ special_room(R,chasm)   : room(R), R != start, R != goal } = 1.
:- special_room(R,flooded), special_room(R,chasm).

% Item placement: each item in exactly one room among r1..r10
{ item_loc(I,R) : room(R), R != start, R != goal } = 1 :- item(I).

% Equipment cannot be placed in the room type it enables
:- item_loc(boots,R), special_room(R,flooded).
:- item_loc(grapple,R), special_room(R,chasm).

% YellowKey must be in the Chasm room
:- item_loc(yellowkey,R), not special_room(R,chasm).

% Define the linear chain pairs (10 bidirectional pairs)
pair(start,r1). pair(r1,r2). pair(r2,r3). pair(r3,r4). pair(r4,r5). pair(r5,r6). pair(r6,r7). pair(r7,r8). pair(r8,r9). pair(r9,r10).

% Generate bidirectional connections (requires null)
conn(A,B,null) :- pair(A,B).
conn(B,A,null) :- pair(A,B).

% Extra one-way connection (no reverse)
conn(r3,r7,null).

% Goal edge (one-way into goal)
conn(r10,goal,null).

% Ensure total number of bidirectional pairs is between 10 and 15
:- #count{A,B : pair(A,B)} < 10.
:- #count{A,B : pair(A,B)} > 15.

% Key lock rule: if a directed edge requires a key, the opposite must be keyless
:- conn(A,B,Req), Req != null, not conn(B,A,null).

% Goal constraints
:- conn(goal,_,_).                     % no outgoing from goal
incoming_goal(N) :- conn(N,goal,_).
:- #count{N : incoming_goal(N)} != 1.   % exactly one incoming to goal

% Define one-way detection (edges without opposite)
opposite_exists(A,B) :- conn(B,A,_).
one_way(A,B) :- conn(A,B,_), not opposite_exists(A,B).
% Exactly one extra one-way besides the goal edge
:- #count{A,B : one_way(A,B), B != goal} != 1.
% Ensure total one-way edges (including goal) is 2
:- #count{A,B : one_way(A,B)} != 2.

% Reachability analysis
reachable(start).

% An item is owned when its room becomes reachable
has_item(I) :- item_loc(I,R), reachable(R).

% Entry requirements for special rooms
can_enter(R) :- room(R), not special_room(R,_).                     % normal rooms
can_enter(R) :- room(R), special_room(R,flooded), has_item(boots).   % need boots
can_enter(R) :- room(R), special_room(R,chasm),   has_item(grapple). % need grapple

% Move along connections respecting entry requirements
reachable(To) :- reachable(From), conn(From,To,_), can_enter(To).

% All rooms must be reachable (including goal)
:- room(R), not reachable(R).

% Show solution
#show special_room/2.
#show item_loc/2.
#show conn/3.