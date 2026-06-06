%% Problem: Schedule 10 tasks with precedence constraints and machine assignments
%% Objective: Minimize makespan

%% --- Domain Definitions ---

% Tasks 0-9
task(0..9).

% Machines 1,2,3
machine(1..3).

% Time horizon - we need enough time. Expected optimal makespan is 17.
% Let's set a reasonable upper bound. Sum of all durations = 4+3+5+2+6+3+4+5+2+3 = 37
% But with parallelism, makespan should be much less. Let's use 30 as upper bound.
time(0..30).

%% --- Task Properties ---

% duration(task, duration)
duration(0,4).
duration(1,3).
duration(2,5).
duration(3,2).
duration(4,6).
duration(5,3).
duration(6,4).
duration(7,5).
duration(8,2).
duration(9,3).

% eligible(task, machine)
eligible(0,1).
eligible(1,2).
eligible(2,3).
eligible(3,1).
eligible(4,2).
eligible(5,1).
eligible(6,3).
eligible(7,2).
eligible(8,1).
eligible(9,2).
eligible(9,3).

% prerequisite(task, prereq)
prereq(3,0).
prereq(4,1).
prereq(5,3).
prereq(6,2).
prereq(6,4).
prereq(7,4).
prereq(8,5).
prereq(9,7).
prereq(9,8).

%% --- Decision Variables ---

% Each task is assigned to exactly one eligible machine
1 { assign(T, M) : eligible(T, M) } 1 :- task(T).

% Each task starts at exactly one time
1 { start(T, S) : time(S) } 1 :- task(T).

% Completion time of task T
end(T, E) :- task(T), start(T, S), duration(T, D), E = S + D.

%% --- Constraints ---

% 1. Machine capacity: A machine can only execute one task at a time
% Two tasks on the same machine cannot overlap
:- assign(T1, M), assign(T2, M), T1 != T2,
   start(T1, S1), duration(T1, D1),
   start(T2, S2), duration(T2, D2),
   S1 < S2, S2 < S1 + D1.

% 2. Precedence: Task cannot start until all prerequisites complete
:- prereq(T, P), start(T, S), end(P, E), S < E.

% 3. All tasks must be scheduled (implicitly enforced by choice rules)

%% --- Objective: Minimize makespan ---

% Makespan is the maximum end time across all tasks
makespan(M) :- M = #max { E, T : end(T, E) }.

% Minimize makespan
#minimize { M@1 : makespan(M) }.

%% --- Output ---

#show assign/2.
#show start/2.
#show end/2.
#show makespan/1.