tff(distinct, axiom, $distinct(monkeypox_virus, monkeypox, fever, headache, muscle_pains, tiredness, coughing, animal1)).
tff(rule_occurs, axiom, ! [X] : (occurs(monkeypox_virus, X) => has_disease(X, monkeypox))).
tff(rule_symptom_fever, axiom, has_symptom(monkeypox, fever)).
tff(rule_symptom_headache, axiom, has_symptom(monkeypox, headache)).
tff(rule_symptom_muscle_pains, axiom, has_symptom(monkeypox, muscle_pains)).
tff(rule_symptom_tiredness, axiom, has_symptom(monkeypox, tiredness)).
tff(rule_human_mammal, axiom, ! [X] : (human(X) => mammal(X))).
tff(rule_mammal_animal, axiom, ! [X] : (mammal(X) => animal(X))).
tff(rule_exists_animal, axiom, animal(animal1)).
tff(rule_occurs_animal, axiom, occurs(monkeypox_virus, animal1)).
tff(rule_flu_tired, axiom, ! [X] : (has_disease(X, flu) => feels_tired(X))).
tff(conjecture, conjecture, ~has_symptom(monkeypox, coughing)).