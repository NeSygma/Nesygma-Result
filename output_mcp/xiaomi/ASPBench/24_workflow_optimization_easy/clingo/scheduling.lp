% Task definitions
task(0). task(1). task(2). task(3). task(4). task(5). task(6). task(7).

% Durations
duration(0, 3).
duration(1, 2).
duration(2, 4).
duration(3, 1).
duration(4, 5).
duration(5, 2).
duration(6, 3).
duration(7, 2).

% Prerequisites
prereq(2, 0).
prereq(3, 1).
prereq(4, 2).
prereq(4, 3).
prereq(5, 0).
prereq(6, 4).
prereq(7, 5).
prereq(7, 6).

% Time horizon - upper bound for makespan
% Sum of all durations = 3+2+4+1+5+2+3+2 = 22 (sequential upper bound)
% We'll use 0..22 as time points
time(0..22).

% Each task starts at exactly one time point
1 { start(T, S) : time(S) } 1 :- task(T).

% End time is start time plus duration
end(T, S + D) :- start(T, S), duration(T, D).

% Precedence constraint: task cannot start until all prerequisites are completed
:- start(T, S), prereq(T, P), end(P, E), S < E.

% Makespan is the maximum end time
makespan(M) :- M = #max { E : end(_, E) }.

% Minimize makespan
#minimize { M : makespan(M) }.

% Critical path detection
% A task is on the critical path if it has zero slack
% Slack = latest_start - earliest_start
% For critical path: a task T is critical if there exists a path from T to the end
% where the sum of durations equals the remaining time

% Helper: direct dependency edges
dep_edge(P, T) :- prereq(T, P).

% Compute longest path from each task to the end
% longest_to_end(T, L) = duration(T) + max over successors of longest_to_end(successor)
% We need to compute this bottom-up

% Base case: tasks with no successors have longest path = their duration
has_successor(T) :- prereq(_, T).
longest_to_end(T, D) :- task(T), duration(T, D), not has_successor(T).

% Recursive case: for tasks with successors
% We need to find the maximum longest_to_end among successors
% Use a choice to select which successor gives the max
{ select_successor(T, S) : prereq(_, T), prereq(S, T) } 1 :- task(T), has_successor(T).

% The selected successor must have the maximum path
% We need to ensure the selected successor has the longest path
:- select_successor(T, S1), prereq(S2, T), S1 != S2, 
   longest_to_end(S1, L1), longest_to_end(S2, L2), L2 > L1.

% Compute longest path for tasks with successors
longest_to_end(T, D + L) :- select_successor(T, S), duration(T, D), longest_to_end(S, L).

% A task is critical if its longest_to_end equals the makespan
critical(T) :- longest_to_end(T, L), makespan(M), L == M.

% Also mark predecessors on the critical path
critical(P) :- critical(T), prereq(T, P), longest_to_end(P, LP), longest_to_end(T, LT), 
               duration(T, DT), LP == LT + DT.

% Output
#show start/2.
#show end/2.
#show makespan/1.
#show critical/1.