% --- Facts ---
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

capacity(compute, 150).
capacity(bandwidth, 120).
capacity(storage, 140).
capacity(specialists, 60).

prerequisite(4, 0).
mutual_exclusion(1, 7).

% --- Helper predicates ---
category(ID, C) :- task(ID, C, _, _, _, _, _).

% --- Choice rule ---
{ selected(ID) : task(ID, _, _, _, _, _, _) }.

% --- Constraints ---
% Prerequisite: Task 4 requires Task 0
:- selected(4), not selected(0).

% Mutual exclusion: Task 1 and Task 7 cannot both be selected
:- selected(1), selected(7).

% Resource limits
:- capacity(compute, C), #sum { Compute, ID : task(ID, _, _, Compute, _, _, _), selected(ID) } > C.
:- capacity(bandwidth, B), #sum { Bandwidth, ID : task(ID, _, _, _, Bandwidth, _, _), selected(ID) } > B.
:- capacity(storage, S), #sum { Storage, ID : task(ID, _, _, _, _, Storage, _), selected(ID) } > S.
:- capacity(specialists, Sp),
   BaseSpecialists = #sum { BaseSp, ID : task(ID, _, _, _, _, _, BaseSp), selected(ID) },
   ConditionalSpecialists = #count { ID : selected(ID), category(ID, deployment) } * ConditionalFactor,
   TotalSpecialists = BaseSpecialists + ConditionalSpecialists,
   TotalSpecialists > Sp.

% Conditional factor: 5 if at least one development task is selected, else 0
development_selected :- selected(ID), category(ID, development).
conditional_factor(5) :- development_selected.
conditional_factor(0) :- not development_selected.

% --- Diversity bonus ---
research_selected :- selected(ID), category(ID, research).
development_selected :- selected(ID), category(ID, development).
deployment_selected :- selected(ID), category(ID, deployment).
diversity_bonus :- research_selected, development_selected, deployment_selected.

% --- Total value ---
base_value(Value) :- Value = #sum { V, ID : task(ID, _, V, _, _, _, _), selected(ID) }.
bonus(Value) :- diversity_bonus, Value = 100.
bonus(0) :- not diversity_bonus.
total_value(Value) :- Value = base_value(Base) + bonus(Bonus).

% --- Optimization ---
#maximize { TotalValue : total_value(TotalValue) }.

% --- Output ---
#show selected/1.
#show total_value/1.
#show diversity_bonus/0.
% Show resource usage components for downstream synthesis
compute_used(C) :- C = #sum { Compute, ID : task(ID, _, _, Compute, _, _, _), selected(ID) }.
bandwidth_used(B) :- B = #sum { Bandwidth, ID : task(ID, _, _, _, Bandwidth, _, _), selected(ID) }.
storage_used(S) :- S = #sum { Storage, ID : task(ID, _, _, _, _, Storage, _), selected(ID) }.
specialists_used(Sp) :-
    BaseSp = #sum { BaseSp, ID : task(ID, _, _, _, _, _, BaseSp), selected(ID) },
    CondFactor = ConditionalFactor,
    ConditionalSp = #count { ID : selected(ID), category(ID, deployment) } * CondFactor,
    Sp = BaseSp + ConditionalSp.
#show compute_used/1.
#show bandwidth_used/1.
#show storage_used/1.
#show specialists_used/1.