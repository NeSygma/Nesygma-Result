% ===== BLOCKS WORLD PLANNING PROBLEM =====

% Domain: Blocks
block(a). block(b). block(c). block(d). block(e). block(f).
block(g). block(h). block(i). block(j). block(k). block(l).

% Weights
weight(a,1). weight(b,2). weight(c,3). weight(d,4).
weight(e,5). weight(f,6). weight(g,7). weight(h,8).
weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% Time horizon - start with smaller horizon, increase if needed
time(0..30).

% Positions: blocks and table
position(B) :- block(B).
position(table).

% ===== INITIAL STATE (Time 0) =====
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

% ===== GOAL STATE =====
% Tower 1: L on table, I on L, F on I, C on F
goal_on(l, table).
goal_on(i, l).
goal_on(f, i).
goal_on(c, f).

% Tower 2: K on table, H on K, E on H, B on E
goal_on(k, table).
goal_on(h, k).
goal_on(e, h).
goal_on(b, e).

% Tower 3: J on table, G on J, D on G, A on D
goal_on(j, table).
goal_on(g, j).
goal_on(d, g).
goal_on(a, d).

% ===== DERIVED PREDICATES =====

% A block is clear if nothing is on top of it
clear(B, T) :- block(B), time(T), not on(_, B, T).

% Count blocks on table
table_count(N, T) :- N = #count{B : block(B), on(B, table, T)}, time(T).

% ===== ACTION GENERATION =====

% At each time step, choose at most one move
0 { move(B, From, To, T) : block(B), position(From), position(To), From != To, B != From, B != To } 1 :- time(T), T > 0.

% ===== PRECONDITIONS =====

% Can only move a clear block
:- move(B, _, _, T), not clear(B, T-1).

% Source must be current position
:- move(B, From, _, T), not on(B, From, T-1).

% Destination must be clear (if placing on a block)
:- move(B, _, To, T), block(To), not clear(To, T-1).

% Weight constraint: cannot place heavier block on lighter block
:- move(B, _, To, T), block(To), weight(B, WB), weight(To, WT), WB > WT.

% ===== EFFECTS =====

% After move: block is now at destination
on(B, To, T) :- move(B, _, To, T), time(T), T > 0.

% Frame axiom: position persists if not moved
on(B, Pos, T) :- on(B, Pos, T-1), time(T), T > 0, not move(B, Pos, _, T).

% ===== CONSTRAINTS =====

% Table limit: at most 6 blocks on table
:- table_count(N, T), N > 6.

% Height limit: no tower exceeds height 5
depth(B, 1, T) :- on(B, table, T), block(B), time(T).
depth(B, D+1, T) :- on(B, B2, T), block(B), block(B2), time(T), depth(B2, D, T).
:- depth(_, D, T), D > 5.

% ===== GOAL CHECK =====
% Check that all goal conditions are met at some time step
goals_met_count(N, T) :- N = #count{B,Pos : goal_on(B,Pos), on(B,Pos,T)}, time(T), T > 0.
total_goals(N) :- N = #count{B,Pos : goal_on(B,Pos)}.

% Find the final time step where a move occurs
final_time(T) :- T = #max{TT : time(TT), move(_,_,_,TT)}.

% All goals must be satisfied at the final move time
:- final_time(T), goals_met_count(N1, T), total_goals(N2), N1 != N2.

% ===== OPTIMIZATION =====
% Minimize number of moves
#minimize { 1,B,From,To,T : move(B, From, To, T) }.

% ===== OUTPUT =====
#show move/4.