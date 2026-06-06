% Negative version: Negated conclusion as conjecture
fof(premise_1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(premise_2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(premise_3, axiom, ! [X] : (us_citizen(X) | tw_citizen(X))).
fof(premise_4, axiom, ! [X] : (russian_official(X) => ~tw_citizen(X))).
fof(premise_5, axiom, ~tw_citizen(vladimir) & ~gazprom_manager(vladimir)).
fof(premise_6, axiom, can_register(ekaterina) | russian_official(ekaterina)).
fof(distinct_entities, axiom, ekaterina != vladimir).
fof(conclusion, conjecture, can_register(ekaterina) & can_participate(vladimir)).