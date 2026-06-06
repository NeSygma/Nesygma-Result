fof(occurs_in_monkeypox, axiom, ! [X] : (occurs_in(monkeypox_virus, X) => has_monkeypox(X))).
fof(monkeypox_in_animals, axiom, ! [X] : (is_animal(X) => occurs_in(monkeypox_virus, X))).
fof(humans_are_mammals, axiom, ! [X] : (human(X) => is_mammal(X))).
fof(mammals_are_animals, axiom, ! [X] : (is_mammal(X) => is_animal(X))).
fof(monkeypox_symptom_fever, axiom, ! [X] : (has_monkeypox(X) => has_symptom(X, fever))).
fof(monkeypox_symptom_headache, axiom, ! [X] : (has_monkeypox(X) => has_symptom(X, headache))).
fof(monkeypox_symptom_muscle_pains, axiom, ! [X] : (has_monkeypox(X) => has_symptom(X, muscle_pains))).
fof(monkeypox_symptom_tiredness, axiom, ! [X] : (has_monkeypox(X) => has_symptom(X, tiredness))).
fof(flu_tiredness, axiom, ! [X] : (has_flu(X) => feels_tired(X))).
fof(distinct_human_animal, axiom, ! [X] : (human(X) => ~is_animal(X))).
fof(distinct_animal_human, axiom, ! [X] : (is_animal(X) => ~human(X))).
fof(negated_conclusion, conjecture, ? [X] : has_flu(X)).