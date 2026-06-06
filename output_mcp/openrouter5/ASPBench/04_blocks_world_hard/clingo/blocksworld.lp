%% Blocks World Planning Problem
%% Transform initial configuration to goal configuration

%% Time horizon
time(0..50).

%% Blocks
block(a;b;c;d;e;f;g;h;i;j;k;l).

%% Weights
weight(a,1). weight(b,2). weight(c,3). weight(d,4).
weight(e,5). weight(f,6). weight(g,7). weight(h,8).
weight(i,9). weight(j,10). weight(k,11). weight(l,12).

%% Table
table(table).

%% Initial Configuration
%% Stack 1: D on table, C on D, B on C, A on B
on(d, table, 0).
on(c, d, 0).
on(b, c, 0).
on(a, b, 0).

%% Stack 2: H on table, G on H, F on G, E on F
on(h, table, 0).
on(g, h, 0).
on(f, g, 0).
on(e, f, 0).

%% Stack 3: L on table, K on L, J on K, I on J
on(l, table, 0).
on(k, l, 0).
on(j, k, 0).
on(i, j, 0).

%% Goal Configuration
%% Tower 1: L on table, I on L, F on I, C on F
goal_on(l, table).
goal_on(i, l).
goal_on(f, i).
goal_on(c, f).

%% Tower 2: K on table, H on K, E on H, B on E
goal_on(k, table).
goal_on(h, k).
goal_on(e, h).
goal_on(b, e).

%% Tower 3: J on table, G on J, D on G, A on D
goal_on(j, table).
goal_on(g, j).
goal_on(d, g).
goal_on(a, d).

%% Positions: table or any block
pos(table).
pos(B) :- block(B).

%% A block is clear at time T if nothing is on top of it
clear(B, T) :- block(B), time(T), not on(_, B, T).
clear(table, T) :- time(T).  %% table is always clear

%% Count blocks on table at time T
table_count(N, T) :- N = #count { B : on(B, table, T) }, time(T).

%% Constraint: At most 6 blocks on table at any time
:- table_count(N, T), N > 6.

%% Height of a stack: count blocks in chain from table up
height(B, 1, T) :- on(B, table, T).
height(B, H+1, T) :- on(B, X, T), height(X, H, T), H < 5.

%% Constraint: No tower exceeds height 5
:- height(_, H, T), H > 5.

%% Action choice: at most one move per time step
0 { move(B, Src, Dst, T) : block(B), pos(Src), pos(Dst), Src != Dst, B != Dst } 1 :- time(T), T < 50.

%% Preconditions for moving
%% Block B must be clear at time T
:- move(B, _, _, T), not clear(B, T).

%% Block B must be on Src at time T
:- move(B, Src, _, T), not on(B, Src, T).

%% Destination must be clear at time T (if not table)
:- move(_, _, Dst, T), Dst != table, not clear(Dst, T).

%% Weight constraint: heavier block cannot be placed on lighter block
:- move(B, _, Dst, T), Dst != table, weight(B, Wb), weight(Dst, Wd), Wb > Wd.

%% Effects of moves
%% Block B is on Dst at time T+1
on(B, Dst, T+1) :- move(B, _, Dst, T), time(T+1).

%% Block B is no longer on Src at time T+1
:- move(B, Src, _, T), on(B, Src, T+1).

%% Frame axiom: if no move affected a block's position, it stays
on(B, Pos, T+1) :- on(B, Pos, T), time(T+1), 
                   not move(B, Pos, _, T), not move(B, _, Pos, T).

%% A block cannot be on two different positions at the same time
:- on(B, P1, T), on(B, P2, T), P1 != P2.

%% Goal condition: all goal_on relations must hold at the final time
goal_reached :- goal_on(B, Pos) : on(B, Pos, 50).

%% We must reach the goal at some time point
:- not goal_reached.

%% Show the plan
#show move/4.