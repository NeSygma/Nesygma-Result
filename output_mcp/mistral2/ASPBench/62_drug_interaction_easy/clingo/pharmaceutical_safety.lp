% --- Patient Data ---
patient_condition(pain).
patient_condition(hypertension).
patient_condition(diabetes).

patient_contraindication(bleeding_disorder).

max_drugs(3).

% --- Drug Data ---
drug(drug1; drug2; drug3; drug4; drug5).

% Treats
treats(drug1, pain).
treats(drug1, inflammation).
treats(drug2, blood_clot_prevention).
treats(drug3, hypertension).
treats(drug4, diabetes).
treats(drug5, pain).
treats(drug5, inflammation).

% Contraindications
drug_contraindication(drug1, bleeding_disorder).
drug_contraindication(drug2, pregnancy).
drug_contraindication(drug3, kidney_disease).
drug_contraindication(drug4, kidney_disease).

% Max Dose
max_dose(drug1, 4000).
max_dose(drug2, 10).
max_dose(drug3, 40).
max_dose(drug4, 2000).
max_dose(drug5, 2400).

% Interactions
interaction(drug1, drug2, moderate).
interaction(drug2, drug1, moderate).
interaction(drug3, drug4, mild).
interaction(drug4, drug3, mild).
interaction(drug3, drug5, moderate).
interaction(drug5, drug3, moderate).

% --- Prescription Selection ---
% Choose up to max_drugs drugs for prescription
1 { prescribed(D, Dose, Freq) : drug(D), max_dose(D, MaxDose), Dose = 1..MaxDose, Freq = 1 } MaxDrugs :- max_drugs(MaxDrugs).

% Ensure no contraindications are violated
:- prescribed(D, _, _), drug_contraindication(D, C), patient_contraindication(C).

% --- Treatment Coverage ---
% A condition is treated if at least one prescribed drug treats it
treated_condition(C) :- patient_condition(C), prescribed(D, _, _), treats(D, C).

% --- Interaction Detection ---
% Detect interactions between prescribed drugs
interaction_detected(D1, D2, Severity) :-
    prescribed(D1, _, _),
    prescribed(D2, _, _),
    D1 < D2,
    interaction(D1, D2, Severity).

% --- Safety Score Calculation ---
% Count treated conditions
num_treated(N) :- N = #count{ C : treated_condition(C) }.

% Count total conditions
num_total(N) :- N = #count{ C : patient_condition(C) }.

% Calculate coverage bonus
coverage_bonus(Bonus) :-
    num_treated(T),
    num_total(Total),
    Bonus = (T / Total) * 0.5.

% Calculate total penalty from interactions
total_penalty(Penalty) :-
    Penalty = #sum{ PenaltyValue : interaction_detected(_, _, Severity), penalty_value(Severity, PenaltyValue) }.

penalty_value(severe, 0.3).
penalty_value(moderate, 0.15).
penalty_value(mild, 0.05).

% Calculate safety score
safety_score(Score) :-
    coverage_bonus(Bonus),
    total_penalty(Penalty),
    Score = 0.5 + Bonus - Penalty.

% Clamp safety score to [0, 1]
safety_score(Score) :- safety_score(ScoreRaw), Score = #min(1, #max(0, ScoreRaw)).

% --- Untreated Conditions ---
untreated_condition(C) :-
    patient_condition(C),
    not treated_condition(C).

% --- Output ---
#show prescribed/3.
#show treated_condition/1.
#show untreated_condition/1.
#show interaction_detected/3.
#show patient_contraindication/1.
#show safety_score/1.