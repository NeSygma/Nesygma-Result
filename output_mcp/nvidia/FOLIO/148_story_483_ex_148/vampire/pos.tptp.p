fof(axiom_can_reg_vote_impl_participate, axiom, ! [X] : (can_register_to_vote_in_us(X) => can_participate_in_2024_presidential_election(X))).
fof(axiom_us_citizen_impl_reg_vote, axiom, ! [X] : (us_citizen(X) => can_register_to_vote_in_us(X))).
fof(axiom_either_citizen, axiom, ! [X] : (us_citizen(X) | taiwanese_citizen(X))).
fof(axiom_no_russian_taiwan_citizen, axiom, ! [X] : (russian_official(X) => ~taiwanese_citizen(X))).
fof(axiom_vladimir_not_taiwan_citizen, axiom, ~taiwanese_citizen(vladimir)).
fof(axiom_vladimir_not_manager, axiom, ~manager_at_gazprom(vladimir)).
fof(axiom_ekaterina_register_or_official, axiom, can_register_to_vote_in_us(ekaterina) | russian_official(ekaterina)).
fof(axiom_distinct_vladimir_ekaterina, axiom, vladimir != ekaterina).
fof(conjecture_target, conjecture, can_participate_in_2024_presidential_election(ekaterina) | manager_at_gazprom(vladimir)).