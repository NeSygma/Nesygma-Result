fof(premise1, axiom, ! [P] : (can_register_to_vote_in_us(P) => can_participate_in_2024_us_election(P))).
fof(premise2, axiom, ! [P] : (has_us_citizenship(P) => can_register_to_vote_in_us(P))).
fof(premise3, axiom, ! [P] : (has_us_citizenship(P) | has_taiwanese_citizenship(P))).
fof(premise4, axiom, ! [P] : (is_russian_federation_official(P) => ~has_taiwanese_citizenship(P))).
fof(premise5a, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(premise5b, axiom, ~is_manager_at_gazprom(vladimir)).
fof(premise6, axiom, can_register_to_vote_in_us(ekaterina) | is_russian_federation_official(ekaterina)).
fof(conclusion, conjecture, can_participate_in_2024_us_election(ekaterina) | is_manager_at_gazprom(vladimir)).