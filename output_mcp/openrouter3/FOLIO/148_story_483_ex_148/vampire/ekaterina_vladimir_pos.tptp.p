% Positive version: conclusion as conjecture
fof(rule_1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(rule_2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(rule_3, axiom, ! [X] : (us_citizen(X) | taiwanese_citizen(X))).
fof(rule_4, axiom, ! [X] : (russian_official(X) => ~taiwanese_citizen(X))).
fof(fact_5, axiom, ~taiwanese_citizen(vladimir) & ~gazprom_manager(vladimir)).
fof(fact_6, axiom, can_register(ekaterina) | russian_official(ekaterina)).
fof(distinct_entities, axiom, ekaterina != vladimir).
fof(goal, conjecture, can_participate(ekaterina) | gazprom_manager(vladimir)).