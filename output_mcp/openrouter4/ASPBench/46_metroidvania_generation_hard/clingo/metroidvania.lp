%%%=============================================================================
%%% DOMAINS
%%%=============================================================================

% Rooms
room(start; r1; r2; r3; r4; r5; r6; r7; r8; r9; r10; goal).

% Items
item(redkey; bluekey; greenkey; yellowkey; boots; grapple).
key(redkey; bluekey; greenkey; yellowkey).
equipment(boots; grapple).

special_type_name(flooded; chasm).

%%%=============================================================================
%%% CHOICE: Special Room Types
%%%=============================================================================

% Exactly one Flooded room and one Chasm room from R1-R10
{ special_type(R, flooded) : room(R), R != start, R != goal } 1.
{ special_type(R, chasm) : room(R), R != start, R != goal } 1.

% A room cannot have both types
:- special_type(R, T1), special_type(R, T2), T1 != T2.

%%%=============================================================================
%%% CHOICE: Item Placement (R1-R10 only)
%%%=============================================================================

% Each item placed in exactly one room (R1-R10)
{ placed_in(I, R) : room(R), R != start, R != goal } 1 :- item(I).

% No two items in the same room
:- placed_in(I1, R), placed_in(I2, R), I1 != I2.

% Equipment cannot be in the room type it enables
:- placed_in(boots, R), special_type(R, flooded).
:- placed_in(grapple, R), special_type(R, chasm).

% YellowKey must be in the Chasm room
:- placed_in(yellowkey, R), not special_type(R, chasm).
:- special_type(R, chasm), not placed_in(yellowkey, R).

%%%=============================================================================
%%% CHOICE: Connections
%%%=============================================================================

% At most one connection per ordered pair of rooms
% null = no key required
0 { conn_null(A, B); conn_key(A, B, K) : key(K) } 1 :-
    room(A), room(B), A != B.

% Goal constraints: exactly 1 incoming, 0 outgoing
:- #count { A : conn_null(A, goal); A, K : conn_key(A, goal, K) } != 1.
:- conn_null(goal, _).
:- conn_key(goal, _, _).

% Goal's incoming connection must require a key (gates Goal as last room)
:- conn_null(_, goal).

%%%=============================================================================
%%% CONNECTION METRICS
%%%=============================================================================

ordered_conn(A, B) :- conn_null(A, B).
ordered_conn(A, B) :- conn_key(A, B, _).

% Bidirectional pair: both directions exist
bidir_pair(A, B) :- ordered_conn(A, B), ordered_conn(B, A), A < B.

% One-way connection: only one direction exists
oneway_conn(A, B) :- ordered_conn(A, B), not ordered_conn(B, A).

% 10-15 bidirectional pairs
:- N = #count { A,B : bidir_pair(A,B) }, N < 10.
:- N = #count { A,B : bidir_pair(A,B) }, N > 15.

% Exactly 2 one-way connections (Goal incoming + one other)
:- N = #count { A,B : oneway_conn(A,B) }, N != 2.

%%%=============================================================================
%%% BIDIRECTIONAL KEY CONSTRAINT
%%%=============================================================================

% If a bidirectional pair has a key-required connection in one direction,
% the return direction must be keyless (conn_null).
:- bidir_pair(A, B), conn_key(A, B, K), not conn_null(B, A).
:- bidir_pair(A, B), conn_key(B, A, K), not conn_null(A, B).

%%%=============================================================================
%%% REACHABILITY (Fixpoint without using Goal)
%%%=============================================================================

% Helper: can we enter a room given its special type?
entry_ok(R) :- room(R), not special_type(R, flooded), not special_type(R, chasm).
entry_ok(R) :- special_type(R, flooded), have(boots).
entry_ok(R) :- special_type(R, chasm), have(grapple).

% Base: Start is reachable
reachable(start).

% Reachable via null connection
reachable(R) :-
    reachable(A), conn_null(A, R),
    entry_ok(R), R != goal.

% Reachable via key-required connection
reachable(R) :-
    reachable(A), conn_key(A, R, K),
    have(K), entry_ok(R), R != goal.

% Item acquisition: have an item if its room is reachable
have(I) :- reachable(R), placed_in(I, R).

%%%=============================================================================
%%% VERIFICATION CONSTRAINTS
%%%=============================================================================

% All 11 non-Goal rooms must be reachable (without using Goal)
:- room(R), R != goal, not reachable(R).

% Goal must be reachable (using its incoming connection)
goal_reachable :- conn_null(A, goal), reachable(A).
goal_reachable :- conn_key(A, goal, K), reachable(A), have(K).
:- not goal_reachable.

%%%=============================================================================
%%% OUTPUT
%%%=============================================================================

#show special_type/2.
#show placed_in/2.
#show conn_null/2.
#show conn_key/3.
#show bidir_pair/2.
#show oneway_conn/2.
#show ordered_conn/2.
#show reachable/1.
#show have/1.
#show goal_reachable/0.