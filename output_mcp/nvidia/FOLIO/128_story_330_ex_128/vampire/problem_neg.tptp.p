fof(axiom1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(axiom2, axiom, ! [X] : (invites_to_ceremony(X) => makes_wedding_plans(X))).
fof(axiom3, axiom, ! [X] : (has_well_attended_wedding(X) => invites_to_ceremony(X))).
fof(axiom4, axiom, ? [X] : (has_well_attended_wedding(X) & larger_family(X))).
fof(axiom5, axiom, engaged(john) => ~ (invites_friends(john) & makes_wedding_plans(john))).
fof(axiom6, axiom, larger_family(john) => (has_well_attended_wedding(john) | invites_friends(john))).
fof(conjecture, conjecture, ~larger_family(john)).