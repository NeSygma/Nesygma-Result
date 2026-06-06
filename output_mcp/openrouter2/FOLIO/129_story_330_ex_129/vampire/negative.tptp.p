fof(axiom1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(axiom2, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(axiom3, axiom, ! [X] : (well_attended_wedding(X) => invite_others(X))).
fof(axiom4, axiom, well_attended_wedding(a) & larger_family(a)).
fof(distinct, axiom, a != john).
fof(axiom5, axiom, engaged(john) => (~invite_others(john) & make_wedding_plans(john))).
fof(axiom6, axiom, larger_family(john) => (well_attended_wedding(john) | invite_others(john))).
fof(conjecture, conjecture, larger_family(john)).