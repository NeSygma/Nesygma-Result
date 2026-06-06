% Pharmaceutical Safety Analysis - Clingo ASP Model

% ===== DOMAIN DECLARATIONS =====
% Patient domains
patient_condition(pain).
patient_condition(hypertension).
patient_condition(diabetes).
patient_contraindication(bleeding_disorder).
max_drugs(3).

% Drug domains
drug(drug1).
drug(drug2).
drug(drug3).
drug(drug4).
drug(drug5).

% Condition domains (for treatment coverage)
condition(pain).
condition(hypertension).
condition(diabetes).
condition(inflammation).
condition(blood_clot_prevention).
condition(kidney_disease).

% Severity levels for interactions
severity(severe).
severity(moderate).
severity(mild).

% ===== DRUG PROPERTIES =====
% Drug 1 (Aspirin)
treats(drug1, pain).
treats(drug1, inflammation).
drug_contraindication(drug1, bleeding_disorder).
max_dose(drug1, 4000).
interaction(drug1, drug2, moderate). % increased_bleeding

% Drug 2 (Warfarin)
treats(drug2, blood_clot_prevention).
drug_contraindication(drug2, pregnancy).
max_dose(drug2, 10).
interaction(drug2, drug1, moderate). % increased_bleeding

% Drug 3 (Lisinopril)
treats(drug3, hypertension).
drug_contraindication(drug3, kidney_disease).
max_dose(drug3, 40).
interaction(drug3, drug4, mild). % mild_nausea

% Drug 4 (Metformin)
treats(drug4, diabetes).
drug_contraindication(drug4, kidney_disease).
max_dose(drug4, 2000).
interaction(drug4, drug3, mild). % mild_nausea

% Drug 5 (Ibuprofen)
treats(drug5, pain).
treats(drug5, inflammation).
drug_contraindication(drug5, none). % No contraindications
max_dose(drug5, 2400).
interaction(drug5, drug3, moderate). % reduced_bp_effect

% ===== PRESCRIPTION RULES =====
% Define valid doses (1 to 2400 for all drugs - maximum possible)
dose(1..2400).

% Choice rule: Select drugs to prescribe (0 to max_drugs)
{ prescribed(D, Dose) : dose(Dose) } :- drug(D).

% Constraint: Dose must be between 1 and max_dose for prescribed drugs
:- prescribed(D, Dose), max_dose(D, MaxDose), Dose < 1.
:- prescribed(D, Dose), max_dose(D, MaxDose), Dose > MaxDose.

% Constraint: Cannot prescribe drugs that match patient's contraindications
:- prescribed(D, _), drug_contraindication(D, C), patient_contraindication(C).

% Constraint: No more than max_drugs
:- #count{D : prescribed(D, _)} > Max, max_drugs(Max).

% ===== TREATMENT COVERAGE =====
% A condition is treated if at least one prescribed drug treats it
treated(C) :- patient_condition(C), prescribed(D, _), treats(D, C).

% ===== INTERACTION DETECTION =====
% Detect interactions between prescribed drugs (avoid double counting)
interaction_detected(D1, D2, Severity) :- 
    prescribed(D1, _), prescribed(D2, _), 
    interaction(D1, D2, Severity),
    D1 != D2.

% ===== SAFETY SCORE CALCULATION =====
% Count treated conditions
num_treated(N) :- N = #count{C : treated(C)}.
total_conditions(T) :- T = #count{C : patient_condition(C)}.

% Calculate coverage bonus
coverage_bonus(B) :- 
    num_treated(N), total_conditions(T), 
    B = (N * 50) / (T * 100).  % (N/T) * 0.5

% Calculate interaction penalties
penalty(severe, -0.3).
penalty(moderate, -0.15).
penalty(mild, -0.05).

total_penalty(P) :- 
    P = #sum{Pen : interaction_detected(D1, D2, Sev), penalty(Sev, Pen)}.

% Calculate safety score (clamped to [0,1])
% Use helper predicates for clamping
safety_score_raw(Raw) :-
    coverage_bonus(B), total_penalty(P),
    Raw = 0.5 + B + P.

safety_score(S) :-
    safety_score_raw(Raw),
    Raw >= 0, Raw <= 1,
    S = Raw.

safety_score(0) :-
    safety_score_raw(Raw),
    Raw < 0.

safety_score(1) :-
    safety_score_raw(Raw),
    Raw > 1.

% ===== OUTPUT PREDICATES =====
% Prescribed drugs with dose
prescribed_drug(D, Dose) :- prescribed(D, Dose).

% Treated conditions
treated_condition(C) :- treated(C).

% Untreated conditions
untreated_condition(C) :- patient_condition(C), not treated(C).

% Interaction detection for output
interaction_pair(D1, D2, Sev) :- interaction_detected(D1, D2, Sev).

% Contraindications avoided (informational)
contraindication_avoided(C) :- patient_contraindication(C).

% ===== SHOW DIRECTIVES =====
#show prescribed_drug/2.
#show treated_condition/1.
#show untreated_condition/1.
#show interaction_pair/3.
#show contraindication_avoided/1.
#show safety_score/1.