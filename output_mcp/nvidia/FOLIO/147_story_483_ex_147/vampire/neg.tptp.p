fof(distinct_constants, axiom, (vladimir != ekaterina)).
fof(premise1, axiom, ! [X] : (can_register_to_vote_in_us(X) => can_participate_in_2024_presidential_election(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register_to_vote_in_us(X))).
fof(premise3, axiom, ! [X] : (us_citizen(X) | taiwan_citizen(X))).
fof(premise4, axiom, ! [X] : (rus_official(X) => ~taiwan_citizen(X))).
fof(premise5a, axiom, ~taiwan_citizen(vladimir)).
fof(premise5b, axiom, ~manager_at_gazprom(vladimir)).
fof(premise6, axiom, can_register_to_vote_in_us(ekaterina) | rus_official(ekaterina)).
fof(conclusion_neg, conjecture, ~(can_participate_in_2024_presidential_election(ekaterina) | manager_at_gazprom(ekaterina))).