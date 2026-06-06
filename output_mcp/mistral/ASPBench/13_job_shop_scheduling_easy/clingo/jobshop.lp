% --- Instance Data ---
% Jobs and operations
job(1..3).
operation(1..3).

% Durations: duration(Job, Operation, Duration)
duration(1, 1, 3). duration(1, 2, 2). duration(1, 3, 4).
duration(2, 1, 2). duration(2, 2, 5). duration(2, 3, 1).
duration(3, 1, 4). duration(3, 2, 1). duration(3, 3, 3).

% Machine requirements: machine(Job, Operation, Machine)
machine(1, 1, 1). machine(1, 2, 2). machine(1, 3, 3).
machine(2, 1, 2). machine(2, 2, 1). machine(2, 3, 3).
machine(3, 1, 3). machine(3, 2, 1). machine(3, 3, 2).

% Precedence constraints within each job
% For each job, operation 1 must precede operation 2, which must precede operation 3
precedes(J, 1, 2) :- job(J).
precedes(J, 2, 3) :- job(J).

% --- Time Horizon ---
% Set a reasonable time horizon based on the expected makespan
time(0..12).

% --- Choice Rules ---
% Assign a start time to each operation
{ start_time(J, O, T) : time(T) } = 1 :- job(J), operation(O).

% Assign a machine to each operation (deterministic from data)
assigned_machine(J, O, M) :- machine(J, O, M), job(J), operation(O).

% --- Constraints ---

% 1. Precedence constraints: If op1 precedes op2 in job J, then op2 must start after op1 ends
:- precedes(J, O1, O2), 
   start_time(J, O1, T1), 
   start_time(J, O2, T2), 
   T2 < T1 + duration(J, O1, _).

% 2. Machine exclusivity: No two operations can use the same machine at the same time
:- assigned_machine(J1, O1, M), assigned_machine(J2, O2, M),
   J1 != J2, O1 != O2,
   start_time(J1, O1, T1), start_time(J2, O2, T2),
   T1 < T2 + duration(J2, O2, _),
   T2 < T1 + duration(J1, O1, _).

% 3. End time calculation: end_time = start_time + duration
end_time(J, O, T) :- start_time(J, O, S), duration(J, O, D), T = S + D, time(T).

% 4. Makespan is the maximum end time across all operations
makespan(T) :- T = #max { E : end_time(_, _, E) }.

% --- Objective: Minimize makespan ---
#minimize { T : makespan(T) }.

% --- Output ---
#show start_time/3.
#show assigned_machine/3.
#show makespan/1.