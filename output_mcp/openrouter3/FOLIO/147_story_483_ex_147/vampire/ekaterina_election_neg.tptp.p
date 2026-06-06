% Premises
fof(premise1, axiom, ! [X] : (can_register_vote_us(X) => can_participate_election(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register_vote_us(X))).
fof(premise3a, axiom, ! [X] : (us_citizen(X) | taiwanese_citizen(X))).
fof(premise3b, axiom, ! [X] : ~(us_citizen(X) & taiwanese_citizen(X))).
fof(premise4, axiom, ! [X] : (russian_official(X) => ~taiwanese_citizen(X))).
fof(premise5, axiom, ~taiwanese_citizen(vladimir) & ~manager_gazprom(vladimir)).
fof(premise6, axiom, can_register_vote_us(ekaterina) | russian_official(ekaterina)).

% Negated conclusion
fof(goal_neg, conjecture, ~(can_participate_election(ekaterina) | manager_gazprom(ekaterina))).