fof(all_make_wedding_plans_are_engaged, axiom, 
    ! [X] : (make_wedding_plans(X) => engaged(X))).

fof(all_inviting_others_make_wedding_plans, axiom, 
    ! [X] : (invites_others(X) => make_wedding_plans(X))).

fof(all_well_attended_weddings_invite_others, axiom, 
    ! [X] : (has_well_attended_wedding(X) => invites_others(X))).

fof(some_well_attended_have_larger_families, axiom, 
    ? [X] : (has_well_attended_wedding(X) & has_larger_family(X))).

fof(john_engaged_implies_not_both, axiom, 
    engaged(john) => ~(invites_others(john) & make_wedding_plans(john))).

fof(john_larger_family_implies_either, axiom, 
    has_larger_family(john) => (has_well_attended_wedding(john) | invites_others(john))).

fof(conclusion, conjecture, 
    (~has_larger_family(john) & ~invites_others(john))).