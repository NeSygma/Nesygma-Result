fof(premise1, axiom, ! [X] : (can_register_to_vote_us(X) => can_participate_2024_election(X))).
fof(premise2, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote_us(X))).
fof(premise3a, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(premise3b, axiom, ! [X] : ~(has_us_citizenship(X) & has_taiwanese_citizenship(X))).
fof(premise4, axiom, ! [X] : (russian_federation_official(X) => ~has_taiwanese_citizenship(X))).
fof(premise5a, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(premise5b, axiom, ~manager_at_gazprom(vladimir)).
fof(premise6, axiom, can_register_to_vote_us(ekaterina) | russian_federation_official(ekaterina)).
fof(distinct_people, axiom, vladimir != ekaterina).
fof(conclusion_negation, conjecture, ~russian_federation_official(vladimir)).