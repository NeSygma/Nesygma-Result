% =============================================
% Pharmaceutical Safety - Drug Combination Solver
% =============================================

% === DRUG DOMAINS ===
drug(drug1). drug(drug2). drug(drug3). drug(drug4). drug(drug5).

% === PATIENT DATA ===
patient_condition(pain).
patient_condition(hypertension).
patient_condition(diabetes).

patient_contra(bleeding_disorder).

max_drugs(3).

% === DRUG PROPERTIES ===

% What each drug treats
treats(drug1, pain).
treats(drug1, inflammation).
treats(drug2, blood_clot_prevention).
treats(drug3, hypertension).
treats(drug4, diabetes).
treats(drug5, pain).
treats(drug5, inflammation).

% Drug contraindications
drug_contra(drug1, bleeding_disorder).
drug_contra(drug2, pregnancy).
drug_contra(drug3, kidney_disease).
drug_contra(drug4, kidney_disease).
% drug5 has no contraindications

% Maximum doses (mg)
max_dose(drug1, 4000).
max_dose(drug2, 10).
max_dose(drug3, 40).
max_dose(drug4, 2000).
max_dose(drug5, 2400).

% Drug interactions (stored with smaller ID first)
interaction(drug1, drug2, increased_bleeding, moderate).
interaction(drug3, drug4, mild_nausea, mild).
interaction(drug3, drug5, reduced_bp_effect, moderate).

% === CHOICE RULES ===

% Choose which drugs to prescribe
{ prescribed(D) } :- drug(D).

% === HARD CONSTRAINTS ===

% Constraint 1: Maximum number of prescribed drugs
:- #count{ D : prescribed(D) } > N, max_drugs(N).

% Constraint 2: Cannot prescribe drugs matching patient contraindications
:- prescribed(D), drug_contra(D, C), patient_contra(C).

% === DERIVED ATOMS ===

% Assign a valid dose (use minimum valid dose of 1mg for each prescribed drug)
dose(D, 1) :- prescribed(D).

% A patient condition is treated if at least one prescribed drug treats it
treated(C) :- prescribed(D), treats(D, C), patient_condition(C).

% Untreated conditions
untreated(C) :- patient_condition(C), not treated(C).

% Detect pairwise interactions between prescribed drugs (D1 < D2 to avoid double counting)
interaction_detected(D1, D2, Effect, Severity) :-
    prescribed(D1), prescribed(D2),
    interaction(D1, D2, Effect, Severity),
    D1 < D2.

interaction_detected(D1, D2, Effect, Severity) :-
    prescribed(D1), prescribed(D2),
    interaction(D2, D1, Effect, Severity),
    D1 < D2.

% === COUNTS FOR SAFETY SCORE ===

treated_count(N) :- N = #count{ C : treated(C) }.
total_conditions(N) :- N = #count{ C : patient_condition(C) }.
severe_count(N) :- N = #count{ D1, D2 : interaction_detected(D1, D2, _, severe) }.
moderate_count(N) :- N = #count{ D1, D2 : interaction_detected(D1, D2, _, moderate) }.
mild_count(N) :- N = #count{ D1, D2 : interaction_detected(D1, D2, _, mild) }.

% === SAFETY SCORE (scaled by 1000 for integer arithmetic) ===
% safety_score = 0.5 + (treated/total)*0.5 - (severe*0.3 + moderate*0.15 + mild*0.05)
% Scaled: 500 + (treated*500)/total - (severe*300 + moderate*150 + mild*50)

safety_score_raw(S) :-
    treated_count(TC), total_conditions(TOT),
    severe_count(SC), moderate_count(MC), mild_count(IC),
    S = 500 + (TC * 500) / TOT - (SC * 300 + MC * 150 + IC * 50).

% Clamp to [0, 1000]
safety_score(0) :- safety_score_raw(S), S < 0.
safety_score(1000) :- safety_score_raw(S), S > 1000.
safety_score(S) :- safety_score_raw(S), S >= 0, S <= 1000.

% === OPTIMIZATION ===
% Maximize the safety score (combines coverage and interaction penalties)
#maximize { S : safety_score(S) }.

% === OUTPUT DIRECTIVES ===
#show prescribed/1.
#show dose/2.
#show treated/1.
#show untreated/1.
#show interaction_detected/4.
#show safety_score/1.
#show treated_count/1.
#show total_conditions/1.
#show severe_count/1.
#show moderate_count/1.
#show mild_count/1.
#show patient_contra/1.