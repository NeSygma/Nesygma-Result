%%% DOMAIN DEFINITIONS %%%
job(1..4).
machine(1..4).
time(0..40).

%%% JOBS AND OPERATIONS %%%
% Operations per job
job_op(1,1). job_op(1,2). job_op(1,3).
job_op(2,1). job_op(2,2). job_op(2,3). job_op(2,4).
job_op(3,1). job_op(3,2). job_op(3,3).
job_op(4,1). job_op(4,2). job_op(4,3). job_op(4,4).

% Durations
duration(1,1,4). duration(1,2,5). duration(1,3,3).
duration(2,1,6). duration(2,2,4). duration(2,3,2). duration(2,4,3).
duration(3,1,7). duration(3,2,6). duration(3,3,2).
duration(4,1,2). duration(4,2,5). duration(4,3,3). duration(4,4,4).

% Machine assignments
op_machine(1,1,1). op_machine(1,2,3). op_machine(1,3,2).
op_machine(2,1,2). op_machine(2,2,4). op_machine(2,3,1). op_machine(2,4,3).
op_machine(3,1,4). op_machine(3,2,1). op_machine(3,3,3).
op_machine(4,1,3). op_machine(4,2,2). op_machine(4,3,4). op_machine(4,4,1).

% Master operator requirement
op_master(1,2).
op_master(3,1).
op_master(4,4).

%%% DUE DATES & PENALTY WEIGHTS %%%
job_due(1,20). job_due(2,25). job_due(3,22). job_due(4,30).
job_penalty_weight(1,3). job_penalty_weight(2,1). job_penalty_weight(3,2). job_penalty_weight(4,1).

%%% DECISION VARIABLES: Start times %%%
% Each operation gets exactly one start time
1 { start(J,O,T) : time(T) } 1 :- job_op(J,O).

% Start time + duration must not exceed time horizon
:- start(J,O,T), duration(J,O,D), T + D > 40.

%%% CONSTRAINT 1: Precedence within job %%%
% Operation O must finish before operation O+1 starts
:- job_op(J,O1), job_op(J,O2), O2 = O1 + 1,
   start(J,O1,T1), duration(J,O1,D1),
   start(J,O2,T2),
   T1 + D1 > T2.

%%% CONSTRAINT 2: Machine exclusivity %%%
% Two different operations cannot run on the same machine at overlapping times
:- start(J1,O1,T1), duration(J1,O1,D1),
   start(J2,O2,T2), duration(J2,O2,D2),
   op_machine(J1,O1,M), op_machine(J2,O2,M),
   (J1,O1) != (J2,O2),
   T1 < T2 + D2, T2 < T1 + D1.

%%% CONSTRAINT 3: Master Operator exclusivity %%%
% At most one master-operator operation at any time
:- op_master(J1,O1), op_master(J2,O2),
   start(J1,O1,T1), duration(J1,O1,D1),
   start(J2,O2,T2), duration(J2,O2,D2),
   (J1,O1) != (J2,O2),
   T1 < T2 + D2, T2 < T1 + D1.

%%% CONSTRAINT 4: Maintenance windows %%%
% Machine 2 unavailable from time 10 to 11 inclusive
:- start(J,O,T), duration(J,O,D), op_machine(J,O,2),
   T <= 11, T + D - 1 >= 10.

% Machine 4 unavailable from time 15 to 16 inclusive
:- start(J,O,T), duration(J,O,D), op_machine(J,O,4),
   T <= 16, T + D - 1 >= 15.

%%% CONSTRAINT 5: Non-preemptive is implicit (single start time) %%%

%%% METRICS COMPUTATION %%%
% End time of each operation
op_end(J,O,E) :- start(J,O,T), duration(J,O,D), E = T + D.

% Completion time of each job (max end time of its operations)
job_end(J,C) :- job(J), C = #max { E : job_op(J,O), op_end(J,O,E) }.

% Tardiness per job (weighted)
tardiness(J,Tr) :- job_end(J,C), job_due(J,D), job_penalty_weight(J,W),
                   C > D, Tr = (C - D) * W.
tardiness(J,0) :- job_end(J,C), job_due(J,D), C <= D.

% Total weighted tardiness penalty
total_penalty(P) :- P = #sum { Tr,J : tardiness(J,Tr) }.

% Makespan (latest completion time across all operations)
makespan(M) :- M = #max { E : op_end(J,O,E) }.

% Total cost = makespan + total penalty
total_cost(C) :- makespan(M), total_penalty(P), C = M + P.

%%% OPTIMIZATION %%%
#minimize { C : total_cost(C) }.

%%% OUTPUT %%%
#show start/3.
#show makespan/1.
#show total_penalty/1.
#show total_cost/1.
#show job_end/2.
#show tardiness/2.