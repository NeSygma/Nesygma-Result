% Task definitions
% Categories: research (0-3), development (4-7), deployment (8-11)
task(0;1;2;3;4;5;6;7;8;9;10;11).

category(0, research). category(1, research). category(2, research). category(3, research).
category(4, development). category(5, development). category(6, development). category(7, development).
category(8, deployment). category(9, deployment). category(10, deployment). category(11, deployment).

value(0,40). value(1,60). value(2,70). value(3,55).
value(4,80). value(5,90). value(6,75). value(7,85).
value(8,65). value(9,80). value(10,70). value(11,95).

compute(0,20). compute(1,30). compute(2,25). compute(3,20).
compute(4,40). compute(5,35). compute(6,30). compute(7,45).
compute(8,15). compute(9,20). compute(10,25). compute(11,30).

bandwidth(0,10). bandwidth(1,25). bandwidth(2,20). bandwidth(3,15).
bandwidth(4,30). bandwidth(5,25). bandwidth(6,40). bandwidth(7,35).
bandwidth(8,20). bandwidth(9,30). bandwidth(10,25). bandwidth(11,35).

storage(0,30). storage(1,20). storage(2,15). storage(3,25).
storage(4,20). storage(5,30). storage(6,25). storage(7,15).
storage(8,40). storage(9,35). storage(10,30). storage(11,45).

specialists(0,5). specialists(1,10). specialists(2,5). specialists(3,10).
specialists(4,20). specialists(5,15). specialists(6,18). specialists(7,22).
specialists(8,8). specialists(9,12). specialists(10,10). specialists(11,15).

% Resource capacities
resource(compute, 150).
resource(bandwidth, 120).
resource(storage, 140).
resource(specialists, 60).

% Choice rule for task selection
{selected(T)} :- task(T).

% Prerequisite: Task 4 requires Task 0
:- selected(4), not selected(0).

% Mutual exclusion: Task 1 and Task 7 cannot both be selected
:- selected(1), selected(7).

% Calculate resource usage
used_compute(C) :- C = #sum{Comp : selected(T), compute(T, Comp)}.
used_bandwidth(B) :- B = #sum{Band : selected(T), bandwidth(T, Band)}.
used_storage(S) :- S = #sum{Stor : selected(T), storage(T, Stor)}.

% Calculate specialists usage with conditional cost
% Base cost + 5 for each selected deployment task if any development task is selected
base_specialists(S) :- S = #sum{Spc : selected(T), specialists(T, Spc)}.

% Check if any development task is selected
has_development_task :- selected(T), category(T, development).

% Count selected deployment tasks
selected_deployment_count(N) :- N = #count{T : selected(T), category(T, deployment)}.

% Calculate conditional cost
conditional_cost(C) :- has_development_task, selected_deployment_count(N), C = N * 5.
conditional_cost(0) :- not has_development_task.

% Total specialists usage
used_specialists(TotalSp) :- base_specialists(Base), conditional_cost(Cond), TotalSp = Base + Cond.

% Resource capacity constraints
:- used_compute(C), resource(compute, Cap), C > Cap.
:- used_bandwidth(B), resource(bandwidth, Cap), B > Cap.
:- used_storage(S), resource(storage, Cap), S > Cap.
:- used_specialists(Sp), resource(specialists, Cap), Sp > Cap.

% Calculate base value
base_value(V) :- V = #sum{Val : selected(T), value(T, Val)}.

% Check if all three categories are represented
has_research :- selected(T), category(T, research).
has_development :- selected(T), category(T, development).
has_deployment :- selected(T), category(T, deployment).
bonus_applied :- has_research, has_development, has_deployment.

% Total value
total_value(V) :- base_value(B), bonus_applied, V = B + 100.
total_value(V) :- base_value(V), not bonus_applied.

% Maximize total value
#maximize { V : total_value(V) }.

% Show the solution
#show selected/1.
#show total_value/1.
#show bonus_applied/0.
#show used_compute/1.
#show used_bandwidth/1.
#show used_storage/1.
#show used_specialists/1.