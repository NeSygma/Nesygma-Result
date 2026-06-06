fof(premise_1, axiom, ! [X] : (virus_occurs_in(X) => can_get_monkeypox(X))).
fof(premise_2, axiom, ? [X] : (animal(X) & virus_occurs_in(X))).
fof(premise_3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise_4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise_5a, axiom, symptom_of_monkeypox(fever)).
fof(premise_5b, axiom, symptom_of_monkeypox(headache)).
fof(premise_5c, axiom, symptom_of_monkeypox(muscle_pains)).
fof(premise_5d, axiom, symptom_of_monkeypox(tiredness)).
fof(premise_6, axiom, ! [X] : ((person(X) & gets_flu(X)) => feels_tired(X))).
fof(goal, conjecture, symptom_of_monkeypox(coughing)).