% Job Shop Scheduling Problem - Minimize Makespan
% 3 jobs, 3 operations each, 3 machines

% ============ DOMAINS ============
job(1). job(2). job(3).
op(1). op(2). op(3).
machine(m1). machine(m2). machine(m3).

% ============ INSTANCE DATA ============
% Operation identifiers: j1o1, j1o2, etc.
operation(j1o1). operation(j1o2). operation(j1o3).
operation(j2o1). operation(j2o2). operation(j2o3).
operation(j3o1). operation(j3o2). operation(j3o3).

% Duration of each operation
duration(j1o1, 3). duration(j1o2, 2). duration(j1o3, 4).
duration(j2o1, 2). duration(j2o2, 5). duration(j2o3, 1).
duration(j3o1, 4). duration(j3o2, 1). duration(j3o3, 3).

% Machine requirements
requires(j1o1, m1). requires(j1o2, m2). requires(j1o3, m3).
requires(j2o1, m2). requires(j2o2, m1). requires(j2o3, m3).
requires(j3o1, m3). requires(j3o2, m1). requires(j3o3, m2).

% Precedence within jobs
precedes(j1o1, j1o2). precedes(j1o2, j1o3).
precedes(j2o1, j2o2). precedes(j2o2, j2o3).
precedes(j3o1, j3o2). precedes(j3o2, j3o3).

% ============ TIME HORIZON ============
% Upper bound: sum of all durations = 3+2+4+2+5+1+4+1+3 = 25
% We'll use 0..25 as time points
time(0..25).

% ============ DECISION VARIABLES ============
% Start time for each operation
1 { start(O, T) : time(T) } 1 :- operation(O).

% ============ DERIVED PREDICATES ============
% End time = start + duration
end(O, T+D) :- start(O, T), duration(O, D).

% ============ CONSTRAINTS ============

% 1. Precedence: if A precedes B, then A must finish before B starts
:- precedes(A, B), start(A, TA), start(B, TB), end(A, EA), TB < EA.

% 2. Machine capacity: operations on same machine cannot overlap
% Two operations on same machine: either A finishes before B starts, or B finishes before A start
:- requires(A, M), requires(B, M), A != B,
   start(A, SA), start(B, SB), end(A, EA), end(B, EB),
   SB < EA, SA < EB.

% ============ OBJECTIVE ============
% Makespan is the maximum end time
makespan(M) :- M = #max { E : end(O, E) }.

% Minimize makespan
#minimize { M : makespan(M) }.

% ============ OUTPUT ============
#show start/2.
#show makespan/1.