% ===== DRUG DOMAINS =====
drug(cardio_ease).
drug(metformax).
drug(anxio_calm).
drug(pain_off).
drug(glucopain).
drug(hydro_stress).
drug(renal_guard).
drug(pain_plus).

% ===== CONDITION DOMAINS =====
condition(hypertension).
condition(diabetes).
condition(anxiety).
condition(pain).

% ===== DRUG PROPERTIES =====
cost(cardio_ease, 50).
cost(metformax, 40).
cost(anxio_calm, 70).
cost(pain_off, 60).
cost(glucopain, 110).
cost(hydro_stress, 90).
cost(renal_guard, 120).
cost(pain_plus, 80).

toxicity(cardio_ease, 20).
toxicity(metformax, 25).
toxicity(anxio_calm, 30).
toxicity(pain_off, 15).
toxicity(glucopain, 40).
toxicity(hydro_stress, 35).
toxicity(renal_guard, 10).
toxicity(pain_plus, 25).

max_dose(cardio_ease, 100).
max_dose(metformax, 1000).
max_dose(anxio_calm, 50).
max_dose(pain_off, 400).
max_dose(glucopain, 600).
max_dose(hydro_stress, 200).
max_dose(renal_guard, 150).
max_dose(pain_plus, 300).

% ===== TREATMENT MAPPING =====
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

% ===== PATIENT PROFILE =====
patient_condition(hypertension).
patient_condition(diabetes).
patient_condition(anxiety).
patient_condition(pain).

patient_contraindication(renal_failure).
patient_genetic_marker(g6pd_deficiency).

% ===== CONTRAINDICATIONS =====
% Standard contraindications
std_contraindicated(renal_guard, renal_failure).

% Genetic contraindications
genetic_contraindicated(glucopain, g6pd_deficiency).

% ===== DRUG INTERACTIONS =====
% Regular interactions (always active between the two drugs)
interacts(metformax, pain_plus, reduced_efficacy, moderate).

% Severe interactions (conditional on patient having a specific condition)
severe_interaction_conditional(hydro_stress, metformax, diabetes).

% Synergy effects (informational)
synergy(pain_plus, anxio_calm, anxiety, efficacy_bonus, 2).

% ===== DECISION: SELECT DRUGS =====
{ prescribe(D) } :- drug(D).

% ===== CONSTRAINT 1: Drug limit (at most 4) =====
:- #count{ D : prescribe(D) } > 4.

% ===== CONSTRAINT 2: Budget constraint (total cost <= 250) =====
total_cost(S) :- S = #sum{ C,D : prescribe(D), cost(D,C) }.
:- total_cost(S), S > 250.

% ===== CONSTRAINT 3: Toxicity constraint (total toxicity <= 100) =====
total_toxicity(S) :- S = #sum{ T,D : prescribe(D), toxicity(D,T) }.
:- total_toxicity(S), S > 100.

% ===== CONSTRAINT 4: Standard contraindications =====
:- prescribe(D), std_contraindicated(D, C), patient_contraindication(C).

% ===== CONSTRAINT 5: Genetic contraindications =====
:- prescribe(D), genetic_contraindicated(D, G), patient_genetic_marker(G).

% ===== CONSTRAINT 7: Severe interaction prohibition =====
:- prescribe(D1), prescribe(D2), severe_interaction_conditional(D1, D2, Cond), patient_condition(Cond).
:- prescribe(D1), prescribe(D2), severe_interaction_conditional(D2, D1, Cond), patient_condition(Cond).

% ===== CONSTRAINT 8: Condition coverage (all patient conditions must be treated) =====
covered(C) :- prescribe(D), treats(D, C), patient_condition(C).
:- patient_condition(C), not covered(C).

% ===== SAFETY ANALYSIS: Detect interactions among prescribed drugs =====
interaction_detected(D1, D2, Type, Severity) :-
    prescribe(D1), prescribe(D2),
    interacts(D1, D2, Type, Severity),
    D1 < D2.
interaction_detected(D1, D2, Type, Severity) :-
    prescribe(D1), prescribe(D2),
    interacts(D2, D1, Type, Severity),
    D1 < D2.

% ===== CONTRAINDICATIONS AVOIDED (for reporting) =====
contraindication_avoided(C) :-
    std_contraindicated(D, C),
    patient_contraindication(C),
    not prescribe(D).
contraindication_avoided(G) :-
    genetic_contraindicated(D, G),
    patient_genetic_marker(G),
    not prescribe(D).

% ===== OBJECTIVE: Minimize total cost =====
#minimize{ C,D : prescribe(D), cost(D,C) }.

% ===== OUTPUT =====
#show prescribe/1.
#show total_cost/1.
#show total_toxicity/1.
#show covered/1.
#show interaction_detected/4.
#show contraindication_avoided/1.