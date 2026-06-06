% Arguments
arg(a1). arg(a2). arg(a3). arg(a4). arg(a5). arg(a6).
arg(a7). arg(a8). arg(a9). arg(a10). arg(a11). arg(a12).
arg(a13). arg(a14). arg(a15). arg(a16).

% Levels
level(a1,1). level(a2,1). level(a3,1). level(a4,1). level(a5,1). level(a6,1).
level(a7,2). level(a8,2). level(a9,2). level(a10,2). level(a11,2). level(a12,2).
level(a13,3). level(a14,3). level(a15,3). level(a16,3).

% Strong attacks
strong(a2,a1). strong(a9,a8). strong(a14,a13). strong(a15,a16).
strong(a1,a14). strong(a16,a15). strong(a1,a3). strong(a1,a4).
strong(a13,a7). strong(a13,a10). strong(a3,a5). strong(a5,a3).

% Weak attacks
weak(a8,a2). weak(a13,a9). weak(a8,a5). weak(a8,a6).
weak(a16,a11). weak(a16,a12). weak(a2,a7). weak(a10,a13).

% Successful attacks
succ(A,B) :- strong(A,B).
succ(A,B) :- weak(A,B), level(A,LA), level(B,LB), LA > LB.

% Choice of extension
{ in_extension(A) : arg(A) }.

% Conflict‑free constraint
:- in_extension(A), in_extension(B), succ(A,B).

% Self‑defending constraint
:- in_extension(A), succ(B,A), not in_extension(B), #count{C : in_extension(C), succ(C,B)} = 0.

% Conflict with existing extension (for adding new argument)
conflict_with_existing(D) :- succ(D,X), in_extension(X).
conflict_with_existing(D) :- succ(X,D), in_extension(X).
conflict_with_existing(D) :- succ(D,D).

% Bad attacker for candidate D
bad_attacker(D,B) :- succ(B,D), not in_extension(B), not succ(D,B), #count{C : in_extension(C), succ(C,B)} = 0.

% D is defended when added if no bad attacker exists
defended_when_added(D) :- arg(D), not bad_attacker(D,_).

% Possible to add D while preserving admissibility
possible_add(D) :- arg(D), not in_extension(D), not conflict_with_existing(D), defended_when_added(D).

% Maximality: no possible addition
:- possible_add(_).

#show in_extension/1.