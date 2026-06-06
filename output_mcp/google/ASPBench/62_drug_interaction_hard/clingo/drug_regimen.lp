% --- Data ---
drug(cardio_ease, 50, 20, 100).
drug(metformax, 40, 25, 1000).
drug(anxio_calm, 70, 30, 50).
drug(pain_off, 60, 15, 400).
drug(glucopain, 110, 40, 600).
drug(hydro_stress, 90, 35, 200).
drug(renal_guard, 120, 10, 150).
drug(pain_plus, 80, 25, 300).

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

contraindicated_genetic(glucopain, g6pd_deficiency).
contraindicated_condition(renal_guard, renal_failure).

interaction(metformax, pain_plus, moderate).
interaction(hydro_stress, metformax, severe).

patient_condition(hypertension).
patient_condition(diabetes).
patient_condition(anxiety).
patient_condition(pain).
patient_contraindication(renal_failure).
patient_genetic(g6pd_deficiency).

% --- Logic ---
{ prescribe(D) } :- drug(D, _, _, _).

% 1. Drug limit
:- #count { D : prescribe(D) } > 4.

% 2. Budget constraint
total_cost(C) :- C = #sum { Cost, D : prescribe(D), drug(D, Cost, _, _) }.
:- total_cost(C), C > 250.

% 3. Toxicity constraint
total_toxicity(T) :- T = #sum { Tox, D : prescribe(D), drug(D, _, Tox, _) }.
:- total_toxicity(T), T > 100.

% 4. Standard contraindications
:- prescribe(D), contraindicated_condition(D, C), patient_contraindication(C).

% 5. Genetic contraindications
:- prescribe(D), contraindicated_genetic(D, M), patient_genetic(M).

% 6 & 7. Interaction detection & Severe interaction prohibition
:- prescribe(D1), prescribe(D2), D1 < D2, interaction(D1, D2, severe).

% 8. Condition coverage
covered(C) :- prescribe(D), treats(D, C).
:- patient_condition(C), not covered(C).

% Objective: Minimize cost
#minimize { C, D : prescribe(D), drug(D, C, _, _) }.

#show prescribe/1.
#show total_cost/1.
#show total_toxicity/1.