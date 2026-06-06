% Define tasks
task(0;1;2;3;4;5;6;7;8;9;10;11).

% Task attributes: task_attr(ID, Category, Value, Compute, Bandwidth, Storage, Specialists)
task_attr(0, research, 40, 20, 10, 30, 5).
task_attr(1, research, 60, 30, 25, 20, 10).
task_attr(2, research, 70, 25, 20, 15, 5).
task_attr(3, research, 55, 20, 15, 25, 10).
task_attr(4, development, 80, 40, 30, 20, 20).
task_attr(5, development, 90, 35, 25, 30, 15).
task_attr(6, development, 75, 30, 40, 25, 18).
task_attr(7, development, 85, 45, 35, 15, 22).
task_attr(8, deployment, 65, 15, 20, 40, 8).
task_attr(9, deployment, 80, 20, 30, 35, 12).
task_attr(10, deployment, 70, 25, 25, 30, 10).
task_attr(11, deployment, 95, 30, 35, 45, 15).

% Categories
category(research; development; deployment).

% Resource capacities
capacity(compute, 150).
capacity(bandwidth, 120).
capacity(storage, 140).
capacity(specialists, 60).

% --- Task Selection (0-1 knapsack) ---
{ selected(T) } :- task(T).

% --- Prerequisite: Task 4 requires Task 0 ---
:- selected(4), not selected(0).

% --- Mutual Exclusion: Task 1 and Task 7 cannot both be selected ---
:- selected(1), selected(7).

% --- Resource Usage (Base costs) ---
total_compute(Total) :- Total = #sum { C, T : selected(T), task_attr(T, _, _, C, _, _, _) }.
total_bandwidth(Total) :- Total = #sum { B, T : selected(T), task_attr(T, _, _, _, B, _, _) }.
total_storage(Total) :- Total = #sum { S, T : selected(T), task_attr(T, _, _, _, _, S, _) }.
total_specialists_base(Total) :- Total = #sum { Sp, T : selected(T), task_attr(T, _, _, _, _, _, Sp) }.

% --- Conditional Specialist Cost ---
% dev_selected is true if at least one Development task is selected
dev_selected :- selected(T), task_attr(T, development, _, _, _, _, _).

% Extra specialist cost: 5 per selected Deployment task if any Development task is selected
extra_specialist_cost(Total) :- 
    dev_selected,
    Total = #sum { 5, T : selected(T), task_attr(T, deployment, _, _, _, _, _) }.
extra_specialist_cost(0) :- not dev_selected.

% Total specialists = base + conditional extra
total_specialists(Total) :- 
    total_specialists_base(Base),
    extra_specialist_cost(Extra),
    Total = Base + Extra.

% --- Resource Constraints ---
:- total_compute(C), capacity(compute, Cap), C > Cap.
:- total_bandwidth(B), capacity(bandwidth, Cap), B > Cap.
:- total_storage(S), capacity(storage, Cap), S > Cap.
:- total_specialists(Sp), capacity(specialists, Cap), Sp > Cap.

% --- Diversity Bonus ---
has_category(Cat) :- selected(T), task_attr(T, Cat, _, _, _, _, _).
diversity_bonus :- has_category(research), has_category(development), has_category(deployment).

% --- Total Value ---
total_base_value(Total) :- Total = #sum { V, T : selected(T), task_attr(T, _, V, _, _, _, _) }.
total_value(Total) :- total_base_value(Base), diversity_bonus, Total = Base + 100.
total_value(Total) :- total_base_value(Base), not diversity_bonus, Total = Base.

% --- Optimization: Maximize total value ---
#maximize { V : total_value(V) }.

% --- Output ---
#show selected/1.
#show total_value/1.
#show diversity_bonus/0.
#show total_compute/1.
#show total_bandwidth/1.
#show total_storage/1.
#show total_specialists/1.