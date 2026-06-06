% Positive test: John is engaged
fof(distinct_consts, axiom, john != other).
fof(rule1, axiom, ! [X] : (make_plan(X) => engaged(X))).
fof(rule2, axiom, ! [X] : (invite(X) => make_plan(X))).
fof(rule3, axiom, ! [X] : (well_attended_wedding(X) => invite(X))).
fof(rule4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(rule5, axiom, engaged(john) => (~invite(john) & ~make_plan(john))).
fof(rule6, axiom, larger_family(john) => (well_attended_wedding(john) | invite(john))).
fof(goal, conjecture, engaged(john)).