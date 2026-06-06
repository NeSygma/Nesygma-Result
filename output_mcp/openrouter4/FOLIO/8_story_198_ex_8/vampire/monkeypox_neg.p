% Negative test: "Someone gets the flu" as conjecture (negation of "no one gets the flu")
fof(premise1, axiom, ! [X] : (monkeypox_virus_occurs_in(X) => may_get_monkeypox(X))).
fof(premise2, axiom, ? [X] : (animal(X) & monkeypox_virus_occurs_in(X))).
fof(premise3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise5, axiom, ! [X] : (gets_monkeypox(X) => (has_fever(X) & has_headache(X) & has_muscle_pains(X) & is_tired(X)))).
fof(premise6, axiom, ! [X] : ((human(X) & gets_flu(X)) => feels_tired(X))).
fof(goal, conjecture, ? [X] : gets_flu(X)).