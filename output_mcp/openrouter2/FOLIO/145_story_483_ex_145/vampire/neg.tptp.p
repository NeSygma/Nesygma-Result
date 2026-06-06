fof(can_register_participate, axiom, ! [X] : (can_register_to_vote_in_us(X) => can_participate_in_2024_presidential_election(X))).
fof(has_us_can_register, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote_in_us(X))).
fof(us_or_taiwan, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(no_russian_taiwan, axiom, ! [X] : (is_russian_federation_official(X) => ~has_taiwanese_citizenship(X))).
fof(vladimir_not_taiwan, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(vladimir_not_manager, axiom, ~is_manager_at_gazprom(vladimir)).
fof(ekaterina_or_official, axiom, (can_register_to_vote_in_us(ekaterina) | is_russian_federation_official(ekaterina))).
fof(distinct_vladimir_ekaterina, axiom, vladimir != ekaterina).
fof(conjecture, conjecture, ~is_russian_federation_official(vladimir)).