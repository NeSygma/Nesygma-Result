% Negative version: negated conclusion as conjecture
% Conclusion: There is an animal. Negated: There is no animal.

fof(premise_1, axiom, ! [X] : (monkeypox_virus_in(X) => may_get_monkeypox(X))).
fof(premise_2, axiom, ? [X] : (animal(X) & monkeypox_virus_can_occur_in(X))).
fof(premise_3, axiom, ! [X] : (human(X) => mammal(X))).
fof(premise_4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise_5, axiom, ! [X] : (has_monkeypox(X) => (fever(X) & headache(X) & muscle_pains(X) & tiredness(X)))).
fof(premise_6, axiom, ! [X] : (gets_flu(X) => feels_tired(X))).

fof(conclusion_neg, conjecture, ~ ? [X] : animal(X)).