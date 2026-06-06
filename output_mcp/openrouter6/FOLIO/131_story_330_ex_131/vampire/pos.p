fof(premise1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(premise2, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(premise3, axiom, ! [X] : (well_attended_wedding(X) => invite_others(X))).
fof(premise4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(premise5, axiom, engaged(john) => (~invite_friends(john) & ~make_wedding_plans(john))).
fof(premise6, axiom, larger_family(john) => (well_attended_wedding(john) | invite_friends(john))).
fof(conclusion, conjecture, ~larger_family(john) & ~invite_others(john)).