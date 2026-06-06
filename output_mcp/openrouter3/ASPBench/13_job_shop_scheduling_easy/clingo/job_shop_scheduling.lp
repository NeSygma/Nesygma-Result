% Job Shop Scheduling Problem

% Domain declarations
job(1). job(2). job(3).
operation(1..3).  % Operations 1, 2, 3 for each job
machine(1..3).    % Machines m1, m2, m3

% Instance data: durations
duration(1, 1, 3).  % j1o1: duration 3
duration(1, 2, 2).  % j1o2: duration 2
duration(1, 3, 4).  % j1o3: duration 4
duration(2, 1, 2).  % j2o1: duration 2
duration(2, 2, 5).  % j2o2: duration 5
duration(2, 3, 1).  % j2o3: duration 1
duration(3, 1, 4).  % j3o1: duration 4
duration(3, 2, 1).  % j3o2: duration 1
duration(3, 3, 3).  % j3o3: duration 3

% Instance data: machine requirements
requires(1, 1, 1).  % j1o1 requires m1
requires(1, 2, 2).  % j1o2 requires m2
requires(1, 3, 3).  % j1o3 requires m3
requires(2, 1, 2).  % j2o1 requires m2
requires(2, 2, 1).  % j2o2 requires m1
requires(2, 3, 3).  % j2o3 requires m3
requires(3, 1, 3).  % j3o1 requires m3
requires(3, 2, 1).  % j3o2 requires m1
requires(3, 3, 2).  % j3o3 requires m2

% Precedence relationships within each job
precedence(1, 1, 2).  % j1o1 before j1o2
precedence(1, 2, 3).  % j1o2 before j1o3
precedence(2, 1, 2).  % j2o1 before j2o2
precedence(2, 2, 3).  % j2o2 before j2o3
precedence(3, 1, 2).  % j3o1 before j3o2
precedence(3, 2, 3).  % j3o2 before j3o3

% Time horizon - estimate based on total work
% Total work: 3+2+4 + 2+5+1 + 4+1+3 = 25
% With 3 machines, makespan should be around 11-12
time(0..20).  % Sufficient horizon

% Decision variables: start times for each operation
% Each operation must start at some time
{ start(J, O, T) : time(T) } 1 :- operation(J, O).

% Calculate end times
end(J, O, T + D) :- start(J, O, T), duration(J, O, D).

% Precedence constraints: operation O2 must start after O1 finishes
:- precedence(J, O1, O2), start(J, O1, T1), end(J, O1, E1), start(J, O2, T2), T2 < E1.

% Machine capacity constraints: no two operations on same machine at same time
% For any two different operations on same machine, they cannot overlap
% We need to ensure we don't compare an operation with itself
:- requires(J1, O1, M), requires(J2, O2, M), 
   start(J1, O1, S1), end(J1, O1, E1),
   start(J2, O2, S2), end(J2, O2, E2),
   (J1 != J2; O1 != O2),  % Different operations
   S1 < E2, S2 < E1.  % Overlap condition

% Calculate makespan as maximum end time
makespan(T) :- T = #max{ E, J, O : end(J, O, E) }.

% Minimize makespan
#minimize { T@1 : makespan(T) }.

% Show relevant information
#show job/1.
#show operation/1.
#show machine/1.
#show duration/3.
#show requires/3.
#show start/3.
#show end/3.
#show makespan/1.