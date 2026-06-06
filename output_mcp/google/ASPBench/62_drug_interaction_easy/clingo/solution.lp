% --- Data ---
drug("drug1", 4000).
drug("drug2", 10).
drug("drug3", 40).
drug("drug4", 2000).
drug("drug5", 2400).

treats("drug1", "pain").
treats("drug1", "inflammation").
treats("drug2", "blood_clot_prevention").
treats("drug3", "hypertension").
treats("drug4", "diabetes").
treats("drug5", "pain").
treats("drug5", "inflammation").

contra("drug1", "bleeding_disorder").
contra("drug2", "pregnancy").
contra("drug3", "kidney_disease").
contra("drug4", "kidney_disease").

interacts("drug1", "drug2", "moderate").
interacts("drug3", "drug4", "mild").
interacts("drug3", "drug5", "moderate").

patient_condition("pain").
patient_condition("hypertension").
patient_condition("diabetes").
patient_contra("bleeding_disorder").

max_drugs(3).

% --- Logic ---
{ prescribe(ID) } :- drug(ID, _).

% Constraint: Max drugs
:- #count { ID : prescribe(ID) } > M, max_drugs(M).

% Constraint: Contraindications
:- prescribe(ID), contra(ID, C), patient_contra(C).

% Treatment coverage
treated(C) :- patient_condition(C), prescribe(ID), treats(ID, C).
num_treated(N) :- N = #count { C : treated(C) }.
total_conditions(3).

% Interaction penalties
penalty_val("severe", 300).
penalty_val("moderate", 150).
penalty_val("mild", 50).

interaction(ID1, ID2, Sev) :- prescribe(ID1), prescribe(ID2), ID1 < ID2, interacts(ID1, ID2, Sev).
interaction(ID1, ID2, Sev) :- prescribe(ID1), prescribe(ID2), ID1 < ID2, interacts(ID2, ID1, Sev).

total_penalty(P) :- P = #sum { SevVal, ID1, ID2 : interaction(ID1, ID2, Sev), penalty_val(Sev, SevVal) }.
total_penalty(0) :- not interaction(_, _, _).

% Score calculation (scaled by 1000 to avoid floats)
% score = 500 + (num_treated / total_conditions) * 500 - total_penalty
score(S) :- num_treated(N), total_conditions(T), total_penalty(P), S = 500 + (N * 500 / T) - P.

#maximize { S : score(S) }.

% --- Output ---
option(prescribe(ID)) :- prescribe(ID).
#show prescribe/1.
#show score/1.