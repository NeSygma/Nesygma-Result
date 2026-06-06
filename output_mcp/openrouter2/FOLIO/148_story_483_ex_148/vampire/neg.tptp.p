fof(distinct, axiom, vladimir != ekaterina).
fof(rule1, axiom, ! [X] : (can_register(X) => can_participate(X))).
fof(rule2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(rule3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(rule4, axiom, ! [X] : (rf_official(X) => ~taiwan_citizen(X))).
fof(rule5, axiom, ~taiwan_citizen(vladimir) & ~manager_gazprom(vladimir)).
fof(rule6, axiom, can_register(ekaterina) | rf_official(ekaterina)).
fof(goal, conjecture, ~can_participate(ekaterina) & ~manager_gazprom(vladimir)).