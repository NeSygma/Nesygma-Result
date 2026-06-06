% Monkeypox problem - Negative version
% Premises
fof(premise_1, axiom, ! [X] : (virus_occurs_in(X) => may_get_monkeypox(X))).
fof(premise_2, axiom, ? [X] : (animal(X) & virus_occurs_in(monkeypox_virus, X))).
fof(premise_3, axiom, human(human_constant)).
fof(premise_4, axiom, ! [X] : (mammal(X) => animal(X))).
fof(premise_5, axiom, ! [X] : (has_monkeypox(X) => (has_fever(X) & has_headache(X) & has_muscle_pains(X) & has_tiredness(X)))).
fof(premise_6, axiom, ! [X] : (human(X) & has_flu(X) => feels_tired(X))).

% Distinctness
fof(distinct, axiom, human_constant != monkeypox_virus).

% Negated conclusion
fof(goal_negated, conjecture, ~(? [X] : animal(X))).  % There is NO animal