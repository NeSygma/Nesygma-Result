fof(premise_1, axiom, ! [X] : (makes_wedding_plans(X) => engaged(X))).
fof(premise_2, axiom, ! [X] : (invites_others(X) => makes_wedding_plans(X))).
fof(premise_3, axiom, ! [X] : (well_attended_wedding(X) => invites_others(X))).
fof(premise_4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise_5, axiom, engaged(john) => (~invites_friends(john) & makes_wedding_plans(john))).
fof(premise_6, axiom, larger_family(john) => (well_attended_wedding(john) | invites_friends(john))).
fof(distinct_john, axiom, person(john)).
fof(goal_neg, conjecture, ~(~larger_family(john) & ~invites_others(john))).