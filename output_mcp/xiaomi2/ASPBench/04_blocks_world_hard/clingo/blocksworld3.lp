% ============================
% BLOCKS & WEIGHTS
% ============================
block(a). block(b). block(c). block(d). block(e). block(f).
block(g). block(h). block(i). block(j). block(k). block(l).

weight(a,1). weight(b,2). weight(c,3). weight(d,4).
weight(e,5). weight(f,6). weight(g,7). weight(h,8).
weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% ============================
% TIME HORIZON
% ============================
#const maxtime = 30.
time(0..maxtime).

% ============================
% INITIAL STATE (time 0)
% ============================
on(d, table, 0). on(c, d, 0). on(b, c, 0). on(a, b, 0).
on(h, table, 0). on(g, h, 0). on(f, g, 0). on(e, f, 0).
on(l, table, 0). on(k, l, 0). on(j, k, 0). on(i, j, 0).

% ============================
% GOAL STATE
% ============================
goal(l, table). goal(i, l). goal(f, i). goal(c, f).
goal(k, table). goal(h, k). goal(e, h). goal(b, e).
goal(j, table). goal(g, j). goal(d, g). goal(a, d).

:- goal(X, Y), not on(X, Y, maxtime).

% ============================
% Each block on exactly one location per time
% ============================
1 { on(X, table, T) ; on(X, Y, T) : block(Y) } 1 :- block(X), time(T).

% A block cannot be placed on itself
:- on(X, X, T), block(X), time(T).

% ============================
% CLEAR DEFINITION
% ============================
has_on_top(Y, T) :- on(_, Y, T), block(Y), time(T).
clear(X, T) :- block(X), time(T), not has_on_top(X, T).

% ============================
% ACTIONS: at most one move per time step
% ============================
{ move(X, table, T) ; move(X, Y, T) : block(Y) } 1 :- time(T), T > 0.

% ============================
% ACTION PRECONDITIONS
% ============================
% Block must be clear before move
:- move(X, _, T), not clear(X, T-1).

% Source and destination must differ
:- move(X, To, T), on(X, To, T-1).

% If destination is a block, it must be clear
:- move(X, Y, T), block(Y), not clear(Y, T-1).

% Weight constraint: destination block must be heavier
:- move(X, Y, T), block(Y), weight(X, WX), weight(Y, WY), WY < WX.

% ============================
% EFFECTS
% ============================
on(X, table, T) :- move(X, table, T), time(T), T > 0.
on(X, Y, T) :- move(X, Y, T), block(Y), time(T), T > 0.

% ============================
% FRAME AXIOM (persistence)
% ============================
moved(X, T) :- move(X, _, T).
on(X, Y, T) :- on(X, Y, T-1), time(T), T > 0, not moved(X, T).

% ============================
% TABLE LIMIT: at most 6 blocks on table
% ============================
:- 7 { on(X, table, T) : block(X) }, time(T).

% ============================
% HEIGHT LIMIT: no tower exceeds height 5
% Use unrolled depth levels (no recursion)
% ============================
at_depth_1(X, T) :- on(X, table, T), time(T).
at_depth_2(X, T) :- on(X, Y, T), at_depth_1(Y, T), time(T).
at_depth_3(X, T) :- on(X, Y, T), at_depth_2(Y, T), time(T).
at_depth_4(X, T) :- on(X, Y, T), at_depth_3(Y, T), time(T).
at_depth_5(X, T) :- on(X, Y, T), at_depth_4(Y, T), time(T).
:- on(X, Y, T), at_depth_5(Y, T), time(T).

% ============================
% OPTIMIZATION: minimize number of moves
% ============================
#minimize { 1,X,To,T : move(X,To,T) }.

% ============================
% SYMMETRY BREAKING
% ============================
:- move(X, Y, T), move(X, Z, T+1), on(X, Z, T-1).

% ============================
% OUTPUT
% ============================
plan_length(N) :- N = #count{ X,To,T : move(X,To,T) }.
#show plan_length/1.
#show move/3.