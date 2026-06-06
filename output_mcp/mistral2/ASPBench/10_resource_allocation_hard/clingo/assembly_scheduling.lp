% --- DOMAINS ---
time(0..15).  % Time horizon (0 to 15)

% --- FACTS ---
% Tasks: task(T;D;S;M;DL)
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

% Workers: worker(W;C;Skills)
worker(w1, 15, "welding", "inspection").
worker(w2, 12, "assembly", "inspection").
worker(w3, 20, "programming", "assembly").
worker(w4, 18, "welding", "programming").
worker(w5, 16, "assembly", "inspection", "welding").

% Machines: machine(M;T;C)
machine(m1, a, 3).
machine(m2, b, 2).
machine(m3, c, 4).

% Precedence: precedes(A,B)
precedes(t1, t3).
precedes(t1, t4).
precedes(t2, t5).
precedes(t2, t6).
precedes(t3, t7).
precedes(t4, t9).
precedes(t5, t8).
precedes(t6, t10).
precedes(t7, t12).
precedes(t8, t11).

% Helper: has_skill(W,S)
has_skill(W, S) :-
    worker(W, _, S1, S2),
    (S = S1 ; S = S2).

has_skill(W, S) :-
    worker(W, _, S1, S2, S3),
    (S = S1 ; S = S2 ; S = S3).

% --- CHOICE RULES ---
% Assign each task to exactly one worker, one machine, and a start time.
1 { assigned(T, W, M, S) : worker(W), machine(M), time(S) } 1 :-
    task(T, _, _, _, _).

% --- CONSTRAINTS ---

% Skill compatibility: Task T can only be assigned to worker W if W has the required skill.
:- assigned(T, W, _, _),
   task(T, _, S, _, _),
   not has_skill(W, S).

% Machine type compatibility: Task T can only be assigned to machine M of the required type.
:- assigned(T, _, M, _),
   task(T, _, _, MT, _),
   machine(M, MT2, _),
   MT != MT2.

% Worker capacity: At any time S, a worker W can work on at most 3 tasks.
:- time(S),
   worker(W, _, _, _),
   #count{T : assigned(T, W, _, S)} > 3.

:- time(S),
   worker(W, _, _, _, _),
   #count{T : assigned(T, W, _, S)} > 3.

% Machine capacity: At any time S, a machine M can be used for at most 2 tasks.
:- time(S),
   machine(M, _, _),
   #count{T : assigned(T, _, M, S)} > 2.

% Precedence: If precedes(A,B), then A must finish before B starts.
:- precedes(A, B),
   assigned(A, _, _, SA),
   assigned(B, _, _, SB),
   SA + task(A, D, _, _, _) > SB.

% Deadlines: Each task must finish by its deadline.
:- assigned(T, _, _, S),
   task(T, D, _, _, DL),
   S + D > DL.

% Budget: Total cost <= 470.
% Cost for task T: (worker_cost(W) + machine_cost(M)) * duration(T)
:- #sum{ (WC + MC) * D, T : assigned(T, W, M, _), task(T, D, _, _, _), worker(W, WC, _, _), machine(M, _, MC) } > 470.

:- #sum{ (WC + MC) * D, T : assigned(T, W, M, _), task(T, D, _, _, _), worker(W, WC, _, _, _), machine(M, _, MC) } > 470.

% --- FLUENTS ---
% working(W,T,S): Worker W is working on task T at time S.
working(W, T, S) :-
    assigned(T, W, _, S1),
    task(T, D, _, _, _),
    time(S),
    S >= S1,
    S < S1 + D.

% using(M,T,S): Machine M is being used for task T at time S.
using(M, T, S) :-
    assigned(T, _, M, S1),
    task(T, D, _, _, _),
    time(S),
    S >= S1,
    S < S1 + D.

% --- MAKESPAN ---
% makespan(F): The makespan is F if the last task finishes at F.
makespan(F) :-
    F = #max{ S + D : assigned(T, _, _, S), task(T, D, _, _, _) }.

% --- TOTAL COST ---
total_cost(C) :-
    C = #sum{ (WC + MC) * D, T : assigned(T, W, M, _), task(T, D, _, _, _), worker(W, WC, _, _, _), machine(M, _, MC) }.

% --- FEASIBILITY ---
feasible :-
    makespan(_),
    total_cost(C),
    C <= 470.

% --- OUTPUT ---
#show assigned/4.
#show makespan/1.
#show total_cost/1.
#show feasible/0.