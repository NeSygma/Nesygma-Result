% Positive: original conclusion as conjecture
fof(distinct, axiom, vladimir != ekaterina).

fof(premise1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(premise3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(premise4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).
fof(premise5, axiom, ~taiwan_citizen(vladimir) & ~manager_gazprom(vladimir)).
fof(premise6, axiom, can_register(ekaterina) | russian_official(ekaterina)).

fof(conclusion, conjecture, can_participate(ekaterina) | manager_gazprom(vladimir)).