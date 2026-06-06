% --- Available Drugs ---
drug(cardio_ease; metformax; anxio_calm; pain_off; glucopain; hydro_stress; renal_guard; pain_plus).

% Drug - Condition mapping
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

% Drug costs
cost(cardio_ease, 50).
cost(metformax, 40).
cost(anxio_calm, 70).
cost(pain_off, 60).
cost(glucopain, 110).
cost(hydro_stress, 90).
cost(renal_guard, 120).
cost(pain_plus, 80).

% Drug toxicity values
toxicity(cardio_ease, 20).
toxicity(metformax, 25).
toxicity(anxio_calm, 30).
toxicity(pain_off, 15).
toxicity(glucopain, 40).
toxicity(hydro_stress, 35).
toxicity(renal_guard, 10).
toxicity(pain_plus, 25).

% Maximum doses
max_dose(cardio_ease, 100).
max_dose(metformax, 1000).
max_dose(anxio_calm, 50).
max_dose(pain_off, 400).
max_dose(glucopain, 600).
max_dose(hydro_stress, 200).
max_dose(renal_guard, 150).
max_dose(pain_plus, 300).

% --- Patient Profile ---
patient_condition(hypertension; diabetes; anxiety; pain).
patient_contraindication(renal_failure).
patient_genetic_marker(g6pd_deficiency).

% --- Drug Contraindications ---
% Standard contraindications
contraindication(renal_guard, renal_failure, standard).
% Genetic contraindications
contraindication(glucopain, g6pd_deficiency, genetic).

% --- Drug Interactions ---
% metformax interacts with pain_plus (reduced_efficacy, moderate)
interaction(metformax, pain_plus, moderate, reduced_efficacy).

% hydro_stress has severe interaction with metformax IF patient has diabetes
% Since patient HAS diabetes, this severe interaction is active
severe_interaction_active(hydro_stress, metformax) :- patient_condition(diabetes).
severe_interaction_active(metformax, hydro_stress) :- patient_condition(diabetes).

% Synergy (positive interaction, not a prohibition)
synergy(pain_plus, anxio_calm, anxiety, 2).

% --- Constraints ---
max_drugs(4).
max_budget(250).
max_toxicity_threshold(100).

% Choose which drugs to prescribe
{ prescribed(D) } :- drug(D).

% Constraint 1: At most 4 drugs
:- #count { D : prescribed(D) } > M, max_drugs(M).

% Constraint 2: Budget constraint
total_cost(C) :- C = #sum { Co, D : prescribed(D), cost(D, Co) }.
:- total_cost(C), max_budget(B), C > B.

% Constraint 3: Toxicity constraint
total_toxicity(T) :- T = #sum { Tox, D : prescribed(D), toxicity(D, Tox) }.
:- total_toxicity(T), max_toxicity_threshold(Mxt), T > Mxt.

% Constraint 4: Standard contraindications
:- prescribed(D), contraindication(D, C, standard), patient_contraindication(C).

% Constraint 5: Genetic contraindications
:- prescribed(D), contraindication(D, G, genetic), patient_genetic_marker(G).

% Constraint 7: Severe interaction prohibition
:- prescribed(D1), prescribed(D2), severe_interaction_active(D1, D2).

% Constraint 8: All conditions must be treated
treated(C) :- prescribed(D), treats(D, C).
:- patient_condition(C), not treated(C).

% --- Objective: Minimize total cost ---
#minimize { Co, D : prescribed(D), cost(D, Co) }.

% --- Output ---

% Prescribed drugs (with dose = 1, since dose does not affect constraints)
prescribed_drug(D, 1) :- prescribed(D).

% Treated conditions
treated_condition(C) :- treated(C).

% Untreated conditions (should be empty for optimal solution)
untreated_condition(C) :- patient_condition(C), not treated(C).

% Interactions detected between prescribed drugs (sorted alphabetically via D1 < D2)
interaction_detected(D1, D2, Type, Effect) :-
    prescribed(D1), prescribed(D2), D1 < D2,
    interaction(D1, D2, Type, Effect).

% Contraindications avoided (patient contraindications respected)
contraindication_avoided(C) :- patient_contraindication(C).

% Genetic markers respected
genetic_marker_respected(G) :- patient_genetic_marker(G).

#show prescribed_drug/2.
#show treated_condition/1.
#show untreated_condition/1.
#show total_cost/1.
#show total_toxicity/1.
#show interaction_detected/4.
#show contraindication_avoided/1.
#show genetic_marker_respected/1.