% Axioms and conjecture for positive case
fof(axiom1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(axiom2, axiom, ! [X] : (invite_others_to_ceremony(X) => make_wedding_plans(X))).
fof(axiom3, axiom, ! [X] : (well_attended_wedding(X) => invite_others_to_ceremony(X))).
fof(axiom4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(axiom5, axiom, engaged(john) => ( ~invite_friends_to_ceremony(john) & make_wedding_plans(john) )).
fof(axiom6, axiom, larger_family(john) => ( well_attended_wedding(john) | invite_friends_to_ceremony(john) )).
fof(conjecture, conjecture, engaged(john)).