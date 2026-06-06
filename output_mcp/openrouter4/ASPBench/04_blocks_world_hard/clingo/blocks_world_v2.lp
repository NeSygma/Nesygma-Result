% Blocks World Planning - Transform stacks with weighted blocks

% ========== DOMAIN ==========
#const max_time = 20.

% Blocks A through L
block(a;b;c;d;e;f;g;h;i;j;k;l).

% Weights
weight(a,1). weight(b,2). weight(c,3). weight(d,4).
weight(e,5). weight(f,6). weight(g,7). weight(h,8).
weight(i,9). weight(j,10). weight(k,11). weight(l,12).

% Time
time(0..max_time).
step(1..max_time).

% ========== INITIAL STATE ==========
% Stack 1: D-C-B-A (D on table, C on D, B on C, A on B)
on(d,table,0). on(c,d,0). on(b,c,0). on(a,b,0).
% Stack 2: H-G-F-E
on(h,table,0). on(g,h,0). on(f,g,0). on(e,f,0).
% Stack 3: L-K-J-I
on(l,table,0). on(k,l,0). on(j,k,0). on(i,j,0).

% ========== STATE CONSTRAINTS ==========
% Each block is on exactly one thing
:- block(X), time(T), { on(X,Y,T) : position(Y) } != 1.

% No two blocks on the same block
:- block(Y), time(T), { on(X,Y,T) : block(X) } > 1.

% Position types
position(table).
position(X) :- block(X).

% ========== HELPER PREDICATES ==========
% Clear block: nothing on top of it
clear(X,T) :- block(X), time(T), not on(_,X,T).

% Weight check: can X be placed on Y? (Y must be at least as heavy or Y is table)
weight_ok(X,Y) :- block(X), block(Y), weight(X,WX), weight(Y,WY), WY >= WX.
weight_ok(X,table) :- block(X).

% Distinctness check
distinct(X,Y) :- X != Y.

% ========== TABLE LIMIT CONSTRAINT ==========
% At most 6 blocks on table at any time
:- time(T), not { on(X,table,T) : block(X) } <= 6.

% ========== HEIGHT LIMIT CONSTRAINT ==========
% Define chain: Y is directly below X (Y supports X)
% Then transitive: if Y below Z and Z below X, Y below X
below_dir(Y,X,T) :- on(X,Y,T), block(Y), block(X), time(T).
below(Y,X,T) :- below_dir(Y,X,T).
below(Y,X,T) :- below_dir(Y,Z,T), below(Z,X,T).

% Height constraint: no block has >= 5 blocks below it (max height 5)
:- block(X), time(T), { Y : below(Y,X,T) } >= 5.

% ========== MOVE GENERATION ==========
% Possible move: block X from From to To at step T
possible(X,From,To,T) :- 
    step(T), on(X,From,T-1), clear(X,T-1),
    position(To), To != From, To != X,
    weight_ok(X,To), (To=table; clear(To,T-1)).

% Choose exactly 0 or 1 move per step
{ move(X,From,To,T) : possible(X,From,To,T) } 1 :- step(T).

% Block that moved at step T
moved(X,T) :- move(X,_,_,T), step(T).

% ========== EFFECTS ==========
on(X,To,T) :- move(X,_,To,T), step(T), time(T).

% ========== FRAME AXIOMS ==========
on(X,Y,T) :- on(X,Y,T-1), step(T), not moved(X,T), time(T).

% ========== GOAL STATE ==========
% Tower 1: L on table, I on L, F on I, C on F
:- not on(l,table,max_time).
:- not on(i,l,max_time).
:- not on(f,i,max_time).
:- not on(c,f,max_time).

% Tower 2: K on table, H on K, E on H, B on E
:- not on(k,table,max_time).
:- not on(h,k,max_time).
:- not on(e,h,max_time).
:- not on(b,e,max_time).

% Tower 3: J on table, G on J, D on G, A on D
:- not on(j,table,max_time).
:- not on(g,j,max_time).
:- not on(d,g,max_time).
:- not on(a,d,max_time).

% ========== OPTIMIZATION ==========
#minimize { 1,T : move(_,_,_,T) }.

% ========== OUTPUT ==========
plan_length(N) :- N = #sum { 1,T : move(_,_,_,T) }.
#show plan_length/1.
#show move/4.