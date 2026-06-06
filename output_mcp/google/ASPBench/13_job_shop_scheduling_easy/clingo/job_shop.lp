% --- Domain ---
job(1..3).
op(1..3).
machine(1..3).
time(0..20).

% --- Instance Data ---
% Job 1
duration(1, 1, 3). machine_req(1, 1, 1).
duration(1, 2, 2). machine_req(1, 2, 2).
duration(1, 3, 4). machine_req(1, 3, 3).
% Job 2
duration(2, 1, 2). machine_req(2, 1, 2).
duration(2, 2, 5). machine_req(2, 2, 1).
duration(2, 3, 1). machine_req(2, 3, 3).
% Job 3
duration(3, 1, 4). machine_req(3, 1, 3).
duration(3, 2, 1). machine_req(3, 2, 1).
duration(3, 3, 3). machine_req(3, 3, 2).

% Precedence
precedence(J, 1, 2) :- job(J).
precedence(J, 2, 3) :- job(J).

% --- Logic ---
% 1. Choice Rule: Assign start time to each operation
1 { start(J, O, T) : time(T) } 1 :- job(J), op(O).

% 2. Precedence Constraint
:- precedence(J, O1, O2), start(J, O1, T1), start(J, O2, T2), duration(J, O1, D1), T2 < T1 + D1.

% 3. Resource Constraint (No overlap on same machine)
:- machine_req(J1, O1, M), machine_req(J2, O2, M), 
   start(J1, O1, T1), start(J2, O2, T2), 
   duration(J1, O1, D1), duration(J2, O2, D2),
   (J1, O1) != (J2, O2),
   T1 <= T2, T2 < T1 + D1.

% 4. Makespan Calculation
end(J, O, T + D) :- start(J, O, T), duration(J, O, D).
makespan(M) :- M = #max { T + D : start(J, O, T), duration(J, O, D) }.

% 5. Optimization
#minimize { M : makespan(M) }.

% --- Output ---
#show start/3.
#show makespan/1.