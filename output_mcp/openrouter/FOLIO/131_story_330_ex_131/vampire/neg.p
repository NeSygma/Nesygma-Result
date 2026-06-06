% Negative version: conjecture is negation of conclusion
fof(rule1, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(rule2, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(rule3, axiom, ! [X] : (well_attended_wedding(X) => invite_others(X))).
fof(rule4, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(rule5, axiom, engaged(john) => (~invite_others(john) & ~make_wedding_plans(john))).
fof(rule6, axiom, larger_family(john) => (well_attended_wedding(john) | invite_others(john))).
fof(conj_neg, conjecture, (larger_family(john) | invite_others(john))).