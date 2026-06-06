% Task Data
task(0, research, 40, 20, 10, 30, 5).
task(1, research, 60, 30, 25, 20, 10).
task(2, research, 70, 25, 20, 15, 5).
task(3, research, 55, 20, 15, 25, 10).
task(4, development, 80, 40, 30, 20, 20).
task(5, development, 90, 35, 25, 30, 15).
task(6, development, 75, 30, 40, 25, 18).
task(7, development, 85, 45, 35, 15, 22).
task(8, deployment, 65, 15, 20, 40, 8).
task(9, deployment, 80, 20, 30, 35, 12).
task(10, deployment, 70, 25, 25, 30, 10).
task(11, deployment, 95, 30, 35, 45, 15).

% Task Selection
{ selected(ID) } :- task(ID, _, _, _, _, _, _).

% Prerequisite: Task 4 requires Task 0
:- selected(4), not selected(0).

% Mutual Exclusion: Task 1 and Task 7 cannot both be selected
:- selected(1), selected(7).

% Helper: Check if any development task is selected
dev_selected :- selected(ID), task(ID, development, _, _, _, _, _).

% Specialist Cost Calculation
% Base cost for non-deployment tasks
specialist_cost(ID, Cost) :- selected(ID), task(ID, Cat, _, _, _, _, Cost), Cat != deployment.
% Deployment tasks cost base + 5 if dev_selected
specialist_cost(ID, Cost + 5) :- selected(ID), task(ID, deployment, _, _, _, _, Cost), dev_selected.
% Deployment tasks cost base if NOT dev_selected
specialist_cost(ID, Cost) :- selected(ID), task(ID, deployment, _, _, _, _, Cost), not dev_selected.

% Resource Constraints
:- #sum { C, ID : selected(ID), task(ID, _, _, C, _, _, _) } > 150.
:- #sum { B, ID : selected(ID), task(ID, _, _, _, B, _, _) } > 120.
:- #sum { S, ID : selected(ID), task(ID, _, _, _, _, S, _) } > 140.
:- #sum { C, ID : specialist_cost(ID, C) } > 60.

% Diversity Bonus
has_research :- selected(ID), task(ID, research, _, _, _, _, _).
has_development :- selected(ID), task(ID, development, _, _, _, _, _).
has_deployment :- selected(ID), task(ID, deployment, _, _, _, _, _).
bonus_achieved :- has_research, has_development, has_deployment.

% Objective
total_value(V) :- V = V_base + (100 * B), 
                  V_base = #sum { Val, ID : selected(ID), task(ID, _, Val, _, _, _, _) },
                  B = #count { 1 : bonus_achieved }.

#maximize { V : total_value(V) }.

% Output
#show selected/1.
#show total_value/1.
#show bonus_achieved/0.
#show total_compute/1.
#show total_bandwidth/1.
#show total_storage/1.
#show total_specialists/1.

total_compute(C) :- C = #sum { Val, ID : selected(ID), task(ID, _, _, Val, _, _, _) }.
total_bandwidth(B) :- B = #sum { Val, ID : selected(ID), task(ID, _, _, _, Val, _, _) }.
total_storage(S) :- S = #sum { Val, ID : selected(ID), task(ID, _, _, _, _, S, _) }.
total_specialists(S) :- S = #sum { C, ID : specialist_cost(ID, C) }.