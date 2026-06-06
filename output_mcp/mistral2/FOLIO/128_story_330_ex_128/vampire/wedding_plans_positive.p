fof(premise1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invites_friends_to_ceremony(X) => makes_wedding_plans(X))).
fof(premise3, axiom, ! [X] : (has_well_attended_wedding(X) => invites_friends_to_ceremony(X))).
fof(premise4, axiom, ? [X] : (has_well_attended_wedding(X) & has_larger_family(X))).
fof(premise5, axiom, engaged(john) => ~(invites_friends_to_ceremony(john) & makes_wedding_plans(john))).
fof(premise6, axiom, has_larger_family(john) => (has_well_attended_wedding(john) | invites_friends_to_ceremony(john))).

fof(goal, conjecture, has_larger_family(john)).