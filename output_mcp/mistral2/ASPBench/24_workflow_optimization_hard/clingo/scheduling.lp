% --- DOMAINS ---
task(0..9).
machine(1..3).

% --- INPUT DATA ---
duration(0,4). duration(1,3). duration(2,5). duration(3,2). duration(4,6).
duration(5,3). duration(6,4). duration(7,5). duration(8,2). duration(9,3).

eligible(0,1). eligible(3,1). eligible(5,1). eligible(8,1).
eligible(1,2). eligible(4,2). eligible(7,2). eligible(9,2).
eligible(2,3). eligible(6,3). eligible(9,3).

prereq(3,0). prereq(4,1). prereq(5,3). prereq(6,2). prereq(6,4).
prereq(7,4). prereq(8,5). prereq(9,7). prereq(9,8).

% --- TIME HORIZON ---
time(0..50).

% --- ASSIGNMENT ---
% Assign each task to exactly one eligible machine
1 { assigned(T, M) : eligible(T, M) } 1 :- task(T).

% --- START AND END TIMES ---
% Define start and end times for each task
start_time(T, S) :- assigned(T, M), time(S), S >= 0.
end_time(T, E) :- start_time(T, S), duration(T, D), E = S + D, time(E).

% --- PRECEDENCE CONSTRAINTS ---
% A task cannot start until all its prerequisites are completed
:- assigned(T, M), prereq(T, P), start_time(T, S), end_time(P, E), S < E.

% --- MACHINE EXCLUSIVITY ---
% No two tasks on the same machine can overlap
:- assigned(T1, M), assigned(T2, M), T1 != T2,
   start_time(T1, S1), end_time(T1, E1),
   start_time(T2, S2), end_time(T2, E2),
   not (E1 =< S2), not (E2 =< S1).

% --- MAKESPAN ---
% The makespan is the maximum end time across all tasks
makespan(MK) :- MK = #max { E : end_time(_, E) }.

% --- CRITICAL PATH ---
% A task is on the critical path if it ends at the makespan
critical_path(T) :- task(T), makespan(MK), end_time(T, MK).

% --- OPTIMIZATION ---
% Minimize the makespan
#minimize { MK : makespan(MK) }.

% --- OUTPUT ---
#show assigned/2.
#show start_time/2.
#show end_time/2.
#show makespan/1.
#show critical_path/1.