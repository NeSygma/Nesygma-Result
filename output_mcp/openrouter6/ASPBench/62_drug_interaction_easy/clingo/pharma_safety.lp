% Pharmaceutical Safety Analysis - ASP Model

% ===== FACTS FROM PROBLEM STATEMENT =====

% Patient data
patient_condition(pain).
patient_condition(hypertension).
patient_condition(diabetes).
patient_contraindication(bleeding_disorder).
max_drugs(3).

% Drug data
drug(drug1).
drug(drug2).
drug(drug3).
drug(drug4).
drug(drug5).

% Drug treatments
treats(drug1, pain).
treats(drug1, inflammation).
treats(drug2, blood_clot_prevention).
treats(drug3, hypertension).
treats(drug4, diabetes).
treats(drug5, pain).
treats(drug5, inflammation).

% Drug contraindications
drug_contraindication(drug1, bleeding_disorder).
drug_contraindication(drug2, pregnancy).
drug_contraindication(drug3, kidney_disease).
drug_contraindication(drug4, kidney_disease).
drug_contraindication(drug5, none).  % none means no contraindications

% Max doses (mg)
max_dose(drug1, 4000).
max_dose(drug2, 10).
max_dose(drug3, 40).
max_dose(drug4, 2000).
max_dose(drug5, 2400).

% Interactions: interaction(Drug1, Drug2, Severity)
% Severity: severe, moderate, mild
interaction(drug1, drug2, moderate).
interaction(drug2, drug1, moderate).
interaction(drug3, drug4, mild).
interaction(drug4, drug3, mild).
interaction(drug5, drug3, moderate).
interaction(drug3, drug5, moderate).

% ===== CHOICE RULES =====

% Select drugs (0 to max_drugs)
{ prescribed(D) } :- drug(D).
% Ensure we don't exceed max drugs
:- #count{ D : prescribed(D) } > N, max_drugs(N).

% Assign dose to each prescribed drug (1 to max_dose)
{ dose(D, Dose) : Dose = 1..Max } :- prescribed(D), max_dose(D, Max).
% Ensure exactly one dose per prescribed drug
:- prescribed(D), #count{ Dose : dose(D, Dose) } != 1.

% ===== CONSTRAINTS =====

% No prescribed drug can match patient contraindications
:- prescribed(D), drug_contraindication(D, C), patient_contraindication(C).

% ===== DERIVED PREDICATES =====

% Conditions treated by prescribed drugs
treated_condition(C) :- patient_condition(C), prescribed(D), treats(D, C).

% Untreated conditions
untreated_condition(C) :- patient_condition(C), not treated_condition(C).

% Interaction detection: if two prescribed drugs have an interaction
interaction_detected(D1, D2, Severity) :- 
    prescribed(D1), prescribed(D2), D1 != D2,
    interaction(D1, D2, Severity).

% Interaction penalties (using integer weights for optimization)
% severe = 3, moderate = 2, mild = 1
interaction_penalty(D1, D2, 3) :- interaction_detected(D1, D2, severe).
interaction_penalty(D1, D2, 2) :- interaction_detected(D1, D2, moderate).
interaction_penalty(D1, D2, 1) :- interaction_detected(D1, D2, mild).

% Total interaction penalty (sum of weights)
total_interaction_weight(W) :- W = #sum{ P : interaction_penalty(_, _, P) }.

% Count of treated conditions
treated_count(N) :- N = #count{ C : treated_condition(C) }.

% Count of total conditions
total_conditions(N) :- N = #count{ C : patient_condition(C) }.

% ===== SAFETY SCORE CALCULATION =====

% Coverage bonus: (treated / total) * 0.5
% We'll compute using integer arithmetic: bonus = (treated * 50) / total
coverage_bonus_int(B) :- 
    treated_count(T), total_conditions(Total),
    B = (T * 50) / Total.

% Convert to float for safety score (but ASP doesn't have floats, so we'll compute safety score as integer scaled)
% Instead, we'll compute safety score as integer scaled by 100
% safety_score_scaled = 50 + coverage_bonus_int - penalty_scaled
% where penalty_scaled = severe: 30, moderate: 15, mild: 5

% Interaction penalty values scaled by 100
penalty_value_scaled(severe, 30).
penalty_value_scaled(moderate, 15).
penalty_value_scaled(mild, 5).

% Total penalty scaled
total_penalty_scaled(P) :-
    P = #sum{ Penalty : interaction_detected(D1, D2, Severity), penalty_value_scaled(Severity, Penalty) }.

% Safety score scaled by 100 (0 to 100)
safety_score_scaled(S) :-
    coverage_bonus_int(CB),
    total_penalty_scaled(TP),
    S = 50 + CB - TP.

% Clamp to [0, 100]
safety_score_scaled_clamped(S) :- safety_score_scaled(S0), S0 >= 0, S0 <= 100, S = S0.
safety_score_scaled_clamped(0) :- safety_score_scaled(S0), S0 < 0.
safety_score_scaled_clamped(100) :- safety_score_scaled(S0), S0 > 100.

% Convert to float for output (we'll output as integer and let downstream convert)
safety_score_int(S) :- safety_score_scaled_clamped(S).

% ===== OPTIMIZATION =====

% Objective: maximize treated conditions, minimize interaction severity
% We use weighted sum: treat each treated condition as +10, each interaction penalty as -weight
objective_value(V) :-
    treated_count(T),
    total_interaction_weight(W),
    V = T * 10 - W.

% Maximize the objective value
#maximize { V : objective_value(V) }.

% ===== OUTPUT =====

% Show prescribed drugs with dose
prescribed_drug(D, Dose) :- prescribed(D), dose(D, Dose).

% Show treated conditions
treated_condition_output(C) :- treated_condition(C).

% Show untreated conditions
untreated_condition_output(C) :- untreated_condition(C).

% Show interactions detected
interaction_output(D1, D2, Severity) :- interaction_detected(D1, D2, Severity).

% Show safety analysis
safety_analysis_contraindications_avoided(C) :- patient_contraindication(C).

% Show safety score (as integer 0-100)
safety_analysis_score_int(S) :- safety_score_int(S).

% Show all output predicates
#show prescribed_drug/2.
#show treated_condition_output/1.
#show untreated_condition_output/1.
#show interaction_output/3.
#show safety_analysis_contraindications_avoided/1.
#show safety_analysis_score_int/1.