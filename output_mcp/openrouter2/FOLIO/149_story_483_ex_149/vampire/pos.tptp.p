fof(can_register_participate, axiom, ! [X] : (can_register(X) => participate(X))).
fof(us_citizen_can_register, axiom, ! [X] : (us_citizen(X) => can_register(X))).
fof(us_or_taiwan, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(no_rfo_taiwan, axiom, ! [X] : (rfo(X) => ~taiwan_citizen(X))).
fof(vladimir_not_taiwan, axiom, ~taiwan_citizen(vladimir)).
fof(vladimir_not_manager, axiom, ~manager_gazprom(vladimir)).
fof(ekaterina_register_or_rfo, axiom, can_register(ekaterina) | rfo(ekaterina)).
fof(distinct_vladimir_ekaterina, axiom, vladimir != ekaterina).
fof(conjecture, conjecture, can_register(ekaterina) & participate(vladimir)).