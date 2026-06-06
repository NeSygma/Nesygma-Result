% --- DOMAINS ---
drug(drug1; drug2; drug3; drug4; drug5).
condition(pain; hypertension; diabetes; inflammation).
contraindication(bleeding_disorder; pregnancy; kidney_disease).
severity(severe; moderate; mild).

% --- PATIENT DATA ---
has_condition(pain).
has_condition(hypertension).
has_condition(diabetes).
has_contraindication(bleeding_disorder).
max_drugs(3).

% --- DRUG PROPERTIES ---
% drug(DrugID, MaxDose)
drug(drug1, 4000).
drug(drug2, 10).
drug(drug3, 40).
drug(drug4, 2000).
drug(drug5, 2400).

% treats(DrugID, Condition)
treats(drug1, pain).
treats(drug1, inflammation).
treats(drug2, blood_clot_prevention).
treats(drug3, hypertension).
treats(drug4, diabetes).
treats(drug5, pain).
treats(drug5, inflammation).

% contraindicated(DrugID, Contraindication)
contraindicated(drug1, bleeding_disorder).
contraindicated(drug2, pregnancy).
contraindicated(drug3, kidney_disease).
contraindicated(drug4, kidney_disease).

% interaction(Drug1, Drug2, Severity)
interaction(drug1, drug2, moderate).
interaction(drug2, drug1, moderate).
interaction(drug3, drug4, mild).
interaction(drug4, drug3, mild).
interaction(drug3, drug5, moderate).
interaction(drug5, drug3, moderate).

% --- PRESCRIPTION SELECTION ---
% Choose which drugs to prescribe, with dose (frequency is not constrained)
{ prescribed(Drug, Dose) : drug(Drug, MaxDose), Dose = 1..MaxDose }.

% --- CONSTRAINTS ---

% 1. Cannot prescribe contraindicated drugs
:- prescribed(D, _), contraindicated(D, C), has_contraindication(C).

% 2. Maximum number of drugs
:- #count{D : prescribed(D, _)} > max_drugs.

% 3. Treatment coverage: each patient condition must be treated by at least one prescribed drug
% Note: inflammation is not a patient condition, so we ignore it
treated_condition(C) :- prescribed(D, _), treats(D, C), has_condition(C).

% Ensure all patient conditions are treated
:- has_condition(C), not treated_condition(C).

% --- INTERACTION DETECTION ---
% For each pair of prescribed drugs, check if they interact
prescribed_pair(D1, D2) :- prescribed(D1, _), prescribed(D2, _), D1 < D2.

% Calculate interaction penalty based on severity (scaled by 100 to avoid floats)
interaction_penalty(D1, D2, 30) :- prescribed_pair(D1, D2), interaction(D1, D2, severe).
interaction_penalty(D1, D2, 15) :- prescribed_pair(D1, D2), interaction(D1, D2, moderate).
interaction_penalty(D1, D2, 5)  :- prescribed_pair(D1, D2), interaction(D1, D2, mild).

total_penalty(Penalty) :- Penalty = #sum[PenaltyVal : interaction_penalty(_, _, PenaltyVal)].

% --- SAFETY SCORE CALCULATION ---
total_conditions(N) :- N = #count{C : has_condition(C)}.
treated_conditions(T) :- T = #count{C : treated_condition(C)}.

% Calculate coverage bonus: (treated_conditions / total_conditions) * 50 (scaled by 100)
coverage_bonus(Bonus) :-
    treated_conditions(T),
    total_conditions(Total),
    Bonus = (T * 50) / Total.

% Calculate safety score: 50 + coverage_bonus - total_penalty (scaled by 100)
% Clamp safety score to [0, 100]
safety_score(Score) :-
    coverage_bonus(Bonus),
    total_penalty(Penalty),
    Score = 50 + Bonus - Penalty,
    Score >= 0,
    Score =< 100.

safety_score(0) :- safety_score(S), S < 0.
safety_score(100) :- safety_score(S), S > 100.

% --- OPTIMIZATION ---
% Prioritize maximizing treatment coverage, then minimizing penalties
#maximize { 1@3, T : treated_conditions(T) }.
#minimize { Penalty@2 : interaction_penalty(_, _, Penalty) }.

% --- OUTPUT ---
#show prescribed/2.
#show treated_condition/1.
#show has_condition/1.
#show has_contraindication/1.
#show safety_score/1.