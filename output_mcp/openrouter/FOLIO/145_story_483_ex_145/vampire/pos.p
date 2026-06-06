% Positive test: is Vladimir a Russian federation official?
fof(distinct, axiom, vladimir != ekaterina).

fof(rule1, axiom, ! [X] : (can_register(X) => participate_2024(X))).
fof(rule2, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(rule3, axiom, ! [X] : (us_citizen(X) | tw_citizen(X))).
fof(rule4, axiom, ! [X] : (rf_official(X) => ~tw_citizen(X))).
fof(vladimir_info, axiom, ~tw_citizen(vladimir) & ~manager_gazprom(vladimir)).
fof(ekaterina_info, axiom, can_register(ekaterina) | rf_official(ekaterina)).

fof(goal, conjecture, rf_official(vladimir)).