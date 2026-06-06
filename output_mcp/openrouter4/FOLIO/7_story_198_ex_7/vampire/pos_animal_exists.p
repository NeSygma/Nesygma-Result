% Positive file: conclusion "There is an animal" as conjecture
fof(premise1, axiom, ! [X] : (monkeypox_virus_occurs_in(X) => monkeypox(X))).
fof(premise2, axiom, ? [X] : (animal(X) & monkeypox_virus_occurs_in(X))).
fof(premise3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise5, axiom, ! [X] : (monkeypox(X) => (has_symptom(X, fever) & has_symptom(X, headache) & has_symptom(X, muscle_pains) & has_symptom(X, tiredness)))).
fof(premise6, axiom, ! [X] : ((human(X) & flu(X)) => tired(X))).
fof(conclusion, conjecture, ? [X] : animal(X)).