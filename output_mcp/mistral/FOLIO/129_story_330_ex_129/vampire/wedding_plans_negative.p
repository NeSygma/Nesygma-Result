fof(all_make_plans_are_engaged, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(all_invites_make_plans, axiom, ! [X] : (invites_friends(X) => make_wedding_plans(X))).
fof(well_attended_implies_invites, axiom, ! [X] : (has_well_attended_wedding(X) => invites_friends(X))).
fof(some_well_attended_have_larger_families, axiom, ? [X] : (has_well_attended_wedding(X) & has_larger_family(X))).
fof(john_engaged_implies_not_both, axiom, engaged(john) => ~(invites_friends(john) & make_wedding_plans(john))).
fof(larger_family_implies_either, axiom, has_larger_family(john) => (has_well_attended_wedding(john) | invites_friends(john))).
fof(goal_negation, conjecture, has_larger_family(john)).