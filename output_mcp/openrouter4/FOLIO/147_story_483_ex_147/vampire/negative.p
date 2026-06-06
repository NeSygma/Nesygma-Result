fof(premise_1, axiom, ! [X] : (can_register_vote_us(X) => can_participate_us_election(X))).
fof(premise_2, axiom, ! [X] : (has_us_citizenship(X) => can_register_vote_us(X))).
fof(premise_3, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(premise_4, axiom, ! [X] : (russian_official(X) => ~has_taiwanese_citizenship(X))).
fof(premise_5, axiom, ~has_taiwanese_citizenship(vladimir) & ~manager_at_gazprom(vladimir)).
fof(premise_6, axiom, can_register_vote_us(ekaterina) | russian_official(ekaterina)).
fof(distinct, axiom, ekaterina != vladimir).
fof(negated_conclusion, conjecture, ~(can_participate_us_election(ekaterina) | manager_at_gazprom(ekaterina))).