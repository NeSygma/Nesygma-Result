%% Metroidvania Game World Design
%% Rooms
room(start; r1; r2; r3; r4; r5; r6; r7; r8; r9; r10; goal).

%% Items
item(redKey; blueKey; greenKey; yellowKey; boots; grapple).

%% Keys
key(redKey; blueKey; greenKey; yellowKey).

%% Equipment
equipment(boots; grapple).

%% Special types
special_type(flooded; chasm).

%% Domain for rooms that can have special types or items (R1-R10)
special_room(r1; r2; r3; r4; r5; r6; r7; r8; r9; r10).

%% ============================================================
%% 1. Special Room Types: Exactly one Flooded and one Chasm among R1-R10
%% ============================================================
{ assigned_type(flooded, R) : special_room(R) } 1.
{ assigned_type(chasm, R) : special_room(R) } 1.

%% A room cannot have both types
:- assigned_type(T1, R), assigned_type(T2, R), T1 != T2.

%% ============================================================
%% 2. Item Placement: All 6 items in R1-R10
%% ============================================================
{ placed_in(Item, R) : special_room(R) } 1 :- item(Item).

%% ============================================================
%% 3. Connections
%% ============================================================
req(null; redKey; blueKey; greenKey; yellowKey; boots; grapple).

%% For each ordered pair of distinct rooms, we can have directed edges
{ conn(A, B, Req) : req(Req) } :- room(A), room(B), A != B.

%% Goal room: exactly one incoming connection, no outgoing connections
:- conn(goal, _, _).
1 { conn(A, goal, Req) : room(A), A != goal, req(Req) } 1.

%% Count total edges
total_edges(N) :- N = #count { A, B, Req : conn(A, B, Req) }.

%% Count bidirectional pairs
bidir_pair(A,B) :- conn(A, B, _), conn(B, A, _), A < B.
num_bidir(B) :- B = #count { A, Bp : bidir_pair(A, Bp) }.

%% Count one-way pairs (excluding goal incoming which is mandatory)
oneway_pair(A,B) :- conn(A, B, _), not conn(B, A, _), room(A), room(B), A != B, B != goal.
num_oneway(O) :- O = #count { A, Bp : oneway_pair(A, Bp) }.

%% Constraint: 10-15 total edges (bidirectional count as 2 each, one-way as 1 each)
%% bidir pairs * 2 + oneway + 1 (goal incoming) = total
:- total_edges(N), N < 10.
:- total_edges(N), N > 15.

%% Exactly 1 one-way (non-goal)
:- num_oneway(O), O != 1.

%% ============================================================
%% 4. Key-return constraint: For each bidirectional pair, if any direction requires a key,
%%    there must exist at least one connection in the return direction that is keyless (null)
%% ============================================================
has_key_req(A,B) :- conn(A, B, Req), key(Req).

%% For each pair with a key requirement in one direction, the opposite direction must have a null edge
:- has_key_req(A,B), not conn(B, A, null).
:- has_key_req(B,A), not conn(A, B, null).

%% ============================================================
%% 5. Traversal Rules
%% ============================================================
%% Equipment cannot be placed in the room of the type it enables
:- placed_in(boots, R), assigned_type(flooded, R).
:- placed_in(grapple, R), assigned_type(chasm, R).

%% YellowKey must be in the Chasm room
:- placed_in(yellowKey, R), not assigned_type(chasm, R).
:- assigned_type(chasm, R), not placed_in(yellowKey, R).

%% ============================================================
%% 6. Reachability & Progression
%% ============================================================
%% Time steps 0..12 (max rooms)
time(0..12).

%% State: at(T, R) - player is at room R at time T
%% State: has(T, Item) - player has Item at time T

%% Initial state
at(0, start).
:- at(0, R), R != start.

%% No items at start
:- has(0, Item).

%% Movement: at each time step, player can move to an adjacent room
{ move(T, A, B) : room(B), A != B } 1 :- at(T, A), time(T), T < 12.

%% Can only move if connection exists
:- move(T, A, B), not conn(A, B, _).

%% Can only move if player has required items
:- move(T, A, B), conn(A, B, Req), Req != null, not has(T, Req).

%% Can only enter flooded room with boots
:- move(T, A, B), assigned_type(flooded, B), not has(T, boots).

%% Can only enter chasm room with grapple
:- move(T, A, B), assigned_type(chasm, B), not has(T, grapple).

%% Effects of movement
at(T+1, B) :- move(T, A, B), time(T+1).
at(T+1, A) :- at(T, A), time(T+1), not move(T, A, _).

%% Collect items: if player is in a room with an item, they pick it up
has(T+1, Item) :- has(T, Item), time(T+1).
has(T+1, Item) :- at(T+1, R), placed_in(Item, R), time(T+1).

%% Track when each room is first visited
first_visited(R, T) :- at(T, R), not at(T-1, R), T > 0.
first_visited(start, 0).

%% Goal must be visited at time 12 (last step)
:- not first_visited(goal, 12).

%% All other rooms must be visited by time 11
:- room(R), R != goal, R != start, not first_visited(R, T), time(T), T <= 11.

%% ============================================================
%% 7. Show output
%% ============================================================
#show assigned_type/2.
#show placed_in/2.
#show conn/3.
#show total_edges/1.
#show num_bidir/1.
#show num_oneway/1.