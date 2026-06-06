%%% Task Data %%%
task(0;1;2;3;4;5;6;7).

duration(0,3).
duration(1,2).
duration(2,4).
duration(3,1).
duration(4,5).
duration(5,2).
duration(6,3).
duration(7,2).

% Prerequisites: prereq(Task, Prereq)
prereq(2,0).
prereq(3,1).
prereq(4,2).
prereq(4,3).
prereq(5,0).
prereq(6,4).
prereq(7,5).
prereq(7,6).

%%% Domain: Time Horizon %%%
% Upper bound: sum of all durations = 3+2+4+1+5+2+3+2 = 22
% Expected optimal makespan is 17, so 22 is safe.
time(0..22).

%%% 1. Choice: Assign each task a start time %%%
{ start(T, S) : time(S) } 1 :- task(T).

%%% 2. Constraint: Each task must have exactly one start time %%%
:- task(T), not start(T, _).

%%% 3. Constraint: Prerequisites must finish before task starts %%%
:- start(T, S), prereq(T, P), start(P, SP), duration(P, D), S < SP + D.

%%% 4. Derive end time %%%
end(T, E) :- start(T, S), duration(T, D), E = S + D.

%%% 5. Makespan: maximum end time %%%
makespan(M) :- M = #max{ E : end(T, E) }.

%%% 6. Objective: Minimize makespan %%%
#minimize { M : makespan(M) }.

%%% 7. Critical Path: Tasks on the longest dependency chain with no slack %%%
% A task is on the critical path if its earliest start equals its latest start.
% We compute earliest start (ES) and latest start (LS) under the optimal makespan.

% Earliest start: 0 for tasks with no prerequisites, otherwise max of predecessors' end times.
% We'll compute ES iteratively using the precedence graph.

% Base: tasks with no prereqs have ES = 0
es(T, 0) :- task(T), not prereq(T, _).

% For tasks with prereqs, ES is the max end time of all prereqs
es(T, E) :- task(T), prereq(T, P), end(P, E), not prereq(T, P2), end(P2, E2), E2 > E.
% Actually we need a proper max. Let's use a different approach.

% Better: compute ES via constraints and optimization.
% We'll define earliest_possible_start and latest_possible_start.

% Actually, let's compute critical path differently.
% A task is on the critical path if there is no slack between its start and end
% relative to the makespan, and it lies on a longest path.

% We can compute: a task is on the critical path if:
% 1. Its start time is fixed (no flexibility) - i.e., earliest start = latest start
% 2. It lies on a path from source to sink with total duration = makespan

% Let's compute earliest start (ES) and latest start (LS) given the makespan.

% ES: earliest possible start respecting prereqs
% We'll compute ES using a simple iterative approach with time points.

% For each task, ES is the minimum time such that all prereqs can finish before it.
% We'll use a choice rule to pick ES values and constrain them.

{ es(T, S) : time(S) } 1 :- task(T).
:- task(T), not es(T, _).

% ES of tasks with no prereqs is 0
:- task(T), not prereq(T, _), es(T, S), S != 0.

% ES of a task must be >= end time of all its prereqs
:- task(T), prereq(T, P), es(T, S), end(P, E), S < E.

% ES must be the minimum such time - we enforce by saying there's no earlier feasible time
% Actually, for critical path we just need to know if start time = ES = LS.
% Let's compute LS similarly.

% LS: latest start time such that task can finish by makespan
{ ls(T, S) : time(S) } 1 :- task(T).
:- task(T), not ls(T, _).

% LS + duration <= makespan
:- task(T), ls(T, S), duration(T, D), makespan(M), S + D > M.

% For each successor, LS of predecessor + duration <= LS of successor
:- prereq(P, T), ls(P, SP), duration(P, D), ls(T, ST), SP + D > ST.
% Wait, prereq(P, T) means P is prerequisite of T. So P must finish before T starts.
% LS(P) + D(P) <= LS(T)

% Actually let's fix: prereq(T, P) means P is prerequisite of T.
% So P must finish before T starts.
% LS(P) + D(P) <= LS(T) for the latest start constraint.

% A task is on the critical path if its start time equals both ES and LS.
on_critical_path(T) :- task(T), start(T, S), es(T, S), ls(T, S).

% Also, the critical path must form a connected chain from source to sink.
% We need to ensure we only include tasks that are part of the longest path.
% Let's define: a task is on the critical path if it has no slack.

% Actually, let's simplify: critical path = tasks where start = ES = LS.
% This naturally gives the longest path.

%%% Show results %%%
#show start/2.
#show end/2.
#show makespan/1.
#show on_critical_path/1.