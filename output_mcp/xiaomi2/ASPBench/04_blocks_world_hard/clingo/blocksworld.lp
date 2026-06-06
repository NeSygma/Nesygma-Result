% ============================
% BLOCKS & WEIGHTS
% ============================
block(a). block(b). block(c). block(d). block(e). block(f).
block(g). block(h). block(i). block(j). block(k). block(l).

weight(a,1). weight(b,2). weight(c,3). weight(d,4).
weight(e,5). weight(f,6). weight(g,7). weight(h,8).
weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% ============================
% TIME HORIZON (max 50 moves)
% ============================
time(0..50).

% ============================
% LOCATIONS (table + blocks)
% ============================
location(table).
location(X) :- block(X).

% ============================
% INITIAL STATE (time 0)
% Stack 1: D on table, C on D, B on C, A on B
% Stack 2: H on table, G on H, F on G, E on F
% Stack 3: L on table, K on L, J on K, I on J
% ============================
on(d, table, 0). on(c, d, 0). on(b, c, 0). on(a, b, 0).
on(h, table, 0). on(g, h, 0). on(f, g, 0). on(e, f, 0).
on(l, table, 0). on(k, l, 0). on(j, k, 0). on(i, j, 0).

% ============================
% GOAL STATE (must hold at time 50)
% Tower 1: L on table, I on L, F on I, C on F
% Tower 2: K on table, H on K, E on H, B on E
% Tower 3: J on table, G on J, D on G, A on D
% ============================
:- not on(l, table, 50).
:- not on(i, l, 50).
:- not on(f, i, 50).
:- not on(c, f, 50).
:- not on(k, table, 50).
:- not on(h, k, 50).
:- not on(e, h, 50).
:- not on(b, e, 50).
:- not on(j, table, 50).
:- not on(g, j, 50).
:- not on(d, g, 50).
:- not on(a, d, 50).

% ============================
% STATE: each block on exactly one location per time
% ============================
1 { on(X, Y, T) : location(Y) } 1 :- block(X), time(T).

% A block cannot be placed on itself
:- on(X, X, T), block(X), time(T).

% ============================
% CLEAR DEFINITION
% ============================
has_on_top(Y, T) :- on(X, Y, T), block(X), time(T).
clear(X, T) :- block(X), time(T), not has_on_top(X, T).

% ============================
% ACTIONS: at most one move per time step
% Choose (block, destination) where block is clear
% ============================
{ move(X, To, T) : block(X), location(To), clear(X, T-1) } 1 :- time(T), T > 0.

% Derive source location for output
move_from(X, From, T) :- move(X, To, T), on(X, From, T-1).

% ============================
% ACTION PRECONDITIONS
% ============================
% Source and destination must differ
:- move(X, To, T), on(X, To, T-1).

% If destination is a block, it must be clear
:- move(X, To, T), block(To), not clear(To, T-1).

% Weight constraint: destination block must be >= weight of moved block
:- move(X, To, T), block(To), weight(X, WX), weight(To, WT), WT < WX.

% ============================
% EFFECTS
% ============================
on(X, To, T) :- move(X, To, T), time(T), T > 0.

% ============================
% FRAME AXIOM (persistence)
% ============================
moved(X, T) :- move(X, _, T).
on(X, Y, T) :- on(X, Y, T-1), time(T), T > 0, not moved(X, T).

% ============================
% TABLE LIMIT: at most 6 blocks on table
% ============================
:- #count{ X : on(X, table, T) } > 6, time(T).

% ============================
% HEIGHT LIMIT: no tower exceeds height 5
% ============================
depth(table, T, 0) :- time(T).
depth(X, T, D) :- on(X, Y, T), time(T), depth(Y, T, D1), D = D1 + 1.
:- depth(X, T, D), D > 5, time(T).

% ============================
% OPTIMIZATION: minimize number of moves
% ============================
#minimize { 1,X,To,T : move(X,To,T) }.

% ============================
% OUTPUT
% ============================
plan_length(N) :- N = #count{ X,To,T : move(X,To,T) }.
#show plan_length/1.
#show move_from/3.
#show move/3.