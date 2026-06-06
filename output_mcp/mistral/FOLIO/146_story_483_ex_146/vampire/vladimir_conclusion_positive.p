fof(premise1, axiom, ! [X] : (can_register_to_vote_us(X) => can_participate_2024_election_us(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register_to_vote_us(X))).
fof(premise3a, axiom, ! [X] : (us_citizen(X) | taiwanese_citizen(X))).
fof(premise3b, axiom, ! [X] : ~(us_citizen(X) & taiwanese_citizen(X))).
fof(premise4, axiom, ! [X] : (russian_federation_official(X) => ~taiwanese_citizen(X))).
fof(premise5a, axiom, ~taiwanese_citizen(vladimir)).
fof(premise5b, axiom, ~gazprom_manager(vladimir)).
fof(premise6, axiom, can_register_to_vote_us(ekaterina) | russian_federation_official(ekaterina)).
fof(distinct_entities, axiom, vladimir != ekaterina).
fof(conclusion, conjecture, ~russian_federation_official(vladimir)).