% ==================== DOMAINS ====================
room(start). room(goal).
room(r1). room(r2). room(r3). room(r4). room(r5).
room(r6). room(r7). room(r8). room(r9). room(r10).

key(red_key). key(blue_key). key(green_key). key(yellow_key).
equipment(boots). equipment(grapple).
item(I) :- key(I).
item(I) :- equipment(I).

special_type(flooded). special_type(chasm).

interior(R) :- room(R), R != start, R != goal.

time(0..30).

% ==================== SPECIAL ROOM PLACEMENT ====================
{ special_room(T, R) : interior(R) } 1 :- special_type(T).
:- special_room(flooded, R), special_room(chasm, R).

% ==================== ITEM PLACEMENT ====================
{ item_room(I, R) : interior(R) } 1 :- item(I).
:- item_room(I1, R), item_room(I2, R), I1 != I2.

% Equipment cannot be in the room type it enables
:- item_room(boots, R), special_room(flooded, R).
:- item_room(grapple, R), special_room(chasm, R).

% YellowKey must be in Chasm room
:- item_room(yellow_key, R), not special_room(chasm, R).

% ==================== CONNECTIONS ====================
{ conn(A, B, null) } :- room(A), room(B), A != B.
{ conn(A, B, K) } :- room(A), room(B), A != B, key(K).

% At most one connection per ordered pair
:- conn(A, B, R1), conn(A, B, R2), R1 != R2.

has_conn(A, B) :- conn(A, B, _).
bidir(A, B) :- has_conn(A, B), has_conn(B, A), A < B.
oneway(A, B) :- has_conn(A, B), not has_conn(B, A).

% 10-15 bidirectional connections
:- #count { A, B : bidir(A, B) } < 10.
:- #count { A, B : bidir(A, B) } > 15.

% Exactly 2 one-way edges total (1 general + 1 to Goal)
:- #count { A, B : oneway(A, B) } != 2.

% Goal: exactly one incoming, no outgoing
:- #count { A : has_conn(A, goal) } != 1.
:- has_conn(goal, _).

% Bidirectional key rule: if one direction requires key, return must be keyless
:- bidir(A, B), conn(A, B, K1), K1 != null, conn(B, A, K2), K2 != null.

% ==================== GAME STATE SIMULATION ====================
% Initial state
pos(start, 0).
visited(start, 0).

% Actions: pick up item or move (at most one per time step)
0 { do_pickup(I, T) : item(I) } 1 :- time(T), T > 0.
0 { do_move(A, B, T) : room(A), room(B), has_conn(A, B) } 1 :- time(T), T > 0.
:- do_pickup(I, T), do_move(A, B, T).

% Pickup preconditions
:- do_pickup(I, T), has_item(I, T-1).  % Don't pick up what you have
:- do_pickup(I, T), item_room(I, R), not pos(R, T).  % Must be in room

% Move preconditions
:- do_move(A, B, T), not pos(A, T).  % Must be in source room
:- do_move(A, B, T), conn(A, B, K), K != null, not has_item(K, T).  % Need key
:- do_move(A, B, T), special_room(flooded, B), not has_item(boots, T).  % Need boots
:- do_move(A, B, T), special_room(chasm, B), not has_item(grapple, T).  % Need grapple

% Helper: detect if player moves from R at time T
moves_from(R, T) :- do_move(R, _, T).

% State transitions - Position
pos(R, T) :- pos(R, T-1), time(T), T > 0, not moves_from(R, T).
pos(B, T) :- do_move(A, B, T).

% State transitions - Items (persist and acquire)
has_item(I, T) :- has_item(I, T-1), time(T), T > 0.
has_item(I, T) :- do_pickup(I, T).

% State transitions - Visited rooms
visited(R, T) :- visited(R, T-1), time(T), T > 0.
visited(R, T) :- pos(R, T).

% ==================== REACHABILITY CONSTRAINTS ====================
% All rooms must be visited at some point
visited_at_any_time(R) :- visited(R, T), time(T).
:- room(R), not visited_at_any_time(R).

% First visit detection
visited_before(R, T) :- visited(R, T-1), time(T), T > 0.
first_visit(R, T) :- pos(R, T), not visited_before(R, T).

% Every room must have a first visit
has_first_visit(R) :- first_visit(R, T).
:- room(R), not has_first_visit(R).

% Goal must be the LAST new room reached
:- first_visit(goal, T1), first_visit(R, T2), R != goal, T2 >= T1.

% ==================== OUTPUT ====================
#show special_room/2.
#show item_room/2.
#show conn/3.
#show bidir/2.
#show oneway/2.