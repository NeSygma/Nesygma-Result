% Define the domain
job(1..4).
machine(1..4).
operation(J, O) :- job(J), O = 1..max_operations(J).
max_operations(1, 3).
max_operations(2, 4).
max_operations(3, 3).
max_operations(4, 4).

% Job data
% Job 1: Due 20, Penalty Weight 3, 3 operations
duration(1, 1, 4). machine_req(1, 1, 1).
duration(1, 2, 5). machine_req(1, 2, 3). master_req(1, 2).
duration(1, 3, 3). machine_req(1, 3, 2).
due_date(1, 20). penalty_weight(1, 3).

% Job 2: Due 25, Penalty Weight 1, 4 operations
duration(2, 1, 6). machine_req(2, 1, 2).
duration(2, 2, 4). machine_req(2, 2, 4).
duration(2, 3, 2). machine_req(2, 3, 1).
duration(2, 4, 3). machine_req(2, 4, 3).
due_date(2, 25). penalty_weight(2, 1).

% Job 3: Due 22, Penalty Weight 2, 3 operations
duration(3, 1, 7). machine_req(3, 1, 4). master_req(3, 1).
duration(3, 2, 6). machine_req(3, 2, 1).
duration(3, 3, 2). machine_req(3, 3, 3).
due_date(3, 22). penalty_weight(3, 2).

% Job 4: Due 30, Penalty Weight 1, 4 operations
duration(4, 1, 2). machine_req(4, 1, 3).
duration(4, 2, 5). machine_req(4, 2, 2).
duration(4, 3, 3). machine_req(4, 3, 4).
duration(4, 4, 4). machine_req(4, 4, 1). master_req(4, 4).
due_date(4, 30). penalty_weight(4, 1).

% Machine maintenance windows
maintenance(2, 10, 11).
maintenance(4, 15, 16).

% Time horizon
time(0..40).

% Choice rules for assignments
{ start(J, O, T) : time(T) } 1 :- operation(J, O).
{ assigned(J, O, M) : machine(M) } 1 :- operation(J, O).

% Precedence constraints: operations in a job must be sequential
:- operation(J, O), operation(J, O+1), 
   start(J, O, T1), start(J, O+1, T2), T2 < T1 + duration(J, O, D).

% Calculate finish times
finish(J, O, T) :- start(J, O, T), duration(J, O, D), T + D = Tf, Tf = T.
finish(J, O, Tf) :- start(J, O, T), duration(J, O, D), Tf = T + D.

% Job completion time (last operation finish time)
job_finish(J, Tf) :- operation(J, O), 
                   finish(J, O, Tf), 
                   not operation(J, O+1).

% Machine exclusivity: no two operations on same machine at overlapping times
:- assigned(J1, O1, M), assigned(J2, O2, M), J1 != J2,
   start(J1, O1, S1), finish(J1, O1, F1),
   start(J2, O2, S2), finish(J2, O2, F2),
   time(T), S1 <= T, T < F1, S2 <= T, T < F2.

% Master operator exclusivity: at most one master-required operation at a time
:- master_req(J1, O1), master_req(J2, O2), J1 != J2,
   start(J1, O1, S1), finish(J1, O1, F1),
   start(J2, O2, S2), finish(J2, O2, F2),
   time(T), S1 <= T, T < F1, S2 <= T, T < F2.

% Maintenance windows: no operations during maintenance
:- assigned(J, O, M), maintenance(M, Start, End),
   start(J, O, S), finish(J, O, F),
   S < End, Start < F.

% Non-preemptive: operations run to completion (enforced by finish time calculation)

% Calculate tardiness and weighted penalty
tardy(J, T) :- job_finish(J, T), due_date(J, D), T > D, Diff = T - D.
tardy(J, 0) :- job_finish(J, T), due_date(J, D), T <= D.
weighted_penalty(J, P) :- tardy(J, Diff), penalty_weight(J, W), P = Diff * W.

% Total penalty
total_penalty(P) :- P = #sum{ WP : operation(J, _), weighted_penalty(J, WP) }.

% Makespan (maximum finish time)
makespan(M) :- M = #max{ T : operation(J, O), finish(J, O, T) }.

% Total cost
total_cost(C) :- makespan(M), total_penalty(P), C = M + P.

% Objective: minimize total cost
#minimize{ C : total_cost(C) }.

% Show the solution
#show start/3.
#show assigned/3.
#show makespan/1.
#show total_penalty/1.
#show total_cost/1.
#show job_finish/2.