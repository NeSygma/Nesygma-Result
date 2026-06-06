fof(p1, axiom, ! [X] : (wedding_plans(X) => engaged(X))).
fof(p2, axiom, ! [X] : (invite_others(X) => wedding_plans(X))).
fof(p3, axiom, ! [X] : (well_attended(X) => invite_others(X))).
fof(p4, axiom, ? [X] : (well_attended(X) & larger_family(X))).
fof(p5, axiom, engaged(john) => (~invite_others(john) & ~wedding_plans(john))).
fof(p6, axiom, larger_family(john) => (well_attended(john) | invite_others(john))).
fof(goal, conjecture, ~engaged(john)).