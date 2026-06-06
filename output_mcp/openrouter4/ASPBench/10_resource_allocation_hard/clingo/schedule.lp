% --- Time Horizon ---
time(0..15).

% --- Tasks: task(ID, Duration, Skill, MachineType, Deadline) ---
task(t1, 2, welding, a, 6).
task(t2, 3, assembly, b, 8).
task(t3, 1, inspection, a, 7).
task(t4, 2, welding, a, 9).
task(t5, 3, assembly, c, 10).
task(t6, 2, programming, b, 9).
task(t7, 1, inspection, a, 8).
task(t8, 2, assembly, c, 11).
task(t9, 3, welding, a, 12).
task(t10, 2, programming, b, 11).
task(t11, 1, assembly, c, 10).
task(t12, 2, inspection, a, 13).

% --- Workers ---
worker(w1, 15).
worker_skill(w1, welding). worker_skill(w1, inspection).
worker(w2, 12).
worker_skill(w2, assembly). worker_skill(w2, inspection).
worker(w3, 20).
worker_skill(w3, programming). worker_skill(w3, assembly).
worker(w4, 18).
worker_skill(w4, welding). worker_skill(w4, programming).
worker(w5, 16).
worker_skill(w5, assembly). worker_skill(w5, inspection). worker_skill(w5, welding).

% --- Machines: machine(ID, Type, HourlyCost) ---
machine(m1, a, 3).
machine(m2, b, 2).
machine(m3, c, 4).

% --- Precedence ---
prec(t1, t3). prec(t1, t4).
prec(t2, t5). prec(t2, t6).
prec(t3, t7).
prec(t4, t9).
prec(t5, t8).
prec(t6, t10).
prec(t7, t12).
prec(t8, t11).

% --- Compatibility ---
compatible_worker(T, W) :- task(T, _, Skill, _, _), worker_skill(W, Skill).
compatible_machine(T, M) :- task(T, _, _, MType, _), machine(M, MType, _).
compatible(T, W, M) :- compatible_worker(T, W), compatible_machine(T, M).

% --- Assignment Choice: exactly one (worker, machine, start) per task ---
1 { assign(T, W, M, S) : compatible(T, W, M), time(S), task(T, Dur, _, _, DL), S + Dur - 1 <= DL } 1 :- task(T, _, _, _, _).

% --- Worker Capacity: at most 3 simultaneous tasks per worker ---
:- time(T), worker(W, _),
   #count { Task : assign(Task, W, _, S), task(Task, Dur, _, _, _), S <= T, T <= S + Dur - 1 } > 3.

% --- Machine Capacity: at most 2 simultaneous tasks per machine ---
:- time(T), machine(M, _, _),
   #count { Task : assign(Task, _, M, S), task(Task, Dur, _, _, _), S <= T, T <= S + Dur - 1 } > 2.

% --- Precedence: A must finish before B starts ---
:- prec(A, B), assign(A, _, _, SA), task(A, DurA, _, _, _), assign(B, _, _, SB), task(B, _, _, _, _), SA + DurA > SB.

% --- Deadline Compliance (redundant safety net) ---
:- assign(T, _, _, S), task(T, Dur, _, _, DL), S + Dur - 1 > DL.

% --- Cost Calculation ---
task_cost(T, C) :- assign(T, W, M, _), task(T, Dur, _, _, _), worker(W, CostW), machine(M, _, CostM), C = (CostW + CostM) * Dur.

total_cost(TC) :- TC = #sum { C, T : task_cost(T, C) }.

:- total_cost(TC), TC > 470.

% --- Makespan ---
finish(T, F) :- assign(T, _, _, S), task(T, Dur, _, _, _), F = S + Dur.
makespan(M) :- M = #max { F : finish(T, F) }.

% --- Minimize makespan ---
#minimize { M@1 : makespan(M) }.

% --- Output ---
#show assign/4.
#show makespan/1.
#show total_cost/1.