% --- Declare the domain of tasks ---
task(0..7).

% --- Task durations ---
duration(0, 3).
duration(1, 2).
duration(2, 4).
duration(3, 1).
duration(4, 5).
duration(5, 2).
duration(6, 3).
duration(7, 2).

% --- Prerequisites ---
prerequisite(2, 0).
prerequisite(3, 1).
prerequisite(4, 2).
prerequisite(4, 3).
prerequisite(5, 0).
prerequisite(6, 4).
prerequisite(7, 5).
prerequisite(7, 6).

% --- Time horizon: 0 to a sufficiently large upper bound (e.g., 100) ---
time(0..100).

% --- Choice rule: Assign a start time to each task ---
{ start_time(T, S) : time(S) } 1 :- task(T).

% --- End time is start time + duration ---
end_time(T, E) :- start_time(T, S), duration(T, D), E = S + D.

% --- Prerequisite constraint: A task can only start after all its prerequisites have finished ---
:- prerequisite(T, P), start_time(T, S), end_time(P, E), S < E.

% --- All tasks must be scheduled (ensured by the choice rule) ---

% --- Makespan: Maximum end time across all tasks ---
makespan(M) :- M = #max { E : end_time(_, E) }.

% --- Critical path: Longest dependency chain ---
% Compute the longest path from each task to the end
critical_path_length(T, L) :- task(T), duration(T, D), not prerequisite(T, _), L = D.
critical_path_length(T, L) :- task(T), prerequisite(T, P), critical_path_length(P, L1), duration(T, D), L = L1 + D.

% The critical path consists of tasks where critical_path_length(T, L) equals the makespan
critical_path(T) :- task(T), critical_path_length(T, L), makespan(M), L = M.

% --- Show the required output ---
#show start_time/2.
#show end_time/2.
#show makespan/1.
#show critical_path/1.