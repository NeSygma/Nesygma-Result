fof(can_register_participate, axiom, ! [X] : (can_register_to_vote(X) => participates_in_election(X))).
fof(us_citizen_register, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote(X))).
fof(citizenship_disjunction, axiom, ! [X] : (has_us_citizenship(X) v has_taiwanese_citizenship(X))).
fof(russian_no_taiwan, axiom, ! [X] : (is_russian_federation_official(X) => ~has_taiwanese_citizenship(X))).
fof(vladimir_not_taiwan, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(vladimir_not_manager, axiom, ~is_manager_at_gazprom(vladimir)).
fof(ekaterina_register_or_russian, axiom, can_register_to_vote(ekaterina) v is_russian_federation_official(ekaterina)).
fof(distinct_vladimir_ekaterina, axiom, vladimir != ekaterina).
fof(conclusion, conjecture, is_russian_federation_official(vladimir)).