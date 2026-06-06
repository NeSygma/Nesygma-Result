fof(premise1, axiom, ! [X] : (can_register_to_vote_us(X) => can_participate_2024_election(X))).
fof(premise2, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote_us(X))).
fof(premise3, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(premise4, axiom, ! [X] : (is_russian_federation_official(X) => ~has_taiwanese_citizenship(X))).
fof(premise5a, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(premise5b, axiom, ~is_manager_at_gazprom(vladimir)).
fof(premise6, axiom, can_register_to_vote_us(ekaterina) | is_russian_federation_official(ekaterina)).

fof(conclusion_negation, conjecture, ~is_russian_federation_official(vladimir)).