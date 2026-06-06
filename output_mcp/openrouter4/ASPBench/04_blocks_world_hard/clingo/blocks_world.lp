% Blocks World Planning Problem
% Transform stacks of weighted blocks from initial to goal configuration

% ========== DOMAIN DEFINITION ==========

#const max_time = 50.

% Blocks A through L
block(a;b;c;d;e;f;g;h;i;j;k;l).

% Weights
weight(a,1). weight(b,2). weight(c,3). weight(d,4). weight(e,5). weight(f,6).
weight(g,7). weight(h,8). weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% Positions: table or any block
position(table).
position(X) :- block(X).

% Time horizon
time(0..max_time).

% ========== INITIAL STATE (time 0) ==========

% Stack 1: D on table, C on D, B on C, A on B
on(d, table, 0).
on(c, d, 0).
on(b, c, 0).
on(a, b, 0).

% Stack 2: H on table, G on H, F on G, E on F
on(h, table, 0).
on(g, h, 0).
on(f, g, 0).
on(e, f, 0).

% Stack 3: L on table, K on L, J on K, I on J
on(l, table, 0).
on(k, l, 0).
on(j, k, 0).
on(i, j, 0).

% ========== STATE CONSTRAINTS ==========

% Each block is on exactly one thing at any time
:- block(X), time(T), #count { Y : on(X, Y, T) } != 1.

% No two blocks can be on the same block at the same time
:- block(Y), time(T), #count { X : on(X, Y, T) } > 1.

% ========== DERIVED PREDICATES ==========

% A block is occupied if something is on top of it
occupied(X, T) :- on(Y, X, T), block(Y), time(T).

% A block is clear if nothing is on top of it
clear(X, T) :- block(X), time(T), not occupied(X, T).

% ========== ACTION CHOICE ==========

% At each step (1..max_time), at most one move occurs
0 { move(X, From, To, T) : block(X), position(From), position(To) } 1 :- time(T), T > 0.

% ========== MOVE PRECONDITIONS ==========

% Block must be at the source position
:- move(X, From, _, T), not on(X, From, T-1).

% Block must be clear (nothing on top of it)
:- move(X, _, _, T), occupied(X, T-1).

% Destination block must be clear
:- move(X, _, Y, T), block(Y), occupied(Y, T-1).

% Source and destination must be different
:- move(X, From, To, T), From = To.

% Block cannot be placed on itself
:- move(X, _, X, T).

% Weight constraint: heavier block cannot be placed on a lighter one
:- move(X, _, Y, T), block(Y), weight(X, WX), weight(Y, WY), WY < WX.

% ========== MOVE EFFECTS ==========

% After moving, the block is at the destination
on(X, To, T) :- move(X, _, To, T), T > 0.

% ========== FRAME AXIOMS ==========

% State persists if the block did not move
on(X, Y, T) :- on(X, Y, T-1), time(T), T > 0, not moved_block(X, T).
moved_block(X, T) :- move(X, _, _, T), T > 0.

% ========== GLOBAL CONSTRAINTS ==========

% Table limit: at most 6 blocks may be directly on the table at any time
:- #count { X : on(X, table, T) } > 6, time(T).

% Height limit: no tower may exceed height 5
height(X, 1, T) :- on(X, table, T), time(T).
height(X, H, T) :- on(X, Y, T), height(Y, H1, T), H = H1 + 1, time(T).
:- height(X, H, T), H > 5, time(T).

% ========== GOAL STATE (at max_time) ==========

% Tower 1: L on table, I on L, F on I, C on F
:- not on(l, table, max_time).
:- not on(i, l, max_time).
:- not on(f, i, max_time).
:- not on(c, f, max_time).

% Tower 2: K on table, H on K, E on H, B on E
:- not on(k, table, max_time).
:- not on(h, k, max_time).
:- not on(e, h, max_time).
:- not on(b, e, max_time).

% Tower 3: J on table, G on J, D on G, A on D
:- not on(j, table, max_time).
:- not on(g, j, max_time).
:- not on(d, g, max_time).
:- not on(a, d, max_time).

% ========== OPTIMIZATION ==========

% Minimize the number of moves
#minimize { 1@1, X, T : move(X, _, _, T) }.

% ========== OUTPUT ==========

plan_length(N) :- N = #count { T : move(_, _, _, T) }.
#show plan_length/1.
#show move/4.