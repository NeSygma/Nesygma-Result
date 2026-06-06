fof(premise1, axiom, ! [X] : (can_register_to_vote(X) => can_participate_election(X))).
fof(premise2, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote(X))).
fof(premise3, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(premise4, axiom, ! [X] : (is_russian_official(X) => ~has_taiwanese_citizenship(X))).
fof(premise5a, axiom, ~has_taiwanese_citizenship(vladimir)).
fof(premise5b, axiom, ~is_manager_at_gazprom(vladimir)).
fof(premise6, axiom, can_register_to_vote(ekaterina) | is_russian_official(ekaterina)).
fof(distinct, axiom, vladimir != ekaterina).
fof(goal, conjecture, is_russian_official(vladimir)).