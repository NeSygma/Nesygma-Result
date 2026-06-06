% Axioms
fof(axiom_1, axiom, ! [X] : (can_register_to_vote_us(X) => participates_2024_us_pres(X))).
fof(axiom_2, axiom, ! [X] : (us_citizenship(X) => can_register_to_vote_us(X))).
fof(axiom_3, axiom, ! [X] : (us_citizenship(X) | taiwanese_citizenship(X))).
fof(axiom_4, axiom, ! [X] : (russian_official(X) & taiwanese_citizenship(X) => false)).
fof(axiom_5a, axiom, ~taiwanese_citizenship(vladimir)).
fof(axiom_5b, axiom, ~manager_at_gazprom(vladimir)).
fof(axiom_6, axiom, can_register_to_vote_us(ekaterina) | russian_official(ekaterina)).
fof(conjecture, conjecture, russian_official(vladimir)).