fof(axiom_1, axiom, ! [X] : (can_register_us(X) => can_participate_2024_us(X))).
fof(axiom_2, axiom, ! [X] : (us_citizen(X) => can_register_us(X))).
fof(axiom_3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(axiom_4, axiom, ! [X] : (russian_official(X) => ~taiwan_citizen(X))).
fof(axiom_5a, axiom, ~taiwan_citizen(vladimir)).
fof(axiom_5b, axiom, ~manager_gazprom(vladimir)).
fof(axiom_6, axiom, (can_register_us(ekaterina) | russian_official(ekaterina))).
fof(conjecture, conjecture, ~(can_register_us(ekaterina) & can_participate_2024_us(vladimir))).