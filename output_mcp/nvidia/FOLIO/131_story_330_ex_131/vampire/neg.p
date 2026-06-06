fof(axiom_1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(axiom_2, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(axiom_3, axiom, ! [X] : (well_attended(X) => invite_others(X))).
fof(axiom_4, axiom, ? [X] : (well_attended(X) & larger_family(X))).
fof(axiom_5, axiom, (engaged(john) => (~invite_friends(john) & make_wedding_plans(john)))).
fof(axiom_6, axiom, (larger_family(john) => (well_attended(john) | invite_friends(john)))).
fof(goal, conjecture, (larger_family(john) | invite_others(john))).