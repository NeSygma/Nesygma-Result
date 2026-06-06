% --- Domains ---
job(1..4).
operation(J, O) :- job(J), J = 1, O = 1..3.
operation(J, O) :- job(J), J = 2, O = 1..4.
operation(J, O) :- job(J), J = 3, O = 1..3.
operation(J, O) :- job(J), J = 4, O = 1..4.
machine(1..4).
time(0..40).

% --- Job and Operation Data ---
% Duration
duration(1, 1, 4). duration(1, 2, 5). duration(1, 3, 3).
duration(2, 1, 6). duration(2, 2, 4). duration(2, 3, 2). duration(2, 4, 3).
duration(3, 1, 7). duration(3, 2, 6). duration(3, 3, 2).
duration(4, 1, 2). duration(4, 2, 5). duration(4, 3, 3). duration(4, 4, 4).

% Machine assignment
machine_assignment(1, 1, 1). machine_assignment(1, 2, 3). machine_assignment(1, 3, 2).
machine_assignment(2, 1, 2). machine_assignment(2, 2, 4). machine_assignment(2, 3, 1). machine_assignment(2, 4, 3).
machine_assignment(3, 1, 4). machine_assignment(3, 2, 1). machine_assignment(3, 3, 3).
machine_assignment(4, 1, 3). machine_assignment(4, 2, 2). machine_assignment(4, 3, 4). machine_assignment(4, 4, 1).

% Requires master operator
requires_master(1, 2).
requires_master(3, 1).
requires_master(4, 4).

% Due date and penalty weight
due_date(1, 20). due_date(2, 25). due_date(3, 22). due_date(4, 30).
penalty_weight(1, 3). penalty_weight(2, 1). penalty_weight(3, 2). penalty_weight(4, 1).

% Precedence
precedence(J, O1, O2) :- operation(J, O1), operation(J, O2), O1 < O2.

% Maintenance windows
maintenance(2, 10, 11).
maintenance(4, 15, 16).

% --- Choice Rule for Assignments ---
% Assign start times and machines to operations
{ assigned(J, O, M, T) : machine(M), time(T) } 1 :- operation(J, O), machine_assignment(J, O, M).

% --- Precedence Constraints ---
% Ensure operations in a job are scheduled in order
:- precedence(J, O1, O2), assigned(J, O1, M1, T1), assigned(J, O2, M2, T2), T2 < T1 + duration(J, O1, D1).
:- precedence(J, O1, O2), assigned(J, O1, M1, T1), assigned(J, O2, M2, T2), T1 + duration(J, O1, D1) > T2.

% --- Machine Exclusivity ---
% No two operations can be assigned to the same machine at overlapping times
:- assigned(J1, O1, M, T1), assigned(J2, O2, M, T2),
   (J1 < J2 ; (J1 == J2, O1 < O2)),
   not (T1 + duration(J1, O1, D1) <= T2),
   not (T2 + duration(J2, O2, D2) <= T1).

% --- Maintenance Constraints ---
% No operation can be scheduled during maintenance windows
:- assigned(J, O, M, T), maintenance(M, Start, End),
   T < End, T + duration(J, O, D) > Start.

% --- Master Operator Exclusivity ---
% At most one operation requiring the master operator can be in progress at any time
:- requires_master(J1, O1), requires_master(J2, O2),
   (J1 < J2 ; (J1 == J2, O1 < O2)),
   assigned(J1, O1, M1, T1), assigned(J2, O2, M2, T2),
   not (T1 + duration(J1, O1, D1) <= T2),
   not (T2 + duration(J2, O2, D2) <= T1).

% --- Derive Start and Finish Times ---
start_time(J, O, T) :- assigned(J, O, M, T).
finish_time(J, O, T + D) :- start_time(J, O, T), duration(J, O, D).

% --- Makespan ---
makespan(T) :- T = #max { TF : finish_time(_, _, TF) }.

% --- Tardiness and Penalty ---
tardy(J, TF) :- finish_time(J, _, TF), due_date(J, DD), TF > DD.
tardiness_penalty(J, (TF - DD) * W) :- tardy(J, TF), due_date(J, DD), penalty_weight(J, W).
total_penalty(P) :- P = #sum { P1 : tardiness_penalty(_, P1) }.

% --- Total Cost ---
total_cost(C) :- makespan(M), total_penalty(P), C = M + P.

% --- Objective: Minimize Total Cost ---
#minimize { C : total_cost(C) }.

% --- Show Relevant Predicates ---
#show assigned/4.
#show makespan/1.
#show total_penalty/1.
#show total_cost/1.
#show tardy/2.
#show tardiness_penalty/2.