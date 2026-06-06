fof(p1, axiom, ! [X] : (wedding_plans(X) => engaged(X))).
fof(p2, axiom, ! [X] : (invites(X) => wedding_plans(X))).
fof(p3, axiom, ! [X] : (well_attended(X) => invites(X))).
fof(p4, axiom, ? [X] : (well_attended(X) & larger_family(X))).
fof(p5, axiom, engaged(john) => (~invites(john) & ~wedding_plans(john))).
fof(p6, axiom, larger_family(john) => (well_attended(john) | invites(john))).
fof(goal, conjecture, ~larger_family(john) & ~invites(john)).