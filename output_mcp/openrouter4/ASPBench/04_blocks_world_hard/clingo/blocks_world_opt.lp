% Blocks World Planning Problem - Optimized
% Transform stacks of weighted blocks from initial to goal configuration

% ========== DOMAIN DEFINITION ==========

#const max_time = 20.

% Blocks A through L
block(a;b;c;d;e;f;g;h;i;j;k;l).

% Weights
weight(a,1). weight(b,2). weight(c,3). weight(d,4). weight(e,5). weight(f,6).
weight(g,7). weight(h,8). weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% Positions: table or any block
position(table).
position(X) :- block(X).

% Time steps for actions (1..max_time)
step(1..max_time).

% Time points for states (0..max_time)
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

% "under" relation: Y is directly under X
under(Y, X, T) :- on(X, Y, T), block(Y), time(T).

% transitive under: if Y is under Z and Z is under X, then Y is under X
under(Y, X, T) :- under(Y, Z, T), on(X, Z, T), time(T).

% A block is clear if nothing is on top of it
clear(X, T) :- block(X), time(T), not occupied(X, T).

% A block is occupied if something is on top of it
occupied(X, T) :- on(_, X, T), time(T).

% ========== VALID MOVE GENERATION ==========

% Check weight constraint for placing on a block
% Weight(Y) >= Weight(X) for placing X on Y
weight_ok(X, Y) :- weight(X, WX), weight(Y, WY), WY >= WX.

% A move is possible if:
% - block X is clear and on From at T-1
% - To is a valid destination (table or clear block with sufficient weight)
% - To differs from From and X
possible_move(X, From, To, T) :-
    step(T),
    on(X, From, T-1),
    clear(X, T-1),
    position(To),
    To != From,
    To != X,
    (To = table; block(To), clear(To, T-1), weight_ok(X, To)).

% Choose exactly 0 or 1 move per step
0 { move(X, From, To, T) : possible_move(X, From, To, T) } 1 :- step(T).

% ========== MOVE EFFECTS ==========

% After moving, the block is at the destination
on(X, To, T) :- move(X, _, To, T), step(T), time(T).

% ========== FRAME AXIOMS ==========

% State persists if the block did not move
on(X, Y, T) :- on(X, Y, T-1), step(T), not moved_block(X, T).
moved_block(X, T) :- move(X, _, _, T), step(T).

% ========== GLOBAL CONSTRAINTS ==========

% Table limit: at most 6 blocks may be directly on the table at any time
:- #count { X : on(X, table, T) } > 6, time(T).

% Height limit: no tower may exceed height 5
% Height = 1 + number of blocks under X
% No block can have height > 5, meaning at most 4 blocks under it
:- block(X), time(T), #count { Y : under(Y, X, T) } >= 5.

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