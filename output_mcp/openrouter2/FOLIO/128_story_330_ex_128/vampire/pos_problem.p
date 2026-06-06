fof(rule1, axiom, ![X] : (make_wedding_plans(X) => engaged(X))).
fof(rule2, axiom, ![X] : (invites(X) => make_wedding_plans(X))).
fof(rule3, axiom, ![X] : (well_attended_wedding(X) => invites(X))).
fof(rule5, axiom, (engaged(john) => (~invites_friends(john) & ~make_wedding_plans(john)))).
fof(rule6, axiom, (larger_family(john) => (well_attended_wedding(john) | invites_friends(john)))).
fof(exist1, axiom, ?[X] : (well_attended_wedding(X) & larger_family(X))).
fof(goal, conjecture, larger_family(john)).