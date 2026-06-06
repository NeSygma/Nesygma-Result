fof(make_plans_engaged, axiom, ! [X] : (make_wedding_plans(X) => engaged(X))).
fof(invite_makes_plans, axiom, ! [X] : (invite_others(X) => make_wedding_plans(X))).
fof(well_attended_invite, axiom, ! [X] : (well_attended_wedding(X) => invite_others(X))).
fof(exist_well_larger, axiom, ? [X] : (well_attended_wedding(X) & larger_family(X))).
fof(john_engaged_not_invite_not_plans, axiom, engaged(john) => (~invite_others(john) & ~make_wedding_plans(john))).
fof(john_larger_family_or_well_or_invite, axiom, larger_family(john) => (well_attended_wedding(john) | invite_others(john))).
fof(conjecture, conjecture, larger_family(john) | invite_others(john)).