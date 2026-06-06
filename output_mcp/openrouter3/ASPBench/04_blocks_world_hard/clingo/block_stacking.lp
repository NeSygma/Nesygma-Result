% Block Stacking Problem
% 12 blocks A-L with weights 1-12
% Initial: 3 stacks of height 4
% Goal: 3 stacks of height 4
% Constraints: clear only, single move, weight constraint, table limit ≤6, height limit ≤5, max 50 moves

% ===== DOMAIN DECLARATIONS =====
block(a). block(b). block(c). block(d). block(e). block(f).
block(g). block(h). block(i). block(j). block(k). block(l).

% Weights
weight(a,1). weight(b,2). weight(c,3). weight(d,4). weight(e,5). weight(f,6).
weight(g,7). weight(h,8). weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% Time steps (0 to 50)
time(0..50).

% ===== INITIAL CONFIGURATION =====
% Stack 1: D on table, C on D, B on C, A on B
on(a,b,0). on(b,c,0). on(c,d,0). on(d,table,0).

% Stack 2: H on table, G on H, F on G, E on F
on(e,f,0). on(f,g,0). on(g,h,0). on(h,table,0).

% Stack 3: L on table, K on L, J on K, I on J
on(i,j,0). on(j,k,0). on(k,l,0). on(l,table,0).

% ===== GOAL CONFIGURATION =====
% Tower 1: L on table, I on L, F on I, C on F
goal_on(l,table). goal_on(i,l). goal_on(f,i). goal_on(c,f).

% Tower 2: K on table, H on K, E on H, B on E
goal_on(k,table). goal_on(h,k). goal_on(e,h). goal_on(b,e).

% Tower 3: J on table, G on J, D on G, A on D
goal_on(j,table). goal_on(g,j). goal_on(d,g). goal_on(a,d).

% ===== ACTIONS =====
% Move action: move(Block, From, To, Time)
% Choice rule: exactly one move per time step
{ move(Block, From, To, T) : block(Block), position(From), position(To) } 1 :- time(T), T < 50.

% Position can be table or any block
position(table).
position(X) :- block(X).

% ===== PRECONDITIONS =====
% Block must be clear (nothing on top) at time T
:- move(Block, From, To, T), on(Block, _, T).

% From must be the actual source at time T
:- move(Block, From, To, T), not on(Block, From, T).

% To must be clear (nothing on top) at time T
:- move(Block, From, To, T), To != table, on(_, To, T).

% Cannot move to itself
:- move(Block, Block, _, T).

% ===== EFFECTS =====
% Frame axiom: State persists unless changed
on(Block, From, T+1) :- on(Block, From, T), time(T), time(T+1), not move(Block, From, _, T).

% New position after move
on(Block, To, T+1) :- move(Block, From, To, T), time(T), time(T+1).

% ===== CONSTRAINTS =====
% Weight constraint: heavier block cannot be on lighter block
% For placing X on Y: weight(Y) >= weight(X)
:- move(Block, From, To, T), To != table, weight(Block, Wb), weight(To, Wt), Wt < Wb.

% Table limit: at most 6 blocks directly on table
:- #count{Block : on(Block, table, T)} > 6, time(T).

% Height limit: no tower may exceed height 5
% Height of a block = 1 + height of block below it
height(Block, T, 1) :- on(Block, table, T).
height(Block, T, H+1) :- on(Block, Below, T), Below != table, height(Below, T, H), H < 5.
:- height(Block, T, H), H > 5.

% ===== GOAL CHECK =====
% Check if goal configuration is reached at time T
goal_at_time(T) :- time(T), 
    on(a, d, T), on(b, e, T), on(c, f, T), on(d, g, T),
    on(e, h, T), on(f, i, T), on(g, j, T), on(h, k, T),
    on(i, l, T), on(j, table, T), on(k, table, T), on(l, table, T).

% ===== OUTPUT =====
#show move/4.
#show on/3.
#show goal_at_time/1.