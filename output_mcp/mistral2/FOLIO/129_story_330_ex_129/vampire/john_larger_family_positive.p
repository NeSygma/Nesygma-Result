fof(all_makes_wedding_plans_are_engaged, axiom,
    ! [X] : (makes_wedding_plans(X) => engaged(X))).

fof(all_inviting_others_make_plans, axiom,
    ! [X] : (invites_others(X) => makes_wedding_plans(X))).

fof(well_attended_implies_invites_others, axiom,
    ! [X] : (has_well_attended_wedding(X) => invites_others(X))).

fof(some_well_attended_have_larger_family, axiom,
    ? [X] : (has_well_attended_wedding(X) & has_larger_family(X))).

fof(john_engaged_implies_not_both, axiom,
    engaged(john) => ~(invites_others(john) & makes_wedding_plans(john))).

fof(john_larger_family_implies_either, axiom,
    has_larger_family(john) => (has_well_attended_wedding(john) | invites_others(john))).

fof(conclusion, conjecture,
    ~has_larger_family(john)).