% Entities
fof(monkeypox_disease_type, axiom, disease(monkeypox_disease)).
fof(fever_type, axiom, symptom(fever)).
fof(headache_type, axiom, symptom(headache)).
fof(muscle_pains_type, axiom, symptom(muscle_pains)).
fof(tiredness_type, axiom, symptom(tiredness)).
fof(coughing_type, axiom, symptom(coughing)).

% Premise 1: Virus occurrence may lead to Monkeypox
fof(premise1, axiom, ! [X] : (has_virus(X) => gets_monkeypox(X))).

% Premise 2: Virus can occur in certain animals
fof(premise2, axiom, ? [X] : (animal(X) & has_virus(X))).

% Premise 3: Humans are mammals
fof(premise3, axiom, ! [X] : (human(X) => mammal(X))).

% Premise 4: Mammals are animals
fof(premise4, axiom, ! [X] : (mammal(X) => animal(X))).

% Premise 5: Symptoms of Monkeypox
fof(premise5_1, axiom, symptom_of(fever, monkeypox_disease)).
fof(premise5_2, axiom, symptom_of(headache, monkeypox_disease)).
fof(premise5_3, axiom, symptom_of(muscle_pains, monkeypox_disease)).
fof(premise5_4, axiom, symptom_of(tiredness, monkeypox_disease)).

% Premise 6: Flu symptom
fof(premise6, axiom, ! [X] : (gets_flu(X) => has_symptom(X, tiredness))).

% Negated conclusion
fof(negated_conclusion, conjecture, ~symptom_of(coughing, monkeypox_disease)).