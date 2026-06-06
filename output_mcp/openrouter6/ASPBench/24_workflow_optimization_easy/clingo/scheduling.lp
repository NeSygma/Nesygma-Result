% Scheduling 8 tasks with precedence constraints to minimize makespan

% Define tasks and their durations
task(0). duration(0, 3).
task(1). duration(1, 2).
task(2). duration(2, 4).
task(3). duration(3, 1).
task(4). duration(4, 5).
task(5). duration(5, 2).
task(6). duration(6, 3).
task(7). duration(7, 2).

% Define prerequisites
prereq(2, 0).
prereq(3, 1).
prereq(4, 2).
prereq(4, 3).
prereq(5, 0).
prereq(6, 4).
prereq(7, 5).
prereq(7, 6).

% Time domain: we need enough time for the longest possible schedule
% Upper bound: sum of all durations = 3+2+4+1+5+2+3+2 = 22
time(0..22).

% Start times: each task gets a start time
1 { start(T, S) : time(S) } 1 :- task(T).

% End times: end = start + duration
end(T, E) :- start(T, S), duration(T, D), E = S + D.

% Precedence constraint: task cannot start until all prerequisites are completed
:- start(T, S), prereq(T, P), end(P, E), S < E.

% All tasks must be scheduled (ensured by choice rule above)

% Makespan: maximum end time across all tasks
makespan(M) :- M = #max{ E : end(T, E) }.

% Minimize makespan
#minimize { M : makespan(M) }.

% Critical path identification:
% A task is on the critical path if its start time equals the maximum end time of its prerequisites
% For tasks with no prerequisites, they are on critical path if they start at time 0
% OR if they are the last task(s) that determine the makespan

% Helper: maximum end time of prerequisites for each task
max_prereq_end(T, MaxE) :- task(T), MaxE = #max{ E : prereq(T, P), end(P, E) }.
max_prereq_end(T, 0) :- task(T), not prereq(T, _). % No prerequisites: max end is 0

% Task is on critical path if it starts exactly when its prerequisites finish (no slack)
% OR if it's the last task(s) that achieve the makespan
critical_task(T) :- start(T, S), max_prereq_end(T, S). % No slack
critical_task(T) :- end(T, E), makespan(M), E = M. % Last task(s)

% For tasks with no prerequisites, they are critical if they start at 0
critical_task(T) :- task(T), not prereq(T, _), start(T, 0).

% Build critical path sequence: order by end time
% First, compute position based on count of earlier critical tasks
pos(T, P) :- critical_task(T), 
             P = 1 + #count{ U : critical_task(U), end(U, EU), end(T, ET), EU < ET }.

% Show directives for output
#show task/1.
#show duration/2.
#show prereq/2.
#show start/2.
#show end/2.
#show makespan/1.
#show critical_task/1.
#show pos/2.