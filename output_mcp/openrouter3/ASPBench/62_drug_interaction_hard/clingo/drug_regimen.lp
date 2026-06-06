% Drug Regimen Optimization Problem

% ===== DOMAIN DECLARATIONS =====
% Drugs
drug("cardio_ease").
drug("metformax").
drug("anxio_calm").
drug("pain_off").
drug("glucopain").
drug("hydro_stress").
drug("renal_guard").
drug("pain_plus").

% Patient conditions
condition("hypertension").
condition("diabetes").
condition("anxiety").
condition("pain").

% Patient contraindications
contraindication("renal_failure").

% Patient genetic markers
genetic_marker("G6PD_deficiency").

% ===== DRUG PROPERTIES =====
% Drug treats conditions
treats("cardio_ease", "hypertension").
treats("metformax", "diabetes").
treats("anxio_calm", "anxiety").
treats("pain_off", "pain").
treats("glucopain", "diabetes").
treats("glucopain", "pain").
treats("hydro_stress", "hypertension").
treats("hydro_stress", "anxiety").
treats("renal_guard", "hypertension").
treats("pain_plus", "pain").

% Drug costs
cost("cardio_ease", 50).
cost("metformax", 40).
cost("anxio_calm", 70).
cost("pain_off", 60).
cost("glucopain", 110).
cost("hydro_stress", 90).
cost("renal_guard", 120).
cost("pain_plus", 80).

% Drug toxicities
toxicity("cardio_ease", 20).
toxicity("metformax", 25).
toxicity("anxio_calm", 30).
toxicity("pain_off", 15).
toxicity("glucopain", 40).
toxicity("hydro_stress", 35).
toxicity("renal_guard", 10).
toxicity("pain_plus", 25).

% Drug max doses (for reference, not used in optimization)
max_dose("cardio_ease", 100).
max_dose("metformax", 1000).
max_dose("anxio_calm", 50).
max_dose("pain_off", 400).
max_dose("glucopain", 600).
max_dose("hydro_stress", 200).
max_dose("renal_guard", 150).
max_dose("pain_plus", 300).

% ===== CONTRAINDICATIONS =====
% Standard contraindications
contraindicated("renal_guard", "renal_failure").  % RenalGuard contraindicated with renal_failure

% Genetic contraindications
genetic_contraindicated("glucopain", "G6PD_deficiency").  % Glucopain contraindicated with G6PD_deficiency

% ===== INTERACTIONS =====
% Drug interactions (Type: reduced_efficacy, severe, synergy)
interacts("metformax", "pain_plus", "reduced_efficacy").  % Metformax interacts with pain_plus (reduced_efficacy, moderate)
interacts("hydro_stress", "metformax", "severe").  % Severe interaction with metformax if patient has diabetes
interacts("pain_plus", "anxio_calm", "synergy").  % Synergy with anxio_calm for anxiety (efficacy_bonus=2)

% ===== DECISION VARIABLES =====
% Choice rule: Select drugs to prescribe
{ prescribed(D) } :- drug(D).

% ===== CONSTRAINTS =====
% 1. Drug limit: At most 4 drugs
:- #count{ D : prescribed(D) } > 4.

% 2. Budget constraint: Total cost <= 250
total_cost(C) :- C = #sum{ V, D : prescribed(D), cost(D, V) }.
:- total_cost(C), C > 250.

% 3. Toxicity constraint: Total toxicity <= 100
total_toxicity(T) :- T = #sum{ V, D : prescribed(D), toxicity(D, V) }.
:- total_toxicity(T), T > 100.

% 4. Standard contraindications: Avoid drugs with standard contraindications
:- prescribed(D), contraindicated(D, C), contraindication(C).

% 5. Genetic contraindications: Avoid drugs with genetic contraindications
:- prescribed(D), genetic_contraindicated(D, G), genetic_marker(G).

% 6. Interaction detection: Identify all drug interactions
% For each pair of prescribed drugs, check if they interact
interaction_detected(D1, D2, Type) :- 
    prescribed(D1), prescribed(D2), D1 != D2,
    interacts(D1, D2, Type).

% Also check reverse interactions (symmetric)
interaction_detected(D1, D2, Type) :- 
    prescribed(D1), prescribed(D2), D1 != D2,
    interacts(D2, D1, Type).

% 7. Severe interaction prohibition: Do not prescribe drug combinations with severe interactions
:- prescribed(D1), prescribed(D2), D1 != D2, interacts(D1, D2, "severe").

% 8. Condition coverage: Treat all patient conditions
% A condition is treated if at least one prescribed drug treats it
treated(C) :- condition(C), prescribed(D), treats(D, C).

% All conditions must be treated
:- condition(C), not treated(C).

% ===== OBJECTIVE: MINIMIZE COST =====
#minimize { C : total_cost(C) }.

% ===== OUTPUT =====
% Show prescribed drugs
#show prescribed/1.

% Show treated conditions
#show treated/1.

% Show total cost and toxicity
#show total_cost/1.
#show total_toxicity/1.

% Show detected interactions
#show interaction_detected/3.

% Show conditions that are not treated (should be empty for optimal solution)
untreated(C) :- condition(C), not treated(C).
#show untreated/1.