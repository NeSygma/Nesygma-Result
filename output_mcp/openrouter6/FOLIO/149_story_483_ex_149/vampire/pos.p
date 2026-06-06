fof(premise1, axiom, ! [X] : (can_register_to_vote(X) => can_participate_election(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register_to_vote(X))).
fof(premise3, axiom, ! [X] : (us_citizen(X) | taiwanese_citizen(X))).
fof(premise4, axiom, ! [X] : (russian_official(X) => ~taiwanese_citizen(X))).
fof(premise5, axiom, ~taiwanese_citizen(vladimir) & ~manager_gazprom(vladimir)).
fof(premise6, axiom, can_register_to_vote(ekaterina) | russian_official(ekaterina)).
fof(distinct, axiom, vladimir != ekaterina).
fof(conclusion, conjecture, ~(can_register_to_vote(ekaterina) & can_participate_election(vladimir))).