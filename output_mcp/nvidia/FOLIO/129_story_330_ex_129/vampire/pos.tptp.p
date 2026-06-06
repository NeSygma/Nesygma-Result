fof(axiom_1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(axiom_2, axiom, ! [X] : (invite_others_to_ceremony(X) => make_wedding_plans(X))).
fof(axiom_3, axiom, ! [X] : (well_attended_wedding(X) => invite_others_to_ceremony(X))).
fof(axiom_4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(axiom_5, axiom, engaged(john) => (~invite_friends_to_ceremony(john) & ~make_wedding_plans(john))).
fof(axiom_6, axiom, larger_family(john) => (well_attended_wedding(john) | invite_friends_to_ceremony(john))).
fof(conjecture, conjecture, ~larger_family(john)).