% --- Instance Data ---
job(1..3).
operation(J, 1..3) :- job(J).

% Durations and machine requirements
duration(1, 1, 3). machine_req(1, 1, 1).
duration(1, 2, 2). machine_req(1, 2, 2).
duration(1, 3, 4). machine_req(1, 3, 3).

duration(2, 1, 2). machine_req(2, 1, 2).
duration(2, 2, 5). machine_req(2, 2, 1).
duration(2, 3, 1). machine_req(2, 3, 3).

duration(3, 1, 4). machine_req(3, 1, 3).
duration(3, 2, 1). machine_req(3, 2, 1).
duration(3, 3, 3). machine_req(3, 3, 2).

% --- Time Horizon ---
max_time(12).
time(0..T) :- max_time(T).

% --- Choice Rule: Assign start times to operations ---
{ start_time(J, O, T) : time(T) } 1 :- operation(J, O).

% --- Derive end times ---
end_time(J, O, T + D) :- start_time(J, O, T), duration(J, O, D).

% --- Precedence Constraints ---
:- start_time(J, O, T), operation(J, O), O > 1,
   start_time(J, O-1, T2), T < T2 + duration(J, O-1, D).

% --- Resource Constraints: No two operations on the same machine at the same time ---
:- start_time(J1, O1, T1), start_time(J2, O2, T2), J1 != J2,
   machine_req(J1, O1, M), machine_req(J2, O2, M),
   T1 < T2 + duration(J2, O2, D), T2 < T1 + duration(J1, O1, D).

% --- Makespan: Maximum end time ---
makespan(T) :- end_time(_, _, T), not makespan(T+1).

% --- Objective: Minimize makespan ---
#minimize { T : makespan(T) }.

% --- Output ---
schedule(J, O, M, T, D) :- start_time(J, O, T), duration(J, O, D), machine_req(J, O, M).
#show schedule/5.
#show makespan/1.