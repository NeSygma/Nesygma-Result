% Scheduling Problem with Precedence Constraints
% Tasks 0-7 with durations and prerequisites

% Domain declarations
task(0..7).
time(0..22).  % Upper bound based on total duration sum

% Task durations
duration(0, 3).
duration(1, 2).
duration(2, 4).
duration(3, 1).
duration(4, 5).
duration(5, 2).
duration(6, 3).
duration(7, 2).

% Prerequisite relationships
prerequisite(2, 0).
prerequisite(3, 1).
prerequisite(4, 2).
prerequisite(4, 3).
prerequisite(5, 0).
prerequisite(6, 4).
prerequisite(7, 5).
prerequisite(7, 6).

% Choice rule for start times (each task must have exactly one start time)
{ start_time(T, S) : time(S) } 1 :- task(T).

% End time calculation
end_time(T, E) :- start_time(T, S), duration(T, D), E = S + D.

% Precondition: Task cannot start until all prerequisites are completed
:- start_time(T, S), prerequisite(T, P), end_time(P, E), S < E.

% All tasks must be scheduled (ensured by choice rule with cardinality 1)

% Makespan calculation (maximum end time across all tasks)
makespan(M) :- M = #max{ E : end_time(_, E) }.

% Minimize makespan
#minimize { M : makespan(M) }.

% Critical path identification
% A task is on critical path if its end time equals the makespan
% OR if it's part of a chain where each task's end time equals the next task's start time
% and the chain leads to a task with end time = makespan

% Helper: Task T is on a path to a critical task
path_to_critical(T) :- end_time(T, E), makespan(M), E = M.
path_to_critical(T) :- prerequisite(U, T), path_to_critical(U), 
                       end_time(T, E), start_time(U, S), E = S.

% Critical path tasks
critical_path(T) :- path_to_critical(T).

% Show directives
#show start_time/2.
#show end_time/2.
#show makespan/1.
#show critical_path/1.