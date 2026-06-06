fof(p1, axiom, ! [X] : (can_register_to_vote(X) => can_participate_in_2024_election(X))).
fof(p2, axiom, ! [X] : (has_us_citizenship(X) => can_register_to_vote(X))).
fof(p3, axiom, ! [X] : (has_us_citizenship(X) | has_taiwanese_citizenship(X))).
fof(p4, axiom, ! [X] : (is_russian_official(X) => ~has_taiwanese_citizenship(X))).
fof(p5, axiom, (~has_taiwanese_citizenship(vladimir) & ~is_manager_at_gazprom(vladimir))).
fof(p6, axiom, (can_register_to_vote(ekaterina) | is_russian_official(ekaterina))).
fof(goal, conjecture, ~is_russian_official(vladimir)).