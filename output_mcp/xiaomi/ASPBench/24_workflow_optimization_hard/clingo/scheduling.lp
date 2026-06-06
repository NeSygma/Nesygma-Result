% ==================== DOMAIN FACTS ====================
% Tasks
task(0). task(1). task(2). task(3). task(4).
task(5). task(6). task(7). task(8). task(9).

% Machines
machine(1). machine(2). machine(3).

% Time horizon (0 to 20 is sufficient for optimal makespan of 17)
time(0..20).

% Durations
duration(0, 4). duration(1, 3). duration(2, 5). duration(3, 2).
duration(4, 6). duration(5, 3). duration(6, 4). duration(7, 5).
duration(8, 2). duration(9, 3).

% Eligible machines for each task
eligible(0, 1).
eligible(1, 2).
eligible(2, 3).
eligible(3, 1).
eligible(4, 2).
eligible(5, 1).
eligible(6, 3).
eligible(7, 2).
eligible(8, 1).
eligible(9, 2). eligible(9, 3).

% Prerequisites: prereq(Task, Prerequisite)
prereq(3, 0).
prereq(4, 1).
prereq(5, 3).
prereq(6, 2). prereq(6, 4).
prereq(7, 4).
prereq(8, 5).
prereq(9, 7). prereq(9, 8).

% ==================== CHOICE RULES ====================
% Each task must be assigned to exactly one eligible machine
1 { assigned(T, M) : eligible(T, M) } 1 :- task(T).

% Each task must start at exactly one time point
1 { start(T, S) : time(S) } 1 :- task(T).

% ==================== DERIVED PREDICATES ====================
% End time = start time + duration
end(T, E) :- start(T, S), duration(T, D), E = S + D.

% ==================== CONSTRAINTS ====================
% Precedence constraints: task cannot start until all prerequisites complete
:- prereq(T, P), start(T, S1), end(P, E2), S1 < E2.

% Machine non-overlap: tasks on same machine cannot overlap
% Two tasks T1, T2 on same machine M overlap if:
% T1 starts before T2 ends AND T2 starts before T1 ends
:- assigned(T1, M), assigned(T2, M), T1 < T2,
   start(T1, S1), end(T1, E1),
   start(T2, S2), end(T2, E2),
   S1 < E2, S2 < E1.

% ==================== OBJECTIVE ====================
% Makespan is the maximum end time
makespan(MS) :- MS = #max { E : end(_, E) }.

% Minimize makespan
#minimize { MS : makespan(MS) }.

% ==================== OUTPUT ====================
#show assigned/2.
#show start/2.
#show end/2.
#show makespan/1.