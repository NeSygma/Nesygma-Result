% Scheduling Problem - Robotic Assembly Lab
% 12 tasks, 5 workers, 3 machines

% ==================== DOMAIN DEFINITIONS ====================
% Time horizon: 0 to 20 (sufficient for makespan ≤ 9)
time(0..20).

% Tasks with their properties
task(t1). task(t2). task(t3). task(t4). task(t5). task(t6).
task(t7). task(t8). task(t9). task(t10). task(t11). task(t12).

% Task durations
duration(t1, 2). duration(t2, 3). duration(t3, 1). duration(t4, 2).
duration(t5, 3). duration(t6, 2). duration(t7, 1). duration(t8, 2).
duration(t9, 3). duration(t10, 2). duration(t11, 1). duration(t12, 2).

% Task required skills
skill(t1, welding). skill(t2, assembly). skill(t3, inspection). skill(t4, welding).
skill(t5, assembly). skill(t6, programming). skill(t7, inspection). skill(t8, assembly).
skill(t9, welding). skill(t10, programming). skill(t11, assembly). skill(t12, inspection).

% Task required machine types
machine_type(t1, a). machine_type(t2, b). machine_type(t3, a). machine_type(t4, a).
machine_type(t5, c). machine_type(t6, b). machine_type(t7, a). machine_type(t8, c).
machine_type(t9, a). machine_type(t10, b). machine_type(t11, c). machine_type(t12, a).

% Task deadlines
deadline(t1, 6). deadline(t2, 8). deadline(t3, 7). deadline(t4, 9).
deadline(t5, 10). deadline(t6, 9). deadline(t7, 8). deadline(t8, 11).
deadline(t9, 12). deadline(t10, 11). deadline(t11, 10). deadline(t12, 13).

% Workers with their skills and hourly costs
worker(w1). worker(w2). worker(w3). worker(w4). worker(w5).

% Worker skills
has_skill(w1, welding). has_skill(w1, inspection).
has_skill(w2, assembly). has_skill(w2, inspection).
has_skill(w3, programming). has_skill(w3, assembly).
has_skill(w4, welding). has_skill(w4, programming).
has_skill(w5, assembly). has_skill(w5, inspection). has_skill(w5, welding).

% Worker hourly costs
worker_cost(w1, 15). worker_cost(w2, 12). worker_cost(w3, 20). worker_cost(w4, 18). worker_cost(w5, 16).

% Machines with their types and hourly costs
machine(m1). machine(m2). machine(m3).

% Machine types
machine_type_id(m1, a). machine_type_id(m2, b). machine_type_id(m3, c).

% Machine hourly costs
machine_cost(m1, 3). machine_cost(m2, 2). machine_cost(m3, 4).

% ==================== TASK ASSIGNMENTS ====================
% Each task must be assigned to exactly one worker and one machine
1 { assigned_worker(T, W) : worker(W) } 1 :- task(T).
1 { assigned_machine(T, M) : machine(M) } 1 :- task(T).

% Skill compatibility: task can only be assigned to worker with required skill
:- assigned_worker(T, W), skill(T, S), not has_skill(W, S).

% Machine type compatibility: task can only be assigned to machine of required type
:- assigned_machine(T, M), machine_type(T, MT), not machine_type_id(M, MT).

% ==================== SCHEDULING ====================
% Start time for each task (integer time)
1 { start(T, S) : time(S) } 1 :- task(T).

% Finish time calculation
finish(T, F) :- task(T), start(T, S), duration(T, D), F = S + D.

% ==================== PRECEDENCE CONSTRAINTS ====================
% T1 must complete before T3, T4
:- finish(t1, F1), start(t3, S3), F1 > S3.
:- finish(t1, F1), start(t4, S4), F1 > S4.

% T2 must complete before T5, T6
:- finish(t2, F2), start(t5, S5), F2 > S5.
:- finish(t2, F2), start(t6, S6), F2 > S6.

% T3 must complete before T7
:- finish(t3, F3), start(t7, S7), F3 > S7.

% T4 must complete before T9
:- finish(t4, F4), start(t9, S9), F4 > S9.

% T5 must complete before T8
:- finish(t5, F5), start(t8, S8), F5 > S8.

% T6 must complete before T10
:- finish(t6, F6), start(t10, S10), F6 > S10.

% T7 must complete before T12
:- finish(t7, F7), start(t12, S12), F7 > S12.

% T8 must complete before T11
:- finish(t8, F8), start(t11, S11), F8 > S11.

% ==================== CAPACITY CONSTRAINTS ====================
% Worker capacity: at most 3 simultaneous tasks per worker
% For each worker and time point, count tasks that overlap with that time
:- worker(W), time(T), 
   #count{ T1 : assigned_worker(T1, W), start(T1, S1), duration(T1, D1), 
           S1 <= T, T < S1 + D1 } > 3.

% Machine capacity: at most 2 simultaneous tasks per machine
:- machine(M), time(T),
   #count{ T1 : assigned_machine(T1, M), start(T1, S1), duration(T1, D1),
           S1 <= T, T < S1 + D1 } > 2.

% ==================== DEADLINE CONSTRAINTS ====================
% Each task must finish by its deadline
:- task(T), finish(T, F), deadline(T, D), F > D.

% ==================== COST CALCULATION ====================
% Calculate cost per task: (worker_hourly_cost + machine_hourly_cost) * duration
task_cost(T, C) :- task(T), 
                   assigned_worker(T, W), worker_cost(W, WC),
                   assigned_machine(T, M), machine_cost(M, MC),
                   duration(T, D),
                   C = (WC + MC) * D.

% Total cost calculation
total_cost(Total) :- Total = #sum{ C, T : task_cost(T, C) }.

% Budget constraint: total cost ≤ 470
:- total_cost(Total), Total > 470.

% ==================== OBJECTIVE: MINIMIZE MAKESPAN ====================
% Makespan is the maximum finish time across all tasks
makespan(M) :- M = #max{ F, T : finish(T, F) }.

% ==================== OUTPUT ====================
% Show the schedule
#show assigned_worker/2.
#show assigned_machine/2.
#show start/2.
#show finish/2.
#show makespan/1.
#show total_cost/1.
#show task_cost/2.

% Also show task assignments for clarity
#show schedule/4 : assigned_worker(T, W), assigned_machine(T, M), start(T, S), duration(T, D).