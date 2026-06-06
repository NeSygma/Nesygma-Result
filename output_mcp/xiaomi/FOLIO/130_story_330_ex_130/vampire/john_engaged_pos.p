fof(premise_1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(premise_2, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(premise_3, axiom, ! [X] : (well_attended_wedding(X) => invite_others(X))).
fof(premise_4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise_5, axiom, engaged(john) => (~invite_friends(john) & ~make_wedding_plans(john))).
fof(premise_6, axiom, larger_family(john) => (well_attended_wedding(john) | invite_friends(john))).
fof(goal, conjecture, engaged(john)).