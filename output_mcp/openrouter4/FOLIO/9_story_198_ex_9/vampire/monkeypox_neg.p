fof(premise1, axiom, ! [X] : (monkeypox_virus_occurs(X) => can_get_monkeypox(X))).
fof(premise2, axiom, ? [X] : (animal(X) & monkeypox_virus_occurs(X))).
fof(premise3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise5, axiom, symptom_of_monkeypox(fever)).
fof(premise6, axiom, symptom_of_monkeypox(headache)).
fof(premise7, axiom, symptom_of_monkeypox(muscle_pains)).
fof(premise8, axiom, symptom_of_monkeypox(tiredness)).
fof(premise9, axiom, ! [X] : (gets_flu(X) => feels_tired(X))).
fof(conjecture, conjecture, ~symptom_of_monkeypox(coughing)).