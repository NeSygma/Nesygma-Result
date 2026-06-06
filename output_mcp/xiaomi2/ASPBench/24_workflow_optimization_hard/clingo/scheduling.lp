% Domains
task(0..9).
machine(1..3).
time(0..40).

% Task durations
duration(0, 4).
duration(1, 3).
duration(2, 5).
duration(3, 2).
duration(4, 6).
duration(5, 3).
duration(6, 4).
duration(7, 5).
duration(8, 2).
duration(9, 3).

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
eligible(9, 2).
eligible(9, 3).

% Prerequisites
prereq(3, 0).
prereq(4, 1).
prereq(5, 3).
prereq(6, 2).
prereq(6, 4).
prereq(7, 4).
prereq(8, 5).
prereq(9, 7).
prereq(9, 8).

% Decision: assign each task to exactly one eligible machine
1 { assign(T, M) : eligible(T, M) } 1 :- task(T).

% Decision: assign each task a start time
1 { start(T, S) : time(S) } 1 :- task(T).

% End time is start + duration
end(T, E) :- start(T, S), duration(T, D), E = S + D.

% Precedence constraint: task cannot start until all prerequisites complete
:- start(T, S), prereq(T, P), end(P, E), S < E.

% No overlap on same machine: for any two tasks on same machine, 
% one must finish before the other starts
:- assign(T1, M), assign(T2, M), T1 < T2, 
   start(T1, S1), end(T1, E1), start(T2, S2), end(T2, E2),
   S2 < E1.

% Makespan is the maximum end time
makespan(MS) :- MS = #max { E : end(_, E) }.

% Minimize makespan
#minimize { MS : makespan(MS) }.

% Output
#show assign/2.
#show start/2.
#show end/2.
#show makespan/1.