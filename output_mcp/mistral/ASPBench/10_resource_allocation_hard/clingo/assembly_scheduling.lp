% --- DOMAIN DECLARATIONS ---
% Tasks
task(t1; t2; t3; t4; t5; t6; t7; t8; t9; t10; t11; t12).

% Workers
worker(w1; w2; w3; w4; w5).

% Machines
machine(m1; m2; m3).

% Time horizon (0 to 20 should be sufficient)
time(0..20).

% Machine types
machine_type(m1, a).
machine_type(m2, b).
machine_type(m3, c).

% Task properties
% task_duration(Task, Duration)
task_duration(t1, 2).  task_duration(t2, 3).  task_duration(t3, 1).
task_duration(t4, 2).  task_duration(t5, 3).  task_duration(t6, 2).
task_duration(t7, 1).  task_duration(t8, 2).  task_duration(t9, 3).
task_duration(t10, 2). task_duration(t11, 1). task_duration(t12, 2).

% task_required_skill(Task, Skill)
task_required_skill(t1, welding).   task_required_skill(t2, assembly).
task_required_skill(t3, inspection). task_required_skill(t4, welding).
task_required_skill(t5, assembly).   task_required_skill(t6, programming).
task_required_skill(t7, inspection). task_required_skill(t8, assembly).
task_required_skill(t9, welding).    task_required_skill(t10, programming).
task_required_skill(t11, assembly).  task_required_skill(t12, inspection).

% task_required_machine_type(Task, Type)
task_required_machine_type(t1, a).  task_required_machine_type(t2, b).
task_required_machine_type(t3, a).  task_required_machine_type(t4, a).
task_required_machine_type(t5, c).  task_required_machine_type(t6, b).
task_required_machine_type(t7, a).  task_required_machine_type(t8, c).
task_required_machine_type(t9, a).  task_required_machine_type(t10, b).
task_required_machine_type(t11, c). task_required_machine_type(t12, a).

% task_deadline(Task, Deadline)
task_deadline(t1, 6).   task_deadline(t2, 8).   task_deadline(t3, 7).
task_deadline(t4, 9).   task_deadline(t5, 10).  task_deadline(t6, 9).
task_deadline(t7, 8).   task_deadline(t8, 11).  task_deadline(t9, 12).
task_deadline(t10, 11). task_deadline(t11, 10). task_deadline(t12, 13).

% Worker properties
% worker_skill(Worker, Skill)
worker_skill(w1, welding).   worker_skill(w1, inspection).
worker_skill(w2, assembly).  worker_skill(w2, inspection).
worker_skill(w3, programming). worker_skill(w3, assembly).
worker_skill(w4, welding).   worker_skill(w4, programming).
worker_skill(w5, assembly).  worker_skill(w5, inspection). worker_skill(w5, welding).

% worker_hourly_cost(Worker, Cost)
worker_hourly_cost(w1, 15). worker_hourly_cost(w2, 12).
worker_hourly_cost(w3, 20). worker_hourly_cost(w4, 18).
worker_hourly_cost(w5, 16).

% Machine properties
% machine_hourly_cost(Machine, Cost)
machine_hourly_cost(m1, 3). machine_hourly_cost(m2, 2). machine_hourly_cost(m3, 4).

% Precedence dependencies
% precedence_before(TaskA, TaskB) means A must finish before B starts
precedence_before(t1, t3). precedence_before(t1, t4).
precedence_before(t2, t5). precedence_before(t2, t6).
precedence_before(t3, t7).
precedence_before(t4, t9).
precedence_before(t5, t8).
precedence_before(t6, t10).
precedence_before(t7, t12).
precedence_before(t8, t11).

% --- CHOICE RULES ---
% Assign exactly one worker and one machine to each task
{ assigned_worker(Task, Worker) : worker(Worker) } = 1 :- task(Task).
{ assigned_machine(Task, Machine) : machine(Machine) } = 1 :- task(Task).

% Assign a start time to each task
{ start_time(Task, Time) : time(Time) } = 1 :- task(Task).

% --- DERIVED PROPERTIES ---
% Calculate finish time for each task
finish_time(Task, Finish) :-
    task(Task),
    task_duration(Task, Duration),
    start_time(Task, Start),
    Finish = Start + Duration.

% Calculate cost for each task
cost(Task, Cost) :-
    task(Task),
    assigned_worker(Task, Worker),
    assigned_machine(Task, Machine),
    task_duration(Task, Duration),
    worker_hourly_cost(Worker, WCost),
    machine_hourly_cost(Machine, MCost),
    Cost = (WCost + MCost) * Duration.

% Total cost
total_cost(Total) :-
    Total = #sum { Cost : cost(_, Cost) }.

% Makespan (maximum finish time)
makespan(M) :-
    M = #max { Finish : finish_time(_, Finish) }.

% --- CONSTRAINTS ---

% 1. Skill compatibility: assigned worker must have required skill
:- assigned_worker(Task, Worker),
   task_required_skill(Task, Skill),
   not worker_skill(Worker, Skill).

% 2. Machine type compatibility: assigned machine must be of required type
:- assigned_machine(Task, Machine),
   task_required_machine_type(Task, Type),
   not machine_type(Machine, Type).

% 3. Worker capacity: no worker handles more than 3 tasks at any time
% Helper: count tasks assigned to a worker at a given time
worker_load(Worker, Time, Count) :-
    worker(Worker),
    time(Time),
    Count = #count { Task : 
        assigned_worker(Task, Worker),
        start_time(Task, Start),
        Time >= Start,
        Time < Start + task_duration(Task, _) 
    }.

:- worker_load(Worker, Time, Count),
   worker(Worker),
   time(Time),
   Count > 3.

% 4. Machine capacity: no machine handles more than 2 tasks at any time
machine_load(Machine, Time, Count) :-
    machine(Machine),
    time(Time),
    Count = #count { Task : 
        assigned_machine(Task, Machine),
        start_time(Task, Start),
        Time >= Start,
        Time < Start + task_duration(Task, _) 
    }.

:- machine_load(Machine, Time, Count),
   machine(Machine),
   time(Time),
   Count > 2.

% 5. Precedence: if A must finish before B starts, then finish(A) <= start(B)
:- precedence_before(A, B),
   finish_time(A, FinishA),
   start_time(B, StartB),
   FinishA > StartB.

% 6. Deadlines: each task must finish by its deadline
:- finish_time(Task, Finish),
   task_deadline(Task, Deadline),
   Finish > Deadline.

% 7. Budget: total cost must not exceed 470
:- total_cost(Total),
   Total > 470.

% --- OBJECTIVE ---
% Minimize makespan
#minimize { M : makespan(M) }.

% --- OUTPUT ---
#show assigned_worker/2.
#show assigned_machine/2.
#show start_time/2.
#show makespan/1.
#show total_cost/1.

% Define feasible as true if the solver returns a model (all constraints satisfied)
feasible.