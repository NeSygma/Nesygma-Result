% Negative test: Does the negation of the conclusion (John has a larger family) follow?
fof(premise1, axiom, ! [X] : (wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invite_ceremony(X) => wedding_plans(X))).
fof(premise3, axiom, ! [X] : (well_attended(X) => invite_ceremony(X))).
fof(premise4, axiom, ? [X] : (well_attended(X) & larger_family(X))).
fof(premise5, axiom, (engaged(john) => (~invite_friends(john) & ~wedding_plans(john)))).
fof(premise6, axiom, (larger_family(john) => (well_attended(john) | invite_friends(john)))).
fof(conclusion_neg, conjecture, larger_family(john)).