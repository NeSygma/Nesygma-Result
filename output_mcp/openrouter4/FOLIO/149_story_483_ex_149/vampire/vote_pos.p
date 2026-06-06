% Positive file: original conclusion as conjecture
fof(premise1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(premise3, axiom, ! [X] : (us_citizen(X) <=> ~taiwanese_citizen(X))).
fof(premise4, axiom, ! [X] : (russian_official(X) => ~taiwanese_citizen(X))).
fof(premise5, axiom, (~taiwanese_citizen(vladimir) & ~manager_gazprom(vladimir))).
fof(premise6, axiom, (can_register(ekaterina) | russian_official(ekaterina))).
fof(distinct, axiom, vladimir != ekaterina).
fof(conclusion, conjecture, ~(can_register(ekaterina) & can_participate(vladimir))).