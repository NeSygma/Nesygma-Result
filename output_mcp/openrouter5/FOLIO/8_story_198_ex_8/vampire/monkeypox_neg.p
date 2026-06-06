% Negative version: negated conclusion as conjecture
% Negated conclusion: Someone gets the flu.

fof(premise_1, axiom, ! [X] : (monkeypox_virus_in(X) => may_get_monkeypox(X))).
fof(premise_2, axiom, ? [X] : (animal(X) & monkeypox_virus_in(X))).
fof(premise_3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise_4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise_5, axiom, ! [X] : (gets_monkeypox(X) => (has_fever(X) & has_headache(X) & has_muscle_pains(X) & has_tiredness(X)))).
fof(premise_6, axiom, ! [X] : (gets_flu(X) => feels_tired(X))).

% Negated conclusion: Someone gets the flu.
fof(goal_neg, conjecture, ? [X] : gets_flu(X)).