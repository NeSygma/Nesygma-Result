fof(premise1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invites_others(X) => makes_wedding_plans(X))).
fof(premise3, axiom, ! [X] : (well_attended_wedding(X) => invites_others(X))).
fof(premise4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise5, axiom, engaged(john) => ~(invites_others(john) & makes_wedding_plans(john))).
fof(premise6, axiom, larger_family(john) => (well_attended_wedding(john) | invites_others(john))).
fof(distinct, axiom, john = john).

fof(goal, conjecture, engaged(john)).