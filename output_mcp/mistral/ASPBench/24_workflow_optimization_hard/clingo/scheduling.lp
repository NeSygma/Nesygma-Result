% Define the time horizon
max_time(20).
time(0..T) :- max_time(T).

% Task and machine definitions
% Tasks 0-9
task(0). task(1). task(2). task(3). task(4).
task(5). task(6). task(7). task(8). task(9).

% Machines 1-3
machine(1). machine(2). machine(3).

% Task durations
duration(0,4). duration(1,3). duration(2,5). duration(3,2). duration(4,6).
duration(5,3). duration(6,4). duration(7,5). duration(8,2). duration(9,3).

% Eligible machines for each task
eligible(0,1).
eligible(1,2).
eligible(2,3).
eligible(3,1).
eligible(4,2).
eligible(5,1).
eligible(6,3).
eligible(7,2).
eligible(8,1).
eligible(9,2). eligible(9,3).

% Prerequisites (task T requires prerequisite P)
prerequisite(3,0).
prerequisite(4,1).
prerequisite(5,3).
prerequisite(6,2). prerequisite(6,4).
prerequisite(7,4).
prerequisite(8,5).
prerequisite(9,7). prerequisite(9,8).

% Choice rule: Assign each task to exactly one eligible machine
1 { assignment(T,M) : eligible(T,M) } 1 :- task(T).

% Choice rule: Assign each task a start time
1 { start_time(T,Ts) : time(Ts) } 1 :- task(T).

% Calculate end time for each task
end_time(T, Es) :- start_time(T, S), duration(T, D), Es = S + D, time(Es).

% Precedence constraints: Task T cannot start until all its prerequisites are completed
:- prerequisite(T,P), end_time(P, E), start_time(T, S), S < E.

% Machine exclusivity: No two tasks on the same machine can overlap
:- assignment(T1,M), assignment(T2,M), T1 != T2,
   start_time(T1,S1), end_time(T1,E1),
   start_time(T2,S2), end_time(T2,E2),
   S1 < E2, S2 < E1.

% Calculate makespan (maximum end time)
makespan(M) :- M = #max { E : task(T), end_time(T,E) }.

% Critical path: Find the longest path in the precedence DAG
% We'll compute the longest path to each task
path_length(T, 0) :- task(T), not prerequisite(T,_).
path_length(T, L) :- prerequisite(T,P), path_length(P, L1), L = L1 + duration(P), task(T).

% The critical path is the path with maximum total duration
critical_path_length(L) :- L = #max { L1 : task(T), path_length(T,L1) }.

% Show the schedule
#show assignment/2.
#show start_time/2.
#show end_time/2.
#show makespan/1.
#show critical_path_length/1.

% Optional: Show critical path as a sequence
% This is complex in ASP, so we'll just show the length for now
% A full sequence would require additional modeling with choice rules
% and is beyond the scope of this core scheduling model.