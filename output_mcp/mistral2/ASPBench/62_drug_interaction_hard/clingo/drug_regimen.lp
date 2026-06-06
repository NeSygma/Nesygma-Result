% --- Facts: Drugs and their attributes ---
% Drug IDs
drug(cardio_ease).
drug(metformax).
drug(anxio_calm).
drug(pain_off).
drug(glucopain).
drug(hydro_stress).
drug(renal_guard).
drug(pain_plus).

% Drug attributes
% treats(Drug, Condition)
treats(cardio_ease, hypertension).
treats(metformax, diabetes).
treats(anxio_calm, anxiety).
treats(pain_off, pain).
treats(glucopain, diabetes).
treats(glucopain, pain).
treats(hydro_stress, hypertension).
treats(hydro_stress, anxiety).
treats(renal_guard, hypertension).
treats(pain_plus, pain).

% cost(Drug, Cost)
cost(cardio_ease, 50).
cost(metformax, 40).
cost(anxio_calm, 70).
cost(pain_off, 60).
cost(glucopain, 110).
cost(hydro_stress, 90).
cost(renal_guard, 120).
cost(pain_plus, 80).

% toxicity(Drug, Toxicity)
toxicity(cardio_ease, 20).
toxicity(metformax, 25).
toxicity(anxio_calm, 30).
toxicity(pain_off, 15).
toxicity(glucopain, 40).
toxicity(hydro_stress, 35).
toxicity(renal_guard, 10).
toxicity(pain_plus, 25).

% max_dose(Drug, MaxDose)
max_dose(cardio_ease, 100).
max_dose(metformax, 1000).
max_dose(anxio_calm, 50).
max_dose(pain_off, 400).
max_dose(glucopain, 600).
max_dose(hydro_stress, 200).
max_dose(renal_guard, 150).
max_dose(pain_plus, 300).

% contraindicated_with(Drug, Contraindication)
% Use quoted strings for constants that start with uppercase
contraindicated_with(glucopain, "renal_failure").
contraindicated_with(glucopain, "G6PD_deficiency").

% genetic_contraindication(Drug, GeneticMarker)
genetic_contraindication(glucopain, "G6PD_deficiency").

% interacts_with(Drug1, Drug2, InteractionType)
% Reduced efficacy, moderate
interacts_with(metformax, pain_plus, "reduced_efficacy").
% Severe interaction if patient has diabetes
interacts_with(hydro_stress, metformax, "severe").

% synergy_with(Drug1, Drug2)
synergy_with(anxio_calm, pain_plus).

% efficacy_bonus(Drug1, Drug2, Bonus)
efficacy_bonus(anxio_calm, pain_plus, 2).

% --- Patient Profile ---
% Conditions
patient_condition(hypertension).
patient_condition(diabetes).
patient_condition(anxiety).
patient_condition(pain).

% Contraindications
contraindication("renal_failure").

% Genetic markers
genetic_marker("G6PD_deficiency").

% --- Constraints ---
% Max drugs
max_drugs(4).

% Max budget
max_budget(250).

% Max toxicity
max_toxicity(100).

% --- Choice Rule: Prescribe drugs and doses ---
% Dose domain: 0 to max_dose for each drug
1 { prescribed(D, Dose) : dose(D, Dose, MaxDose) } 1 :- drug(D), max_dose(D, MaxDose).

% Dose must be within max_dose
dose(D, Dose, MaxDose) :- max_dose(D, MaxDose), Dose = 0..MaxDose.

% --- Constraints ---
% Drug limit
:- { prescribed(D, _) } > MaxDrugs, max_drugs(MaxDrugs).

% Budget constraint
:- #sum { Cost,Dose : prescribed(D, Dose), cost(D, Cost) } > MaxBudget, max_budget(MaxBudget).

% Toxicity constraint
:- #sum { Tox,Dose : prescribed(D, Dose), toxicity(D, Tox) } > MaxTox, max_toxicity(MaxTox).

% Contraindications: Avoid drugs with contraindications matching patient
:- contraindication(C), prescribed(D, _), contraindicated_with(D, C).

% Genetic contraindications: Avoid drugs with genetic contraindications matching patient
:- genetic_marker(G), prescribed(D, _), genetic_contraindication(D, G).

% Interaction detection and prohibition
% Forbid severe interactions
:- interacts_with(D1, D2, "severe"), prescribed(D1, _), prescribed(D2, _).

% Condition coverage: All patient conditions must be covered
covered(C) :- patient_condition(C), prescribed(D, _), treats(D, C).
:- patient_condition(C), not covered(C).

% --- Safety Analysis ---
% Interactions detected (all interactions, not just severe)
interaction_detected(D1, D2) :- prescribed(D1, _), prescribed(D2, _), interacts_with(D1, D2, _), D1 < D2.

% Contraindications avoided
contraindication_avoided(C) :- contraindication(C), not contraindicated_drug(C).
contraindicated_drug(C) :- contraindication(C), prescribed(D, _), contraindicated_with(D, C).

% Genetic markers respected
genetic_marker_respected(G) :- genetic_marker(G), not genetic_contraindicated_drug(G).
genetic_contraindicated_drug(G) :- genetic_marker(G), prescribed(D, _), genetic_contraindication(D, G).

% --- Objective: Minimize total cost ---
#minimize { Cost*Dose : prescribed(D, Dose), cost(D, Cost) }.

% --- Show directives ---
#show prescribed/2.

% Helper predicates for output
prescribed_drug(D) :- prescribed(D, _).

% Total cost and toxicity as aggregates
% Use helper predicates to avoid unsafe variables in aggregates
total_cost(C) :- C = #sum { Cost*Dose : prescribed(D, Dose), cost(D, Cost) }.
total_toxicity(T) :- T = #sum { Tox*Dose : prescribed(D, Dose), toxicity(D, Tox) }.

% Treated conditions
treated_conditions(C) :- patient_condition(C), covered(C).

% Untreated conditions (should be empty)
untreated_conditions(C) :- patient_condition(C), not covered(C).

% Sort interactions for consistent output
sorted_interaction(D1, D2) :- interaction_detected(D1, D2), D1 < D2.

#show prescribed_drug/1.
#show total_cost/1.
#show total_toxicity/1.
#show treated_conditions/1.
#show untreated_conditions/1.
#show contraindication_avoided/1.
#show genetic_marker_respected/1.
#show sorted_interaction/2.