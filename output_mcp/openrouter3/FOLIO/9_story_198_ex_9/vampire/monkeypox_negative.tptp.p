% Monkeypox Problem - Negative Version (Testing if coughing is NOT a symptom)
% Premises
fof(premise_1, axiom, ! [X] : (virus_occurs_in(monkeypox_virus, X) => may_have_disease(X, monkeypox))).
fof(premise_2, axiom, ? [A] : (animal(A) & virus_occurs_in(monkeypox_virus, A))).
fof(premise_3, axiom, ! [H] : (human(H) => mammal(H))).
fof(premise_4, axiom, ! [M] : (mammal(M) => animal(M))).
fof(premise_5a, axiom, has_symptom(monkeypox, fever)).
fof(premise_5b, axiom, has_symptom(monkeypox, headache)).
fof(premise_5c, axiom, has_symptom(monkeypox, muscle_pain)).
fof(premise_5d, axiom, has_symptom(monkeypox, tiredness)).
fof(premise_6, axiom, ! [P] : (human(P) & has_disease(P, flu) => feels_tired(P))).

% Answer predicate mapping - we want to show coughing is NOT a symptom
fof(ans_map, axiom, ! [D, S] : (has_symptom(D, S) => ans(S))).

% Distinctness axioms
fof(distinct_symptoms, axiom, (fever != headache & fever != muscle_pain & fever != tiredness & fever != coughing & headache != muscle_pain & headache != tiredness & headache != coughing & muscle_pain != tiredness & muscle_pain != coughing & tiredness != coughing)).

% Negated conclusion: coughing is NOT a symptom of monkeypox
fof(goal, conjecture, ~has_symptom(monkeypox, coughing))).