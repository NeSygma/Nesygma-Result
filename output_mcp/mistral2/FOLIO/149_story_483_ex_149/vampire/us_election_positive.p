fof(axiom1, axiom, ! [P] : (can_register_to_vote_us(P) => can_participate_2024_us_election(P))).
fof(axiom2, axiom, ! [P] : (citizenship(P, us_citizen) => can_register_to_vote_us(P))).
fof(axiom3, axiom, ! [P] : (citizenship(P, us_citizen) | citizenship(P, taiwanese_citizen))).
fof(axiom4, axiom, ! [P] : (russian_federation_official(P) => ~citizenship(P, taiwanese_citizen))).
fof(axiom5, axiom, (~citizenship(vladimir, taiwanese_citizen) & ~is_manager_at_gazprom(vladimir))).
fof(axiom6, axiom, (can_register_to_vote_us(ekaterina) | russian_federation_official(ekaterina))).
fof(conjecture, conjecture, ~(can_register_to_vote_us(ekaterina) & can_participate_2024_us_election(vladimir))).