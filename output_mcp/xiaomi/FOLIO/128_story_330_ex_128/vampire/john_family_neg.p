fof(p1, axiom, ! [X] : (wedding_planner(X) => engaged(X))).
fof(p2, axiom, ! [X] : (invites_others(X) => wedding_planner(X))).
fof(p3, axiom, ! [X] : (well_attended_wedding(X) => invites_others(X))).
fof(p4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(p5, axiom, engaged(john) => (~invites_friends(john) & ~wedding_planner(john))).
fof(p6, axiom, larger_family(john) => (well_attended_wedding(john) | invites_friends(john))).
fof(goal, conjecture, ~larger_family(john)).