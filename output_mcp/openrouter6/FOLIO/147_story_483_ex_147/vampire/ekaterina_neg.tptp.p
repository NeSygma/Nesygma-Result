fof(premise1, axiom, ! [X] : (can_register_to_vote(X) => can_participate_election(X))).
fof(premise2, axiom, ! [X] : (us_citizen(X) => can_register_to_vote(X))).
fof(premise3, axiom, ! [X] : (us_citizen(X) | tw_citizen(X))).
fof(premise4, axiom, ! [X] : (russian_official(X) => ~tw_citizen(X))).
fof(premise5, axiom, (~tw_citizen(vladimir) & ~manager_gazprom(vladimir))).
fof(premise6, axiom, (can_register_to_vote(ekaterina) | russian_official(ekaterina))).
fof(neg_conclusion, conjecture, (~can_participate_election(ekaterina) & ~manager_gazprom(ekaterina))).