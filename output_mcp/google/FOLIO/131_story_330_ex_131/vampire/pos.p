fof(p1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(p2, axiom, ! [X] : (invites_others(X) => makes_wedding_plans(X))).
fof(p3, axiom, ! [X] : (well_attended_wedding(X) => invites_others(X))).
fof(p5, axiom, engaged(john) => ~(invites_others(john) & makes_wedding_plans(john))).
fof(p6, axiom, larger_family(john) => (well_attended_wedding(john) | invites_others(john))).
fof(goal, conjecture, ~larger_family(john) & ~invites_others(john)).