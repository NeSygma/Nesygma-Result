fof(premise_1, axiom, ! [X] : (can_register_to_vote(X) => can_participate_2024(X))).
fof(premise_2, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote(X))).
fof(premise_3, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(premise_4, axiom, ! [X] : (is_russian_federation_official(X) => ~has_taiwanese_citizenship(X))).
fof(premise_5a, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(premise_5b, axiom, ~is_manager_at_gazprom(vladimir)).
fof(premise_6, axiom, can_register_to_vote(ekaterina) | is_russian_federation_official(ekaterina)).
fof(conclusion_negation, conjecture, can_register_to_vote(ekaterina) & can_participate_2024(vladimir)).