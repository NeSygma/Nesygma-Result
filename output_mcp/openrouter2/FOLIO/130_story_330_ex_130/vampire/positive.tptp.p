fof(all_make_wedding_plans_engaged, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(all_invite_others_make_wedding_plans, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(all_well_attended_invite_others, axiom, ! [X] : (well_attended_wedding(X) => invite_others(X))).
fof(exists_well_attended_larger_family, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(engaged_john_implies_not_invite_friends_and_not_make_plans, axiom, (engaged(john) => (~invite_friends(john) & ~make_wedding_plans(john)))).
fof(larger_family_john_implies_well_attended_or_invite_friends, axiom, (larger_family(john) => (well_attended_wedding(john) | invite_friends(john)))).
fof(conjecture, conjecture, engaged(john)).