% Define the maximum time horizon
max_time(17).

% Time steps (0 to max_time)
time(0..T) :- max_time(T).

% Task definitions: task(ID, Duration)
task(0, 3).
task(1, 2).
task(2, 4).
task(3, 1).
task(4, 5).
task(5, 2).
task(6, 3).
task(7, 2).

% Prerequisites: prereq(Task, Prerequisite)
prereq(2, 0).
prereq(3, 1).
prereq(4, 2).
prereq(4, 3).
prereq(5, 0).
prereq(6, 4).
prereq(7, 5).
prereq(7, 6).

% Assign exactly one start time to each task
{ start_time(T, S) : time(S) } = 1 :- task(T, _).

% Calculate end times: end_time = start_time + duration
end_time(T, S + D) :- start_time(T, S), task(T, D).

% Precedence constraint: all prerequisites must be completed before task starts
:- start_time(T, S), prereq(T, P), end_time(P, E), S < E.

% Calculate makespan as the maximum end time across all tasks
makespan(M) :- M = #max { E : end_time(_, E) }.

% Minimize the makespan (lower values are better)
#minimize { M : makespan(M) }.

% Show the schedule components
#show start_time/2.
#show end_time/2.
#show makespan/1.