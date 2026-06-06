% --- Data ---
task(0..7).

duration(0,3). duration(1,2). duration(2,4). duration(3,1).
duration(4,5). duration(5,2). duration(6,3). duration(7,2).

prereq(2,0). prereq(3,1). prereq(4,2). prereq(4,3).
prereq(5,0). prereq(6,4). prereq(7,5). prereq(7,6).

% --- Time Horizon ---
time(0..20).

% --- Scheduling: each task gets exactly one start time ---
1 { start(T, S) : time(S) } 1 :- task(T).

% End time = start + duration
end_time(T, E) :- start(T, S), duration(T, D), E = S + D.

% Precedence: B cannot start until all its prerequisites A have finished
:- prereq(B, A), start(B, SB), start(A, SA), duration(A, DA), SB < SA + DA.

% --- Makespan ---
makespan(M) :- M = #max { E : end_time(_, E) }.

% Minimize makespan
#minimize { M@0 : makespan(M) }.

% --- Critical Path (zero-slack chain) ---
% Successor relationship
succ(A, B) :- prereq(B, A).

% Root: no prerequisites
root(T) :- task(T), not prereq(T, _).
% Leaf: no successors
leaf(T) :- task(T), not succ(T, _).

% Zero-slack edge: A ends exactly when B starts
zedge(A, B) :- prereq(B, A), end_time(A, EA), start(B, SB), EA = SB.

% Reachable from root via zero-slack edges
from_root(T) :- root(T).
from_root(B) :- from_root(A), zedge(A, B).

% Can reach leaf via zero-slack edges
to_leaf(T) :- leaf(T).
to_leaf(A) :- to_leaf(B), zedge(A, B).

% Critical task: on a zero-slack path from root to leaf
on_critical(T) :- from_root(T), to_leaf(T).

% --- Output ---
#show start/2.
#show end_time/2.
#show makespan/1.
#show on_critical/1.