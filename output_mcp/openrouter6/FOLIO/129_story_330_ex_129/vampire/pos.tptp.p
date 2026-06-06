fof(premise1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invite(X) => make_wedding_plans(X))).
fof(premise3, axiom, ! [X] : (well_attended_wedding(X) => invite(X))).
fof(premise4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise5, axiom, engaged(john) => (~invite(john) & ~make_wedding_plans(john))).
fof(premise6, axiom, larger_family(john) => (well_attended_wedding(john) | invite(john))).
fof(conclusion, conjecture, ~larger_family(john)).