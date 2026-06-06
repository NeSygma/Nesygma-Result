% Axiom: humans are mammals
fof(axiom_human_mammal, axiom, ! [X] : (human(X) => mammal(X))).
% Axiom: mammals are animals
fof(axiom_mammal_animal, axiom, ! [X] : (mammal(X) => animal(X))).
% Axiom: monkeypox virus can occur in rabbit
fof(axiom_can_occur_in_rabbit, axiom, can_occur_in(monkeypox, rabbit)).
% Axiom: symptom fever
fof(axiom_symptom_fever, axiom, has_symptom(monkeypox, fever)).
% Axiom: symptom headache
fof(axiom_symptom_headache, axiom, has_symptom(monkeypox, headache)).
% Axiom: symptom muscle pains
fof(axiom_symptom_muscle_pains, axiom, has_symptom(monkeypox, muscle_pains)).
% Axiom: symptom tiredness
fof(axiom_symptom_tiredness, axiom, has_symptom(monkeypox, tiredness)).
% Axiom: people feel tired when they get the flu
fof(axiom_flu_tired, axiom, ! [X] : (get_flu(X) => feel_tired(X))).
% Conjecture: symptoms of monkeypox include coughing
fof(conjecture, conjecture, has_symptom(monkeypox, coughing)).