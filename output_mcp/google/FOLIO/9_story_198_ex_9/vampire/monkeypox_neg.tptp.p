fof(p1, axiom, ! [X] : (monkeypox_virus_in(X) => may_get_monkeypox(X))).
fof(p2, axiom, ? [A] : monkeypox_virus_can_occur_in(A)).
fof(p3, axiom, ! [X] : (human(X) => mammal(X))).
fof(p4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(p5a, axiom, symptom_of_monkeypox(fever)).
fof(p5b, axiom, symptom_of_monkeypox(headache)).
fof(p5c, axiom, symptom_of_monkeypox(muscle_pains)).
fof(p5d, axiom, symptom_of_monkeypox(tiredness)).
fof(p6, axiom, ! [X] : (get_flu(X) => feel_tired(X))).
fof(goal, conjecture, ~symptom_of_monkeypox(coughing)).