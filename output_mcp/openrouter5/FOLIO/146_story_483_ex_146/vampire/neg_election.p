% Negative file: negated conclusion as conjecture
% Negated conclusion: Vladimir IS a Russian federation official

fof(premise_1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(premise_2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(premise_3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(premise_4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).
fof(premise_5, axiom, (~taiwan_citizen(vladimir) & ~manager_gazprom(vladimir))).
fof(premise_6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).

fof(conclusion_neg, conjecture, russian_official(vladimir)).