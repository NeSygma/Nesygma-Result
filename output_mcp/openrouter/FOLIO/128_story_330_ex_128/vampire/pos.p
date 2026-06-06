% Positive version
fof(rule1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(rule2, axiom, ! [X] : (invites_others(X) => makes_wedding_plans(X))).
fof(rule3, axiom, ! [X] : (well_attended_wedding(X) => invites_others(X))).
fof(rule4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(john_rule1, axiom, engaged(john) => (~invites_others(john) & ~makes_wedding_plans(john))).
fof(john_rule2, axiom, larger_family(john) => (well_attended_wedding(john) | invites_others(john))).
fof(goal, conjecture, larger_family(john)).