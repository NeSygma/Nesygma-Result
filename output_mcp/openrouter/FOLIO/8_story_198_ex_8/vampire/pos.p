% Positive conjecture: No one gets the flu.
fof(distinct_consts, axiom, (monkeypox_virus != person1 & monkeypox_virus != animal1 & person1 != animal1)).
fof(human_def, axiom, ! [X] : (human(X) => mammal(X))).
fof(mammal_def, axiom, ! [X] : (mammal(X) => animal(X))).
fof(monkeypox_occurs_some, axiom, ? [A] : (animal(A) & occurs(monkeypox_virus, A))).
fof(monkeypox_rule, axiom, ! [X] : (occurs(monkeypox_virus, X) => gets_monkeypox(X))).
fof(monkeypox_symptoms, axiom, ! [X] : (gets_monkeypox(X) => (has_fever(X) & has_headache(X) & has_muscle_pain(X) & has_tiredness(X)))).
fof(flu_symptoms, axiom, ! [X] : (gets_flu(X) => has_tiredness(X))).
fof(human1, axiom, human(person1)).
fof(goal_pos, conjecture, ! [X] : ~gets_flu(X)).