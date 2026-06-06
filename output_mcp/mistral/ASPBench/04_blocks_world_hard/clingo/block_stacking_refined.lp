%% Block stacking planning problem (Refined)

% --- Block and weight declarations ---
block(a; b; c; d; e; f; g; h; i; j; k; l).
weight(a,1; b,2; c,3; d,4; e,5; f,6; g,7; h,8; i,9; j,10; k,11; l,12).

% --- Initial configuration (time 0) ---
on(d, "table", 0).
on(c, d, 0).
on(b, c, 0).
on(a, b, 0).
on(h, "table", 0).
on(g, h, 0).
on(f, g, 0).
on(e, f, 0).
on(l, "table", 0).
on(k, l, 0).
on(j, k, 0).
on(i, j, 0).

% --- Time steps ---
max_time(50).
time(0..T) :- max_time(T).

% --- Clear blocks: a block is clear if nothing is on it ---
clear(Block, T) :- block(Block), time(T), not on(_, Block, T).

% --- Choice rule: possible moves at each time step ---
1 { move(Block, From, To, T) : block(Block), 
                          valid_from(Block, From, T), 
                          valid_to(Block, To, T), 
                          From != To } 1 :- time(T), T > 0.

% --- Preconditions for valid moves ---
% Valid 'from' position: the block is on that support at time T
valid_from(Block, From, T) :- move(Block, From, To, T), on(Block, From, T).

% Valid 'to' position: either table or a clear block
valid_to(Block, "table", T) :- move(Block, From, To, T), time(T), To == "table".
valid_to(Block, To, T) :- move(Block, From, To, T), time(T), block(To), clear(To, T).

% Weight constraint: if placing on a block, it must be >= weight of Block
:- move(Block, From, To, T), block(To), To != "table",
   weight(Block, W1), weight(To, W2), W1 > W2.

% --- Effects of moves ---
% When a block is moved, it is no longer on its previous support
:- move(Block, From, To, T),
   on(Block, From, T),
   on(Block, From, T+1).

% When a block is moved, it is on its new support at T+1
on(Block, To, T+1) :- move(Block, From, To, T).

% Frame axiom: if a block is not moved, it stays where it is
on(Block, Support, T+1) :- on(Block, Support, T),
                            time(T),
                            T < max_time,
                            not moved(Block, T).
moved(Block, T) :- move(Block, _, _, T).

% --- Constraints ---

% Table limit: at most 6 blocks directly on table at any time
:- time(T), #count{ B : on(B, "table", T) } > 6.

% Height limit: no tower may exceed height 5 (including base on table)
% For each stack with base on table, count the number of blocks in that stack
% We need to ensure that for each stack, the count <= 5
% To do this, we can group blocks by their base support

% Helper: base_support(B, Base, T) means B is in the stack with base 'Base' at time T
base_support(B, Base, T) :- on(B, Base, T), Base != "table".
base_support(B, B, T) :- on(B, "table", T).

% Count the number of blocks in each stack
stack_size(Base, N, T) :- Base = "table",
                          time(T),
                          N = #count{ B : on(B, "table", T) }.
stack_size(Base, N, T) :- block(Base),
                          Base != "table",
                          time(T),
                          N = #count{ B : base_support(B, Base, T) }.

% Enforce height limit
:- time(T), stack_size(Base, N, T), N > 5.

% --- Goal configuration: define the goal as a set of facts ---
goal_on(l, "table").
goal_on(i, l).
goal_on(f, i).
goal_on(c, f).

goal_on(k, "table").
goal_on(h, k).
goal_on(e, h).
goal_on(b, e).

goal_on(j, "table").
goal_on(g, j).
goal_on(d, g).
goal_on(a, d).

% --- Goal achievement: the goal is achieved if all goal_on facts are true at time T ---
% We use a choice rule to allow the solver to declare that the goal is achieved at some time T
{ goal_achieved(T) : time(T) } 1.

% --- Ensure that if the goal is achieved at time T, all goal_on facts are true at T ---
:- goal_achieved(T), goal_on(Block, Support), not on(Block, Support, T).

% --- Minimize the time to achieve the goal ---
#minimize { T : goal_achieved(T) }.

% --- Ensure plan length does not exceed 50 moves ---
% The number of moves is the number of time steps where a move occurs
plan_length(N) :- N = #count{ T : moved(_, T), time(T) }.
:- plan_length(N), N > 50.

% --- Show directives ---
#show move/4.
#show plan_length/1.

% --- Optional: show the final state for verification ---
#show on/3.